from calculate import split_to_groups
from tiles import Tile
from combinations.character_combinations import get_character_combinations
from combinations.combo_combination import get_combo_combinations

def get_all_combinations():
    

    for combo in get_combo_combinations():
        yield combo

    for character in get_character_combinations():
        yield character

def calculate(mahjong_hand):
    result = split_to_groups(mahjong_hand)
    for m, e in result:
        print(m, e)
        points = []
        for combination in get_all_combinations():
            s = combination.evaluate(m, e)
            if s and len(s) > 0:
                points.extend(s)
        res = points.copy()
        for point in points:
            if point.exclusions:
                for exclusion in point.exclusions:
                    if exclusion in res:
                        res.remove(exclusion)

    return res

def calculate_from_unicode(mahjong_hand_unicode):
    mahjong_hand = [Tile.from_unicode(tile) for tile in mahjong_hand_unicode]
    return calculate(mahjong_hand)

if __name__ == "__main__":
    # mahjong_hand_2 = [
    #         "1x", "1x", "1x", "2x", "2x",
    #         "2x", "3x", "3x", "3x", "4x",
    #         "4x", "4x", "5x", "5x", "5x",
    #         "6x", "6x"
    #     ]

    mahjong_hand_str = [
        "1x", "1x", "1x", "2x", "2x",
        "2x", "3x", "3x", "6x", "7x",
        "7x", "7x", "5x", "5x", "5x",
        "6x", "6x"
    ]

    mahjong_hand = [Tile.from_string(tile) for tile in mahjong_hand_str]

    points = calculate(mahjong_hand)

    for point in points:
        print(point)
