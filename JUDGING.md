# Judging Engine & Normalization

## Assignment Strategy
The assignment strategy allows organizers to explicitly assign Judges to Projects via `JudgeAssignment`. This ensures projects are reviewed by judges with relevant expertise, rather than relying on a blind random assignment.

## Scoring Mathematics
Scores are evaluated on a per-criterion basis. Each criterion has a predefined weight. The raw weighted score for a project is the sum of `(score * criterion_weight)` across all evaluations.

## Cross-Judge Normalization Method
Hackathons frequently suffer from judge calibration issues (e.g., one judge gives all 10s, another gives 5s). To fix this, we implemented Z-score normalization.

1. **Calculate Judge Baseline**: We group all scores by judge. For each judge, we calculate their mean score and standard deviation.
2. **Z-Score Calculation**: Each individual score is converted to a Z-score `(score - mean) / std_dev`, which represents how many standard deviations the score is above or below that judge's personal average.
3. **Standard Scale Mapping**: The Z-score is then mapped to a global standard scale (Global Mean = 70.0, Global StdDev = 15.0) and clamped between 0 and 100.
4. **Final Weighted Output**: The normalized scores are multiplied by their respective criterion weights and aggregated to produce the final `normalized_score`.

This effectively mitigates "harsh" vs "generous" judge biases, ensuring fairness.

## Defense of Method
Z-score standardization is mathematically robust and widely accepted in statistical normalization. It is superior to simple averaging because it preserves the relative ranking of projects *within* a judge's cohort while aligning the absolute magnitude of scores *across* judges.
