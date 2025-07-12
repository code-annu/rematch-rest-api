from math import fabs

from app.model.qna_model import QnaResponse


# For string-based similarity, exact match = 1, else 0
def _exact_str_sim(a, b):
    return 1.0 if a == b else 0.0


# For numeric features like pain_rate or length: convert absolute diff into similarity [0–1]
def _numeric_sim(a, b, max_diff):
    return max(0.0, 1 - fabs(a - b) / max_diff)


def measure_qna_similarity(target_qna: QnaResponse, buddy_qna: QnaResponse, weights=None) -> float:
    if weights is None:
        weights = {
            'breakup_reason': 4.0,
            'pain_rate': 1.0,
            'coping_mechanism': 1.0,
            'relationship_length': 1.0,
            'emotional_quotient': 1.0
        }

    # define max_diff values for numeric normalizations
    max_diff = {
        'pain_rate': 9,  # since scale is 1–10
        'relationship_length': 119  # 1–120 months
    }
    score = 0.0
    total_w = 0.0

    # 1. breakup_reason (categorical, must match)
    sim = _exact_str_sim(target_qna.breakup_reason, buddy_qna.breakup_reason)
    w = weights['breakup_reason']
    score += w * sim
    total_w += w

    # 2. pain_rate (numeric)
    sim = _numeric_sim(target_qna.pain_rate, buddy_qna.pain_rate, max_diff['pain_rate'])
    w = weights['pain_rate']
    score += w * sim
    total_w += w

    # 3. coping_mechanism (categorical)
    sim = _exact_str_sim(target_qna.coping_mechanism, buddy_qna.coping_mechanism)
    w = weights['coping_mechanism']
    score += w * sim
    total_w += w

    # 4. relationship_length
    sim = _numeric_sim(target_qna.relationship_length, buddy_qna.relationship_length, max_diff['relationship_length'])
    w = weights['relationship_length']
    score += w * sim
    total_w += w

    # 5. emotional_quotient (categorical)
    sim = _exact_str_sim(target_qna.emotional_quotient, buddy_qna.emotional_quotient)
    w = weights['emotional_quotient']
    score += w * sim
    total_w += w

    normalized = score / total_w
    return normalized
