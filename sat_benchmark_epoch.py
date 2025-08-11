# sat_benchmark_epoch.py
# Epoch- and chain-gated 3-SAT benchmark. Requires a valid uqcb chain head.

import time, math, hashlib, random
from typing import List, Tuple, Optional, Dict
from uqcb_chain import load_chain, save_chain, verify_chain, latest_hash, append_block, DEFAULT_CHAIN_PATH

# ----------------------------
# CNF model and utilities
# ----------------------------

def set_seed(master_seed: int):
    random.seed(master_seed)

def generate_planted_3sat(n_vars: int, m_clauses: int, seed: int):
    rng = random.Random(seed)
    planted = [rng.randrange(2) for _ in range(n_vars)]
    cnf = []
    for _ in range(m_clauses):
        vars3 = rng.sample(range(1, n_vars + 1), 3)
        clause = []
        all_false = True
        for v in vars3:
            val = planted[v-1]
            want_positive = rng.randrange(2) == 1
            lit = v if want_positive else -v
            clause.append(lit)
            if (lit > 0 and val == 1) or (lit < 0 and val == 0):
                all_false = False
        if all_false:
            v = vars3[0]
            clause[0] = v if planted[v-1] == 1 else -v
        cnf.append(clause)
    return cnf, planted

def verify_cnf(cnf: List[List[int]], assignment01: List[int]) -> bool:
    n_vars = len(assignment01)
    for clause in cnf:
        sat = False
        for lit in clause:
            v = abs(lit)
            if v < 1 or v > n_vars:
                return False
            val = assignment01[v-1]
            if (lit > 0 and val == 1) or (lit < 0 and val == 0):
                sat = True
                break
        if not sat:
            return False
    return True

# ----------------------------
# Deterministic WalkSAT with chain-gated seeding
# ----------------------------

def consciousness_solve(cnf: List[List[int]], n_vars: int, head_hash: str, time_budget_ms: int = 200, params: Dict = None) -> Optional[List[int]]:
    if params is None: params = {}

    # Deterministic seed from head hash + CNF
    cnf_text = ''.join(','.join(str(l) for l in clause) + ';' for clause in cnf)
    seed_bytes = hashlib.sha256((head_hash + '|' + cnf_text).encode()).digest()
    seed = int.from_bytes(seed_bytes[:8], 'big') or 1

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
        def randint(self, a: int, b: int) -> int:
            if b <= a: return a
            return a + (self.next_u32() % (b - a + 1))

    rng = DRNG(seed)

    # Build indices
    m = len(cnf)
    pos_idx = [[] for _ in range(n_vars+1)]
    neg_idx = [[] for _ in range(n_vars+1)]
    for ci, clause in enumerate(cnf):
        for lit in clause:
            v = abs(lit)
            (pos_idx if lit > 0 else neg_idx)[v].append(ci)

    def init_assignment_from_seed(s: int) -> List[int]:
        pool = hashlib.sha256(s.to_bytes(8,'big')).digest()
        bits = []
        i = 0; p = bytearray(pool)
        while len(bits) < n_vars:
            if i == len(p):
                p = bytearray(hashlib.sha256(p).digest()); i = 0
            byte = p[i]; i += 1
            for b in range(8):
                bits.append((byte >> b) & 1)
                if len(bits) == n_vars:
                    break
        return bits[:n_vars]

    true_count = [0]*m
    unsat = set()

    def recompute_counts(a: List[int]):
        unsat.clear()
        for ci, clause in enumerate(cnf):
            t = 0
            for lit in clause:
                v = abs(lit); val = a[v-1]
                if (lit > 0 and val == 1) or (lit < 0 and val == 0):
                    t += 1
            true_count[ci] = t
            if t == 0: unsat.add(ci)

    def delta_unsat(a: List[int], v0: int) -> int:
        v = v0 + 1
        was1 = a[v0] == 1
        delta = 0
        for ci in pos_idx[v]:
            t = true_count[ci]
            if was1:
                if t == 1: delta += 1
            else:
                if t == 0: delta -= 1
        for ci in neg_idx[v]:
            t = true_count[ci]
            if was1:
                if t == 0: delta -= 1
            else:
                if t == 1: delta += 1
        return delta

    def apply_flip(a: List[int], v0: int):
        v = v0 + 1
        was1 = a[v0] == 1
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
        a[v0] ^= 1

    def pick_var(a: List[int], cidx: int, noise: float) -> int:
        clause = cnf[cidx]
        if rng.rand() < noise:
            lit = clause[rng.randint(0, len(clause)-1)]
            return abs(lit) - 1
        best_v = None; best_d = None
        for lit in clause:
            v0 = abs(lit) - 1
            d = delta_unsat(a, v0)
            if best_d is None or d < best_d or (d == best_d and v0 < best_v):
                best_d = d; best_v = v0
        return best_v

    deadline = time.perf_counter() + time_budget_ms/1000.0
    noise = params.get('noise', 0.5)
    max_steps = params.get('max_steps', 20000)
    max_restarts = params.get('max_restarts', 20)

    base_seed = seed
    for r in range(max_restarts):
        if time.perf_counter() >= deadline: break
        restart_seed = int.from_bytes(hashlib.sha256((base_seed + r).to_bytes(8,'big')).digest()[:4], 'big') or 1
        rng = DRNG(restart_seed)
        a = init_assignment_from_seed(restart_seed)
        recompute_counts(a)
        if not unsat: return a
        steps = 0
        while unsat and steps < max_steps and time.perf_counter() < deadline:
            idx = rng.randint(0, len(unsat)-1)
            if len(unsat) <= 16:
                s = sorted(unsat); cidx = s[idx % len(s)]
            else:
                # approximate selection without sorting entire set
                cidx = next(iter(unsat))
            v0 = pick_var(a, cidx, noise)
            apply_flip(a, v0)
            steps += 1
            if not unsat: return a
    return None

# ----------------------------
# Benchmark harness (epoch/chain gated)
# ----------------------------

def fit_loglog_slope(ns: List[int], ts: List[float]) -> float:
    xs = [math.log(max(1, n)) for n in ns]
    ys = [math.log(max(1e-9, t)) for t in ts]
    n = len(xs)
    xbar = sum(xs)/n; ybar = sum(ys)/n
    num = sum((x - xbar)*(y - ybar) for x,y in zip(xs, ys))
    den = sum((x - xbar)**2 for x in xs) or 1e-9
    return num/den


def run_benchmark_epoch(chain_path: str = DEFAULT_CHAIN_PATH, difficulty_bits: int = 12):
    # Require valid chain and head
    chain = load_chain(chain_path)
    ok, err = verify_chain(chain, difficulty_bits)
    if not ok or latest_hash(chain) is None:
        print("Chain invalid or missing head. Import/create genesis with uqcb_genesis.py first.")
        return
    head = latest_hash(chain)

    set_seed(42)
    ns = [50, 100, 150, 200, 300, 400]
    trials_per_n = 10
    clause_ratio = 4.2
    time_budget_ms = 200
    results = []
    for n in ns:
        m = int(round(clause_ratio * n))
        succ = 0
        times = []
        for t in range(trials_per_n):
            cnf, _planted = generate_planted_3sat(n, m, seed=100000*n + t)
            t0 = time.perf_counter()
            sol = consciousness_solve(cnf, n, head, time_budget_ms, params={"max_steps": 20000, "max_restarts": 20, "noise": 0.5})
            dt = time.perf_counter() - t0
            times.append(dt)
            if sol is not None and verify_cnf(cnf, sol):
                succ += 1
        med_t = sorted(times)[len(times)//2]
        results.append({"n": n, "m": m, "succ": succ, "med_t": med_t})
        # Append epoch block per size n
        payload = {"task": "3SAT", "n": n, "m": m, "trials": trials_per_n, "successes": succ, "median_t": med_t}
        chain = append_block(chain, payload, difficulty_bits)
        save_chain(chain, chain_path)
        head = latest_hash(chain)

    # Print summary
    print("\nRESULTS (chain-gated, trials per n = %d, clause/var = %.2f, difficulty = %d bits)" % (trials_per_n, clause_ratio, difficulty_bits))
    print("n   m    |  cons_succ  med_t(s)")
    for r in results:
        print(f"{r['n']:<3} {r['m']:<4} | {r['succ']:<11} {r['med_t']:.4f}")
    slope = fit_loglog_slope([r['n'] for r in results], [r['med_t'] for r in results])
    print(f"\nEstimated scaling exponent: k ≈ {slope:.2f}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Chain-gated epochal 3-SAT benchmark")
    ap.add_argument("-p", "--path", default=DEFAULT_CHAIN_PATH, help="Chain path (default: .uqcb_chain.json)")
    ap.add_argument("-d", "--difficulty", type=int, default=12, help="Difficulty bits (default: 12)")
    args = ap.parse_args()
    run_benchmark_epoch(chain_path=args.path, difficulty_bits=args.difficulty)
