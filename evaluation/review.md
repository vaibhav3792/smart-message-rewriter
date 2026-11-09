# Smart Message Rewriter — Evaluation Review

## 1. Evaluation Overview

**Model:** `openai/gpt-oss-120b`

**Dataset:** 30 test cases (`evaluation/dataset.json`)

**Versions evaluated:** baseline_v1 and baseline_v2

**Evaluation approach:** Automated checks and manual semantic review

The evaluation measures whether the rewriter preserves the original message's meaning while following the requested tone, length, and recipient preferences.

The dataset covers different communication scenarios, including factual details, dates, amounts, restrictions, commitments, uncertainty, technical information, and action status.

## 2. Evaluation Dimensions

| Dimension | What to evaluate |
|---|---|
| Meaning preservation | Facts, dates, amounts, negations, conditions, commitments, and action status |
| Unsupported additions | Details introduced without support from the original message |
| Tone adherence | Whether the output matches the requested tone |
| Length adherence | Whether the output follows the requested length |
| Recipient suitability | Whether the language is appropriate for the intended recipient |
| Fluency | Whether the output sounds natural and clear |

Meaning preservation is a critical requirement. An output that changes an important fact, restriction, or commitment fails this dimension regardless of its other qualities.

## 3. Generation Results

Both versions generated successfully for all 30 test cases.

| Metric | V1 | V2 |
|---|---:|---:|
| Total cases | 30 | 30 |
| Successful generations | 30 | 30 |
| Generation failures | 0 | 0 |

V2 produced different outputs for 23 of the 30 cases compared with V1.

This indicates that the prompt refinement affected a substantial portion of the dataset, although output differences alone do not establish quality improvements.

## 4. Automated Check Results

The automated checks were run against V2.

| Metric | Result |
|---|---:|
| Cases evaluated | 30 |
| Cases flagged | 0 |
| Cases not flagged | 30 |

Automated checks did not identify any violations covered by their implemented rules.

Passing these checks does not establish semantic equivalence. Automated checks cover specific detectable conditions and cannot reliably identify every unsupported addition or change in meaning.

## 5. Manual Review Results

### V2 semantic review

| Cases | Passed | Failed |
|---|---:|---:|
| eval_001–eval_010 | 9 | 1 |
| eval_011–eval_020 | 10 | 0 |
| eval_021–eval_030 | 10 | 0 |
| **Total** | **29** | **1** |

**Manual semantic pass rate: 96.7% (29/30)**

### Important findings

| Case | V1 finding | V2 finding |
|---|---|---|
| eval_005 | Introduced `$` as a currency symbol without support from the original message | Stopped introducing the unsupported currency symbol |
| eval_006 | Action-status preservation issue identified during review | Changed an ongoing action into a completed action |
| eval_017 | Appreciation for the interviewer's time was weakened | Preserved the acknowledgment more effectively |

### eval_006 — Identified semantic failure

**Original:**

> I finished the report. sending it now. let me know if anything needs changes

**V2 output:**

> The report is finished and has been sent. Please let me know if any changes are needed.

The original message communicates that the report is being sent. The rewrite states that it has already been sent.

This changes the action status from ongoing to completed.

The failure is significant because the output sounds natural and professional while changing the underlying meaning.

## 6. Application-Level Safety Safeguard

To address the action-status issue, a deterministic application-level safeguard was implemented in `app/safety.py`.

The safeguard:

- Checks for selected ongoing-to-completed verb transformations.
- Detects transformations such as sending to sent, submitting to submitted, and preparing to prepared.
- Raises `RewriteSafetyError` when a likely action-status change is detected.
- Is integrated into `app/rewriter.py`.
- Returns HTTP 422 through the FastAPI endpoint when a flagged rewrite is rejected.

### Testing

The safeguard has dedicated tests covering:

- Detection of ongoing-to-completed transformations.
- Acceptance of preserved ongoing actions.
- Acceptance of future actions.
- Detection of multiple action-status changes.
- Rejection of unsafe rewrites.
- API-level HTTP 422 handling.

### Limitations

This safeguard is a heuristic, not a semantic verification system.

- It checks a finite list of predefined verbs.
- It cannot detect every possible change in tense, aspect, or action status.
- Different grammatical contexts can produce false positives.
- Equivalent transformations using unlisted verbs may go undetected.
- It does not establish factual correctness or guarantee preservation of the original meaning.

A flagged rewrite is rejected rather than automatically corrected. The safeguard provides an additional layer of protection without introducing another LLM call or a complex verification pipeline.

## 7. Known Evaluation Limitations

1. **Fixed dataset:** The same 30 cases were used during prompt refinement. Consequently, these results represent internal regression evaluation, not an unbiased holdout benchmark.
2. **Limited recipient coverage:** The application supports professor, recruiter, senior, colleague, and friend. Some dataset recipients were mapped to the closest supported category.
3. **Length evaluation:** Length adherence has not been systematically scored across all cases.
4. **Manual assessment:** The semantic review was qualitative rather than a fully scored evaluation across every dimension.
5. **Heuristic safeguards:** Automated safeguards only cover explicitly implemented rules and cannot guarantee semantic equivalence.

The 96.7% manual pass rate should therefore be interpreted only in the context of this particular dataset and review process. It is not a general performance guarantee.

## 8. Future Evaluation Procedure

For future prompt or application changes:

1. Preserve the existing dataset as a regression test set.
2. Maintain a separate holdout dataset that is not used during prompt refinement.
3. Generate outputs using the same model and configuration when comparing versions.
4. Save each evaluation run under a new version.
5. Run automated checks for supported constraints.
6. Review meaning preservation and unsupported additions first.
7. Assess tone, length, recipient suitability, and fluency.
8. Record regressions alongside improvements.
9. Add newly discovered failure cases to the regression dataset.

A prompt or application revision should not be considered better merely because its outputs sound more polished. It must preserve the original meaning while improving the requested writing characteristics.

## 9. Final Conclusion

The evaluation demonstrated successful generation across all 30 cases in both V1 and V2.

V2 showed improvements in handling unsupported currency symbols and preserving important acknowledgments. Manual review identified one significant semantic failure involving an ongoing action being rewritten as completed.

The application-level safeguard adds a deterministic check for selected action-status transformations. Dedicated unit and API tests verify its behavior, including HTTP 422 rejection.

The project now has an evaluation dataset, versioned outputs, automated checks, manual review findings, and an application-level safeguard.

The results are useful for internal quality assessment and regression testing, with the limitation that the evaluation dataset was also used during prompt refinement.