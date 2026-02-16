import random

def get_environment_factor(hour, sleep_start, sleep_end):
    # Handle overnight sleep (e.g., 23 to 07)
    if sleep_start < sleep_end:
        if sleep_start <= hour < sleep_end:
            return None
    else:
        if hour >= sleep_start or hour < sleep_end:
            return None

    # Distraction logic
    if hour in [10, 14]: return 1.1   # Low distraction peak
    if hour in [11, 16]: return 0.8   # High distraction dip
    return 1.0

def calculate_attention(hour, capacity, sleep_start, sleep_end):
    env = get_environment_factor(hour, sleep_start, sleep_end)
    if env is None:
        return None
    
    base = 70
    noise = random.uniform(-5, 5)
    score = (capacity * base * env) + noise
    return max(0, min(100, round(score, 2)))