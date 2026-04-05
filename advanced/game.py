import random


def pick_secret(low: int, high: int) -> int:
    """Return a random integer in [low, high] inclusive."""
    return random.randint(low, high)


def check_guess(secret: int, guess: int) -> str:
    """Compare guess to secret. Returns 'low', 'high', or 'correct'."""
    if guess < secret:
        return "low"
    elif guess > secret:
        return "high"
    else:
        return "correct"
