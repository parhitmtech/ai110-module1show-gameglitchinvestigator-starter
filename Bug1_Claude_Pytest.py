"""
test_bug1_hints.py
------------------
Pytest tests specifically targeting Bug 1:
    The "Too High" and "Too Low" hint messages were swapped in check_guess().

Bug summary:
    When guess > secret  →  game incorrectly said "Go HIGHER" (should be "Go LOWER")
    When guess < secret  →  game incorrectly said "Go LOWER"  (should be "Go HIGHER")

These tests confirm the FIXED behavior is correct.
"""

import pytest
from logic_utils import check_guess


# ---------------------------------------------------------------------------
# Core direction tests
# ---------------------------------------------------------------------------

def test_guess_too_high_returns_go_lower():
    """
    If the player guesses ABOVE the secret, the hint must say Go LOWER.
    Bug 1 caused this to return 'Go HIGHER' instead.
    """
    outcome, message = check_guess(guess=80, secret=42)
    assert outcome == "Too High"
    assert "LOWER" in message, (
        f"Expected hint to contain 'LOWER' when guess > secret, got: '{message}'"
    )


def test_guess_too_low_returns_go_higher():
    """
    If the player guesses BELOW the secret, the hint must say Go HIGHER.
    Bug 1 caused this to return 'Go LOWER' instead.
    """
    outcome, message = check_guess(guess=10, secret=42)
    assert outcome == "Too Low"
    assert "HIGHER" in message, (
        f"Expected hint to contain 'HIGHER' when guess < secret, got: '{message}'"
    )


def test_correct_guess_returns_win():
    """Exact match should always return Win regardless of Bug 1."""
    outcome, message = check_guess(guess=42, secret=42)
    assert outcome == "Win"
    assert "Correct" in message or "🎉" in message


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_guess_one_above_secret():
    """Off-by-one above: guess is just 1 more than secret."""
    outcome, message = check_guess(guess=43, secret=42)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_one_below_secret():
    """Off-by-one below: guess is just 1 less than secret."""
    outcome, message = check_guess(guess=41, secret=42)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_guess_at_range_minimum():
    """Guessing the lowest possible value (1) when secret is higher."""
    outcome, message = check_guess(guess=1, secret=50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_guess_at_range_maximum():
    """Guessing the highest possible value (100) when secret is lower."""
    outcome, message = check_guess(guess=100, secret=50)
    assert outcome == "Too High"
    assert "LOWER" in message


# ---------------------------------------------------------------------------
# Parametrized sweep: multiple (guess, secret) pairs
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("guess, secret, expected_outcome, expected_hint_word", [
    (70, 30, "Too High", "LOWER"),
    (5,  30, "Too Low",  "HIGHER"),
    (30, 30, "Win",      None),
    (99, 1,  "Too High", "LOWER"),
    (1,  99, "Too Low",  "HIGHER"),
])
def test_hint_direction_parametrized(guess, secret, expected_outcome, expected_hint_word):
    """
    Parametrized sweep confirming hint direction is correct across
    a range of (guess, secret) pairs.
    """
    outcome, message = check_guess(guess=guess, secret=secret)
    assert outcome == expected_outcome, (
        f"guess={guess}, secret={secret}: expected outcome '{expected_outcome}', got '{outcome}'"
    )
    if expected_hint_word:
        assert expected_hint_word in message, (
            f"guess={guess}, secret={secret}: expected '{expected_hint_word}' in message, got '{message}'"
        )