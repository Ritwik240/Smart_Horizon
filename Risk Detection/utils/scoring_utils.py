# utils/scoring_utils.py

from typing import List, Tuple

# Mapping of qualitative risk levels to numeric scores
RISK_SCORE_MAP = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3
}

def calculate_risk_score(risks: List[Tuple[str, str]]) -> int:
    """
    Calculates a numeric risk score based on a list of risks.
    
    Args:
        risks: List of tuples, each containing (risk_name, risk_level)
    
    Returns:
        Total numeric risk score
    """
    return sum(RISK_SCORE_MAP.get(level.upper(), 0) for _, level in risks)

def determine_status(risks: List[Tuple[str, str]]) -> str:
    """
    Determines overall status based on risk score.
    
    Returns:
        "SAFE" if no risks, "ALERT" if any risks present
    """
    return "SAFE" if not risks else "ALERT"