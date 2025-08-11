# uqcb_demo_artifacts.py
# Demonstrate storing algorithms, color patterns, and charts into the UQCB chain

from uqcb_chain import load_chain, save_chain, verify_chain, append_block, latest_hash, DEFAULT_CHAIN_PATH
from uqcb_artifacts import encode_algorithm, encode_color_pattern, encode_chart, decode_color_pattern, infer_algorithm_from_colors, series_from_color_grid
import argparse, random


def demo(chain_path: str, difficulty_bits: int):
    chain = load_chain(chain_path)
    ok, err = verify_chain(chain, difficulty_bits)
    if not ok:
        print(f"Chain invalid: {err}. Create genesis first (uqcb_genesis.py)")
        return

    # 1) Store an algorithm abstraction (pseudocode)
    algo = encode_algorithm(
        name="Fraymus-φ-Search",
        description="Golden-ratio guided local search with epochal resets and entanglement bias",
        pseudocode=[
            "seed <- sha256(head_hash | problem)",
            "repeat until time_budget:",
            "  propose step via φ-ratio strides",
            "  accept if reduces unsat or meets protective heuristic",
            "  periodic epoch reset if stagnation",
        ],
        params={"phi": 1.61803398875, "entanglement_bias": 0.21},
    )
    chain = append_block(chain, {"artifact": algo}, difficulty_bits)
    save_chain(chain, chain_path)
    print("Appended algorithm artifact. Head:", latest_hash(chain))

    # 2) Store a color grid pattern (e.g., encoding a heuristic landscape)
    random.seed(7)
    h, w = 12, 24
    grid = [[(random.randrange(256), random.randrange(256), random.randrange(256)) for _ in range(w)] for __ in range(h)]
    color = encode_color_pattern("HeuristicLandscape-v1", grid, palette_note="bands encode difficulty valleys")
    chain = append_block(chain, {"artifact": color}, difficulty_bits)
    save_chain(chain, chain_path)
    print("Appended color pattern artifact. Head:", latest_hash(chain))

    # 3) Store a chart (series) derived from the color grid to enable reverse engineering
    series = series_from_color_grid(grid)
    chart = encode_chart("BrightnessWaveform", series, note="column-averaged luminance")
    chain = append_block(chain, {"artifact": chart}, difficulty_bits)
    save_chain(chain, chain_path)
    print("Appended chart artifact. Head:", latest_hash(chain))

    # 4) Demonstrate reverse engineering hint
    recon = infer_algorithm_from_colors(grid)
    print("Reverse-engineering hint from colors:", recon)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", default=DEFAULT_CHAIN_PATH)
    ap.add_argument("-d", "--difficulty", type=int, default=12)
    args = ap.parse_args()
    demo(args.path, args.difficulty)
