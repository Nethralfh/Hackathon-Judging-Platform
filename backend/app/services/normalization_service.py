import math
from typing import List, Dict
from app.models.score import Score

def normalize_scores(scores: List[Score]) -> Dict[int, float]:
    """
    Returns a dictionary mapping score.id to normalized score.
    Methodology: Z-score normalization per judge, mapped to a standard scale.
    """
    # Group by judge
    judge_scores: Dict[int, List[Score]] = {}
    for s in scores:
        if s.judge_id not in judge_scores:
            judge_scores[s.judge_id] = []
        judge_scores[s.judge_id].append(s)
        
    normalized = {}
    GLOBAL_MEAN = 70.0
    GLOBAL_STD = 15.0

    for judge_id, js in judge_scores.items():
        if len(js) <= 1:
            # Cannot calculate stddev, fallback to raw or global mean
            for s in js:
                normalized[s.id] = s.score
            continue
            
        mean = sum(s.score for s in js) / len(js)
        variance = sum((s.score - mean) ** 2 for s in js) / (len(js) - 1)
        std_dev = math.sqrt(variance)
        
        for s in js:
            if std_dev == 0:
                normalized[s.id] = s.score
            else:
                z_score = (s.score - mean) / std_dev
                norm_score = GLOBAL_MEAN + (z_score * GLOBAL_STD)
                # clamp to reasonable bounds e.g., 0 to 100
                norm_score = max(0.0, min(100.0, norm_score))
                normalized[s.id] = norm_score
                
    return normalized

