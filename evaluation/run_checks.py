
import json
from pathlib import Path

from evaluation.checks import (
    check_output_validity,
    check_number_preservation,
    check_date_preservation,
    check_time_preservation,
    check_technical_identifiers,
    check_length_adherence,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "evaluation" / "results"

RUN_NAME = "v2"
INPUT_PATH = RESULTS_DIR / f"baseline_{RUN_NAME}.json"
OUTPUT_PATH = RESULTS_DIR / f"automated_{RUN_NAME}.json"


def evaluate_case(case):
    original = case["message"]
    output = case["output"]

    validity = check_output_validity(output)

    # Other checks require a valid string output.
    if not validity["passed"]:
        return {
            "output_validity": validity,
            "number_preservation": None,
            "date_preservation": None,
            "time_preservation": None,
            "technical_identifier_preservation": None,
            "length_adherence": None,
            "review_required": True,
        }

    checks = {
        "output_validity": validity,
        "number_preservation": check_number_preservation(
            original, output
        ),
        "date_preservation": check_date_preservation(
            original, output
        ),
        "time_preservation": check_time_preservation(
            original, output
        ),
        "technical_identifier_preservation": check_technical_identifiers(
            original, output
        ),
        "length_adherence": check_length_adherence(
            original, output, case["length"]
        ),
    }

    # A failed deterministic check triggers human review.
    review_required = any(
        not result["passed"]
        for result in checks.values()
    )

    return {
        **checks,
        "review_required": review_required,
    }


def run_checks():
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        baseline = json.load(file)

    results = []

    for case in baseline["results"]:
        if case["status"] != "success":
            automated_checks = {
                "review_required": True,
                "details": "Generation failed; manual review required.",
            }
        else:
            automated_checks = evaluate_case(case)

        results.append({
            **case,
            "automated_checks": automated_checks,
        })

    review_count = sum(
        result["automated_checks"]["review_required"]
        for result in results
    )

    evaluation_data = {
        "run_name": f"automated_{RUN_NAME}",
        "source_run": baseline["run_name"],
        "source_timestamp": baseline["timestamp"],
        "model": baseline["model"],
        "total_cases": len(results),
        "flagged_for_review": review_count,
        "results": results,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            evaluation_data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("=" * 45)
    print("AUTOMATED EVALUATION SUMMARY")
    print("=" * 45)
    print(f"Total cases: {len(results)}")
    print(f"Flagged for review: {review_count}")
    print(f"Not flagged: {len(results) - review_count}")
    print(f"\nResults saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    run_checks()
