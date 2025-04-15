import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calculate import split_to_groups

def test_split_to_groups_valid_hand_1():
    mahjong_hand = [
        "1s", "1s", "1s", "2s", "2s",
        "3s", "3s", "4s", "4s", "4s",
        "5s", "5s", "6s", "6s", "7s",
        "7s", "7s"
    ]
    result = split_to_groups(mahjong_hand)
    assert len(result) > 0  # Ensure at least one valid grouping is found
    for melds, eye in result:
        assert len(melds) == 5  # Ensure there are exactly 5 melds
        assert len(eye) == 2  # Ensure there is exactly one eye

def test_split_to_groups_valid_hand_2():
    mahjong_hand = [
        "1s", "1s", "1s", "2s", "2s",
        "2s", "3s", "3s", "3s", "4s",
        "4s", "4s", "5s", "5s", "5s",
        "6s", "6s"
    ]
    result = split_to_groups(mahjong_hand)
    assert len(result) > 0  # Ensure at least one valid grouping is found
    for melds, eye in result:
        assert len(melds) == 5  # Ensure there are exactly 5 melds
        assert len(eye) == 2  # Ensure there is exactly one eye

def test_split_to_groups_invalid_hand_length():
    mahjong_hand = [
        "1s", "1s", "1s", "2s", "2s",
        "3s", "3s", "4s", "4s", "4s",
        "5s", "5s", "6s", "6s", "7s"
    ]  # Only 15 tiles
    with pytest.raises(ValueError, match="A mahjong hand must contain exactly 17 tiles."):
        split_to_groups(mahjong_hand)

def test_split_to_groups_no_possible_eyes():
    mahjong_hand = [
        "1s", "2s", "3s", "4s", "5s",
        "6s", "7s", "8s", "9s", "1p",
        "2p", "3p", "4p", "5p", "6p",
        "7p", "8p"
    ]  # No pairs for eyes
    with pytest.raises(ValueError, match="No possible eyes in the hand."):
        split_to_groups(mahjong_hand)

def test_split_to_groups_no_valid_eye_values():
    mahjong_hand = [
        "1s", "1s", "1s", "2s", "2s",
        "3s", "3s", "4s", "4s", "4s",
        "5s", "5s", "6s", "6s", "7s",
        "8s", "9s"
    ]  # No valid eye values based on tile_value % 3
    with pytest.raises(ValueError, match="No possible eyes in the hand."):
        split_to_groups(mahjong_hand)