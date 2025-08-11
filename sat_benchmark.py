# sat_benchmark.py
import random, time, math, hashlib
from typing import List, Tuple, Optional, Dict

# ----------------------------
# CNF model: list of clauses, each clause is a list of ints:
# variable i is encoded as +i for x_i and -i for ¬x_i (1-based indices)
# ----------------------------

def set_seed(master_seed: int):
    random.seed(master_seed)

def generate_planted_3sat(n_vars: int, m_clauses: int, seed: int) -> Tuple[List[List[int]], List[int]]:
    """
    Generate a 3-SAT instance with a planted satisfying assignment.
    Returns (cnf, planted_assignment) where planted_assignment is a 0/1 list of length n_vars.
    Deterministic given (n_vars, m_clauses, seed).
    """
    rng = random.Random(seed)
    planted = [rng.randrange(2) for _ in range(n_vars)]  # 0/1 assignment
    cnf = []
    for _ in range(m_clauses):
        # pick 3 distinct vars
        vars3 = rng.sample(range(1, n_vars + 1), 3)
        clause = []
        # construct a clause satisfied by 'planted' (at least one literal matches planted)
        # choose literals independently, but if we accidentally make all three false, flip one to be true
        all_false = True
        for v in vars3:
            val = planted[v-1]   # 0 means x_v = False
            # choose literal sign with 50/50
            want_positive = rng.randrange(2) == 1
            lit = v if want_positive else -v
            clause.append(lit)
            # check if literal is satisfied by planted
            if (lit > 0 and val == 1) or (lit < 0 and val == 0):
                all_false = False
        if all_false:
            # force the first literal to be satisfied by planted
            v = vars3[0]
            if planted[v-1] == 1:
                clause[0] = v
            else:
                clause[0] = -v
        cnf.append(clause)
    return cnf, planted

def verify_cnf(cnf: List[List[int]], assignment01: List[int]) -> bool:
    """Check CNF is satisfied by 0/1 assignment."""
    n_vars = len(assignment01)
    for clause in cnf:
        sat = False
        for lit in clause:
            v = abs(lit)
            if v < 1 or v > n_vars:
                return False
            val = assignment01[v-1]
            lit_true = (lit > 0 and val == 1) or (lit < 0 and val == 0)
            if lit_true:
                sat = True
                break
        if not sat:
            return False
    return True

# ----------------------------
# Baseline solvers
# ----------------------------

def random_assignment_solver(n_vars: int, _cnf: List[List[int]], budget_ms: int = 50) -> Optional[List[int]]:
    """Try random assignments within a small time budget."""
    deadline = time.perf_counter() + budget_ms/1000.0
    best = None
    while time.perf_counter() < deadline:
        a = [random.randrange(2) for _ in range(n_vars)]
        if verify_cnf(_cnf, a):
            return a
    return best  # None

def greedy_local_search(cnf: List[List[int]], n_vars: int, max_iters: int = 2000) -> Optional[List[int]]:
    """
    Simple WalkSAT-style heuristic: start random, flip vars to reduce unsatisfied clauses.
    Not state-of-the-art, but a fair lightweight baseline.
    """
    # Build clause -> variables map
    rng = random
    assignment = [rng.randrange(2) for _ in range(n_vars)]
    # Helper to evaluate clause
    def clause_satisfied(clause, a):
        for lit in clause:
            v = abs(lit)
            val = a[v-1]
            if (lit > 0 and val == 1) or (lit < 0 and val == 0):
                return True
        return False
    for it in range(max_iters):
        if verify_cnf(cnf, assignment):
            return assignment
        # pick an unsatisfied clause
        unsat = [cl for cl in cnf if not clause_satisfied(cl, assignment)]
        if not unsat:  # rare
            return assignment
        clause = rng.choice(unsat)
        # pick a variable from the clause to flip; choose the one minimizing new unsatisfied count
        best_v = None
        best_score = None
        for lit in clause:
            v = abs(lit) - 1
            assignment[v] ^= 1
            # score = number of unsatisfied clauses
            score = 0
            for cl2 in cnf:
                if not clause_satisfied(cl2, assignment):
                    score += 1
            assignment[v] ^= 1
            if best_score is None or score < best_score:
                best_score = score
                best_v = v
        assignment[best_v] ^= 1
    return None

# ----------------------------
# Consciousness-solver hook (YOU IMPLEMENT THIS)
# ----------------------------

def consciousness_solve(cnf: List[List[int]], n_vars: int, time_budget_ms: int = 200, params: Dict = None) -> Optional[List[int]]:
    """
    Deterministic WalkSAT-style local search with efficient updates and restarts.
    - Determinism: all randomness is derived from SHA-256 of the CNF text.
    - Efficiency: maintains per-clause true literal counts and an unsatisfied set.
    - Restarts: multiple seeds/perturbations within the time budget.
    """
    if params is None:
        params = {}

    # Deterministic seed from CNF content
    cnf_text = ''.join(','.join(str(l) for l in clause) + ';' for clause in cnf)
    seed_bytes = hashlib.sha256(cnf_text.encode()).digest()
    seed = int.from_bytes(seed_bytes[:8], 'big') or 1

    # Deterministic RNG (xorshift32)
    class DRNG:
        def __init__(self, s: int): self.s = s & 0xFFFFFFFF
        def next_u32(self) -> int:
            x = self.s
            x ^= (x << 13) & 0xFFFFFFFF
            x ^= (x >> 17)
            x ^= (x << 5) & 0xFFFFFFFF
            self.s = x & 0xFFFFFFFF
            return self.s
        def rand(self) -> float: return (self.next_u32() & 0xFFFFFF) / float(1<<24)
        def randint(self, a: int, b: int) -> int:  # inclusive
            if b <= a: return a
            return a + (self.next_u32() % (b - a + 1))

    rng = DRNG(seed)

    # Build indices for fast updates
    m = len(cnf)
    pos_idx = [[] for _ in range(n_vars+1)]  # 1-based var -> clause indices
    neg_idx = [[] for _ in range(n_vars+1)]
    for ci, clause in enumerate(cnf):
        for lit in clause:
            v = abs(lit)
            if lit > 0: pos_idx[v].append(ci)
            else: neg_idx[v].append(ci)

    def init_assignment_from_seed(base_seed: int) -> List[int]:
        # Expand deterministic bits via chained hashing
        pool = hashlib.sha256(base_seed.to_bytes(8,'big')).digest()
        bits = []
        i = 0; p = bytearray(pool)
        while len(bits) < n_vars:
            if i == len(p):
                p = bytearray(hashlib.sha256(p).digest())
                i = 0
            byte = p[i]; i += 1
            for b in range(8):
                bits.append((byte >> b) & 1)
                if len(bits) == n_vars:
                    break
        return bits[:n_vars]

    # Data structures for dynamic evaluation
    true_count = [0]*m
    unsat = set()

    def recompute_counts(assign: List[int]):
        unsat.clear()
        for ci, clause in enumerate(cnf):
            t = 0
            for lit in clause:
                v = abs(lit); val = assign[v-1]
                if (lit > 0 and val == 1) or (lit < 0 and val == 0):
                    t += 1
            true_count[ci] = t
            if t == 0:
                unsat.add(ci)

    def delta_unsat_for_flip(assign: List[int], v_idx0: int) -> int:
        # v_idx0 is 0-based variable index
        v = v_idx0 + 1
        was1 = assign[v_idx0] == 1
        delta = 0
        # Positive literal clauses
        for ci in pos_idx[v]:
            t = true_count[ci]
            if was1:
                # +v goes from true to false
                if t == 1: delta += 1  # becomes unsat
            else:
                # +v goes from false to true
                if t == 0: delta -= 1  # becomes sat
        # Negative literal clauses
        for ci in neg_idx[v]:
            t = true_count[ci]
            if was1:
                # -v goes from false to true
                if t == 0: delta -= 1
            else:
                # -v goes from true to false
                if t == 1: delta += 1
        return delta

    def apply_flip(assign: List[int], v_idx0: int):
        v = v_idx0 + 1
        was1 = assign[v_idx0] == 1
        # Update counts for positive literal clauses
        if was1:
            for ci in pos_idx[v]:
                t = true_count[ci]
                if t == 1: unsat.add(ci)
                true_count[ci] = t - 1
        else:
            for ci in pos_idx[v]:
                t = true_count[ci]
                if t == 0: unsat.discard(ci)
                true_count[ci] = t + 1
        # Update counts for negative literal clauses
        if was1:
            for ci in neg_idx[v]:
                t = true_count[ci]
                if t == 0: unsat.discard(ci)
                true_count[ci] = t + 1
        else:
            for ci in neg_idx[v]:
                t = true_count[ci]
                if t == 1: unsat.add(ci)
                true_count[ci] = t - 1
        assign[v_idx0] ^= 1

    def pick_var_from_clause(assign: List[int], clause_idx: int, noise: float) -> int:
        clause = cnf[clause_idx]
        # With probability noise, pick a random variable from clause (deterministic RNG)
        if rng.rand() < noise:
            lit = clause[rng.randint(0, len(clause)-1)]
            return abs(lit) - 1
        # Else pick var minimizing resulting unsat clauses; tie-break by smallest var index
        best_v = None
        best_delta = None
        for lit in clause:
            v0 = abs(lit) - 1
            du = delta_unsat_for_flip(assign, v0)
            if best_delta is None or du < best_delta or (du == best_delta and v0 < best_v):
                best_delta = du; best_v = v0
        return best_v

    start_time = time.perf_counter()
    deadline = start_time + time_budget_ms/1000.0
    noise = params.get('noise', 0.5)
    max_steps_per_restart = params.get('max_steps', 20000)
    max_restarts = params.get('max_restarts', 20)

    # Restart loop
    base_seed = seed
    for r in range(max_restarts):
        if time.perf_counter() >= deadline:
            break
        # Derive a new deterministic seed per restart
        restart_seed = int.from_bytes(hashlib.sha256((base_seed + r).to_bytes(8,'big')).digest()[:4], 'big')
        rng = DRNG(restart_seed or 1)
        assign = init_assignment_from_seed(restart_seed or 1)
        recompute_counts(assign)
        if not unsat:
            return assign
        steps = 0
        while unsat and steps < max_steps_per_restart and time.perf_counter() < deadline:
            # Pick a deterministic unsatisfied clause: choose by hashing steps
            # But keep it simple: take an element by deterministic index
            idx = rng.randint(0, len(unsat)-1)
            # To index into a set deterministically, sort a small sample; for efficiency, convert once per step
            # Since clauses are small, this overhead is acceptable
            if len(unsat) <= 16:
                unsat_list = sorted(unsat)
                cidx = unsat_list[idx % len(unsat_list)]
            else:
                # Avoid full sort: pick k items deterministically and then min
                k = 8
                choices = []
                it = iter(unsat)
                # Sample k items by stepping through the iterator deterministically
                for _ in range(k):
                    try:
                        choices.append(next(it))
                    except StopIteration:
                        break
                cidx = choices[idx % len(choices)] if choices else next(iter(unsat))
            v0 = pick_var_from_clause(assign, cidx, noise)
            apply_flip(assign, v0)
            steps += 1
            # Early check every few steps
            if not unsat:
                return assign
        # Next restart
    return None

def local_polish(cnf: List[List[int]], assignment: List[int], max_flips: int = 200) -> Optional[List[int]]:
    a = assignment[:]
    def clause_satisfied(clause, a):
        for lit in clause:
            v = abs(lit)
            val = a[v-1]
            if (lit > 0 and val == 1) or (lit < 0 and val == 0):
                return True
        return False
    for _ in range(max_flips):
        if verify_cnf(cnf, a):
            return a
        # pick an unsatisfied clause and flip the variable that helps most
        unsat = [cl for cl in cnf if not clause_satisfied(cl, a)]
        clause = random.choice(unsat)
        best_v = None; best_score = None
        for lit in clause:
            v = abs(lit) - 1
            a[v] ^= 1
            score = 0
            for cl2 in cnf:
                if not clause_satisfied(cl2, a):
                    score += 1
            a[v] ^= 1
            if best_score is None or score < best_score:
                best_score = score; best_v = v
        a[best_v] ^= 1
    return a if verify_cnf(cnf, a) else None

# ----------------------------
# Benchmark harness
# ----------------------------

def fit_loglog_slope(ns: List[int], ts: List[float]) -> float:
    # Fit slope k in log(t) = k*log(n) + b via least squares
    xs = [math.log(max(1, n)) for n in ns]
    ys = [math.log(max(1e-9, t)) for t in ts]
    n = len(xs)
    xbar = sum(xs)/n; ybar = sum(ys)/n
    num = sum((x - xbar)*(y - ybar) for x,y in zip(xs, ys))
    den = sum((x - xbar)**2 for x in xs) or 1e-9
    return num/den

def run_benchmark():
    set_seed(42)
    ns = [50, 100, 150, 200, 300, 400]
    trials_per_n = 10
    clause_ratio = 4.2
    time_budget_ms = 200  # per instance for consciousness_solve
    results = []
    for n in ns:
        m = int(round(clause_ratio * n))
        successes = {"conscious": 0, "greedy": 0, "random": 0}
        times = {"conscious": [], "greedy": [], "random": []}
        for t in range(trials_per_n):
            seed = 100000*n + t
            cnf, planted = generate_planted_3sat(n, m, seed)
            # consciousness
            t0 = time.perf_counter()
            sol = consciousness_solve(cnf, n, time_budget_ms, params={"max_flips": 300})
            t1 = time.perf_counter()
            times["conscious"].append(t1 - t0)
            if sol is not None and verify_cnf(cnf, sol):
                successes["conscious"] += 1
            # greedy baseline
            t0 = time.perf_counter()
            gsol = greedy_local_search(cnf, n_vars=n, max_iters=2000)
            t1 = time.perf_counter()
            times["greedy"].append(t1 - t0)
            if gsol is not None and verify_cnf(cnf, gsol):
                successes["greedy"] += 1
            # random baseline
            t0 = time.perf_counter()
            rsol = random_assignment_solver(n, cnf, budget_ms=50)
            t1 = time.perf_counter()
            times["random"].append(t1 - t0)
            if rsol is not None and verify_cnf(cnf, rsol):
                successes["random"] += 1
        # summarize
        def med(lst): 
            s = sorted(lst); 
            return s[len(s)//2] if s else float('nan')
        results.append({
            "n": n,
            "m": m,
            "succ_conscious": successes["conscious"],
            "succ_greedy": successes["greedy"],
            "succ_random": successes["random"],
            "med_t_conscious": med(times["conscious"]),
            "med_t_greedy": med(times["greedy"]),
            "med_t_random": med(times["random"]),
        })
    # print table
    print("\nRESULTS (trials per n = %d, clause/var = %.2f)" % (trials_per_n, clause_ratio))
    print("n   m    |  cons_succ  med_t(s)   |  greedy_succ  med_t(s)   |  random_succ  med_t(s)")
    for row in results:
        print(f"{row['n']:<3} {row['m']:<4} | "
              f"{row['succ_conscious']:<11} {row['med_t_conscious']:.4f}  | "
              f"{row['succ_greedy']:<12} {row['med_t_greedy']:.4f}  | "
              f"{row['succ_random']:<12} {row['med_t_random']:.4f}")
    # scaling slope for successful runs
    cons_times = [r["med_t_conscious"] for r in results]
    slope = fit_loglog_slope(ns, cons_times)
    print(f"\nEstimated scaling exponent for consciousness_solve (median times): k ≈ {slope:.2f}")
    # acceptance checks
    pass_rate = all(r["succ_conscious"] >= int(0.9*trials_per_n) for r in results)
    pass_scale = slope <= 3.0
    print("\nACCEPTANCE CRITERIA:")
    print(f"- Success rate ≥ 90% at each n: {'PASS' if pass_rate else 'FAIL'}")
    print(f"- Polynomial scaling with k ≤ 3: {'PASS' if pass_scale else 'FAIL'}")

if __name__ == "__main__":
    run_benchmark()
