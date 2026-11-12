import argparse, json
from pathlib import Path
from .kuhn_cfr import KuhnCFR

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=100_000)
    parser.add_argument("--output", default="data/kuhn_strategy.json")
    args = parser.parse_args()
    solver = KuhnCFR()
    strategy = solver.train(args.iterations)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"game": "Kuhn Poker", "iterations": args.iterations, "strategy": strategy}, indent=2))
    print(f"Wrote {len(strategy)} information sets to {output}")

if __name__ == "__main__":
    main()
