import json
from orchestrator.metrics import compute_global_metrics
from orchestrator.dp_planner import get_cache_stats

def main():
    report = {
        "metrics": compute_global_metrics(),
        "dp_cache": get_cache_stats(),
    }

    with open("logs/final_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("Final report generated")

if __name__ == "__main__":
    main()