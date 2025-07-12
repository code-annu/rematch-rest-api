from math import fabs


# For string-based similarity, exact match = 1, else 0
def exact_str_sim(a, b):
    return 1.0 if a == b else 0.0


# For numeric features like pain_rate or length: convert absolute diff into similarity [0–1]
def numeric_sim(a, b, max_diff):
    return max(0.0, 1 - fabs(a - b) / max_diff)


def find_best_buddy(target, users, weights=None):
    """
    target: dict with keys breakup_reason, pain_rate, coping_mechanism,
            relationship_length, emotional_quotient
    users: list of dicts, each same structure with unique 'id'
    weights: dict of weights for each feature (defaults shown)
    """
    # default weights
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

    best = None
    best_score = -1

    for user in users:
        score = 0.0
        total_w = 0.0

        # 1. breakup_reason (categorical, must match)
        sim = exact_str_sim(target['breakup_reason'], user['breakup_reason'])
        w = weights['breakup_reason']
        score += w * sim
        total_w += w

        # 2. pain_rate (numeric)
        sim = numeric_sim(target['pain_rate'], user['pain_rate'], max_diff['pain_rate'])
        w = weights['pain_rate']
        score += w * sim
        total_w += w

        # 3. coping_mechanism (categorical)
        sim = exact_str_sim(target['coping_mechanism'], user['coping_mechanism'])
        w = weights['coping_mechanism']
        score += w * sim
        total_w += w

        # 4. relationship_length
        sim = numeric_sim(target['relationship_length'], user['relationship_length'],
                          max_diff['relationship_length'])
        w = weights['relationship_length']
        score += w * sim
        total_w += w

        # 5. emotional_quotient (categorical)
        sim = exact_str_sim(target['emotional_quotient'], user['emotional_quotient'])
        w = weights['emotional_quotient']
        score += w * sim
        total_w += w

        normalized = score / total_w

        if normalized > best_score:
            best_score = normalized
            best = user

    return best, best_score


# Example usage:
users = [
    {
        'id': 1,
        'breakup_reason': 'Cheating',
        'pain_rate': 8,
        'coping_mechanism': 'Therapy',
        'relationship_length': 24,
        'emotional_quotient': 'Sadness'
    },
    {
        'id': 2,
        'breakup_reason': 'Cheating',
        'pain_rate': 7,
        'coping_mechanism': 'Hobbies',
        'relationship_length': 18,
        'emotional_quotient': 'Sadness'
    },
    {
        'id': 3,
        'breakup_reason': 'Long Distance',
        'pain_rate': 7,
        'coping_mechanism': 'Exercise',
        'relationship_length': 63,
        'emotional_quotient': 'Fear/Anxiety'
    },
    {'id': 4, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 9, 'coping_mechanism': 'Therapy',
     'relationship_length': 36, 'emotional_quotient': 'Anger'},
    {'id': 5, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 5, 'coping_mechanism': 'Hobbies',
     'relationship_length': 12, 'emotional_quotient': 'Relief'},
    {'id': 6, 'breakup_reason': 'Long Distance', 'pain_rate': 6, 'coping_mechanism': 'Exercise',
     'relationship_length': 30, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 7, 'breakup_reason': 'Cheating', 'pain_rate': 10, 'coping_mechanism': 'Meditation',
     'relationship_length': 48, 'emotional_quotient': 'Anger'},
    {'id': 8, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 8, 'coping_mechanism': 'Work',
     'relationship_length': 60, 'emotional_quotient': 'Sadness'},
    {'id': 9, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 4, 'coping_mechanism': 'Meditation',
     'relationship_length': 6, 'emotional_quotient': 'Relief'},
    {'id': 10, 'breakup_reason': 'Long Distance', 'pain_rate': 7, 'coping_mechanism': 'Therapy',
     'relationship_length': 15, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 11, 'breakup_reason': 'Cheating', 'pain_rate': 9, 'coping_mechanism': 'Work', 'relationship_length': 20,
     'emotional_quotient': 'Anger'},
    {'id': 12, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 10, 'coping_mechanism': 'Therapy',
     'relationship_length': 72, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 13, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 3, 'coping_mechanism': 'Hobbies',
     'relationship_length': 9, 'emotional_quotient': 'Relief'},
    {'id': 14, 'breakup_reason': 'Long Distance', 'pain_rate': 5, 'coping_mechanism': 'Meditation',
     'relationship_length': 48, 'emotional_quotient': 'Sadness'},
    {'id': 15, 'breakup_reason': 'Cheating', 'pain_rate': 8, 'coping_mechanism': 'Exercise', 'relationship_length': 14,
     'emotional_quotient': 'Anger'},
    {'id': 16, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 9, 'coping_mechanism': 'Therapy',
     'relationship_length': 24, 'emotional_quotient': 'Sadness'},
    {'id': 17, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 6, 'coping_mechanism': 'Work',
     'relationship_length': 42, 'emotional_quotient': 'Relief'},
    {'id': 18, 'breakup_reason': 'Long Distance', 'pain_rate': 8, 'coping_mechanism': 'Hobbies',
     'relationship_length': 60, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 19, 'breakup_reason': 'Cheating', 'pain_rate': 7, 'coping_mechanism': 'Meditation', 'relationship_length': 8,
     'emotional_quotient': 'Anger'},
    {'id': 20, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 8, 'coping_mechanism': 'Therapy',
     'relationship_length': 96, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 21, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 4, 'coping_mechanism': 'Exercise',
     'relationship_length': 18, 'emotional_quotient': 'Sadness'},
    {'id': 22, 'breakup_reason': 'Cheating', 'pain_rate': 9, 'coping_mechanism': 'Work', 'relationship_length': 30,
     'emotional_quotient': 'Anger'},
    {'id': 23, 'breakup_reason': 'Long Distance', 'pain_rate': 6, 'coping_mechanism': 'Meditation',
     'relationship_length': 20, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 24, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 5, 'coping_mechanism': 'Hobbies',
     'relationship_length': 24, 'emotional_quotient': 'Relief'},
    {'id': 25, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 6, 'coping_mechanism': 'Therapy',
     'relationship_length': 30, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 26, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 10, 'coping_mechanism': 'Therapy',
     'relationship_length': 42, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 27, 'breakup_reason': 'Long Distance', 'pain_rate': 5, 'coping_mechanism': 'Hobbies',
     'relationship_length': 12, 'emotional_quotient': 'Sadness'},
    {'id': 28, 'breakup_reason': 'Cheating', 'pain_rate': 9, 'coping_mechanism': 'Work', 'relationship_length': 54,
     'emotional_quotient': 'Anger'},
    {'id': 29, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 4, 'coping_mechanism': 'Meditation',
     'relationship_length': 8, 'emotional_quotient': 'Relief'},
    {'id': 30, 'breakup_reason': 'Long Distance', 'pain_rate': 7, 'coping_mechanism': 'Exercise',
     'relationship_length': 36, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 31, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 8, 'coping_mechanism': 'Hobbies',
     'relationship_length': 18, 'emotional_quotient': 'Anger'},
    {'id': 32, 'breakup_reason': 'Cheating', 'pain_rate': 10, 'coping_mechanism': 'Therapy', 'relationship_length': 60,
     'emotional_quotient': 'Sadness'},
    {'id': 33, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 5, 'coping_mechanism': 'Work',
     'relationship_length': 24, 'emotional_quotient': 'Relief'},
    {'id': 34, 'breakup_reason': 'Long Distance', 'pain_rate': 6, 'coping_mechanism': 'Meditation',
     'relationship_length': 27, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 35, 'breakup_reason': 'Cheating', 'pain_rate': 9, 'coping_mechanism': 'Exercise', 'relationship_length': 15,
     'emotional_quotient': 'Anger'},
    {'id': 36, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 9, 'coping_mechanism': 'Therapy',
     'relationship_length': 48, 'emotional_quotient': 'Sadness'},
    {'id': 37, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 6, 'coping_mechanism': 'Hobbies',
     'relationship_length': 72, 'emotional_quotient': 'Relief'},
    {'id': 38, 'breakup_reason': 'Cheating', 'pain_rate': 8, 'coping_mechanism': 'Meditation',
     'relationship_length': 21, 'emotional_quotient': 'Anger'},
    {'id': 39, 'breakup_reason': 'Long Distance', 'pain_rate': 4, 'coping_mechanism': 'Work', 'relationship_length': 9,
     'emotional_quotient': 'Sadness'},
    {'id': 40, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 10, 'coping_mechanism': 'Therapy',
     'relationship_length': 84, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 41, 'breakup_reason': 'Compatibility Issues', 'pain_rate': 3, 'coping_mechanism': 'Meditation',
     'relationship_length': 6, 'emotional_quotient': 'Relief'},
    {'id': 42, 'breakup_reason': 'Cheating', 'pain_rate': 10, 'coping_mechanism': 'Work', 'relationship_length': 33,
     'emotional_quotient': 'Anger'},
    {'id': 43, 'breakup_reason': 'Long Distance', 'pain_rate': 7, 'coping_mechanism': 'Therapy',
     'relationship_length': 44, 'emotional_quotient': 'Fear/Anxiety'},
    {'id': 44, 'breakup_reason': 'Emotional abuse or toxicity', 'pain_rate': 8, 'coping_mechanism': 'Hobbies',
     'relationship_length': 54, 'emotional_quotient': 'Sadness'},
    # more users...
]

target = {
    'breakup_reason': 'Compatibility Issues',
    'pain_rate': 1,
    'coping_mechanism': 'Others',
    'relationship_length': 62,
    'emotional_quotient': 'Fear/Anxiety'
}

buddy, score = find_best_buddy(target, users, weights={
    'breakup_reason': 5.0,  # give extra weight to matching reason
    'pain_rate': 1.0,
    'coping_mechanism': 1.0,
    'relationship_length': 0.5,
    'emotional_quotient': 1.0
})
print(f"Best buddy: {buddy['id']} with similarity score {score:.2f}")
