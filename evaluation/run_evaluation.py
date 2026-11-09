
import json
from datetime import datetime, timezone
from pathlib import Path

from app.rewriter import rewrite_message

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "evaluation" / "dataset.json"
RESULTS_DIR = PROJECT_ROOT / "evaluation" / "results"
RUN_NAME = "baseline_v2"
RESULTS_PATH = RESULTS_DIR / f"{RUN_NAME}.json"

from app.llm import MODEL_NAME


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def run_evaluation():
    dataset = load_dataset()
    print(f"Loaded {len(dataset)} evaluation cases.\n")

    results = []

    for case in dataset:
        print(f"Running {case['id']}...")

        try:
            output = rewrite_message(
                message=case["message"],
                tone=case["tone"],
                length=case["length"],
                recipient=case["recipient"],
            )

            results.append({
                **case,
                "status": "success",
                "output": output,
                "error": None,
            })

        except Exception as error:
            results.append({
                **case,
                "status": "failed",
                "output": None,
                "error": str(error),
            })

            print(f"  FAILED: {error}")

    successful = sum(r["status"] == "success" for r in results)
    failed = len(results) - successful

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    evaluation_data = {
        "run_name": RUN_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_NAME,
        "total_cases": len(results),
        "successful": successful,
        "failed": failed,
        "results": results,
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as file:
        json.dump(evaluation_data, file, indent=4, ensure_ascii=False)

    print("\n" + "=" * 45)
    print("EVALUATION SUMMARY")
    print("=" * 45)
    print(f"Total cases: {len(results)}")
    print(f"Successful:  {successful}")
    print(f"Failed:      {failed}")
    print(f"\nResults saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    run_evaluation()
