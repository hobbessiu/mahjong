from calculate import split_to_groups
from tiles import Tile
from combinations.character_combinations import get_character_combinations
from combinations.combo_combination import get_combo_combinations
from combinations.dragon_combinations import get_dragon_combinations
from combinations.terminal_combinations import get_terminal_combinations
from combinations.three_colour_combinations import get_three_colour_combinations
from combinations.one_colour_combinations import get_one_colour_combinations

def get_all_combinations():
    for combo in get_combo_combinations():
        yield combo

    for character in get_character_combinations():
        yield character

    for dragon in get_dragon_combinations():
        yield dragon
    
    for terminal in get_terminal_combinations():
        yield terminal
    
    for three_colour in get_three_colour_combinations():
        yield three_colour
    
    for one_colour in get_one_colour_combinations():
        yield one_colour

def calculate(mahjong_hand):
    result = split_to_groups(mahjong_hand)
    score_combinations = []
    for m, e, f in result:
        print(m, e, f)
        points = []
        for combination in get_all_combinations():
            s = combination.evaluate(m, e, f)
            if s and len(s) > 0:
                points.extend(s)
        res = points.copy()
        for point in points:
            if point.exclusions:
                for exclusion in point.exclusions:
                    if exclusion in res:
                        res.remove(exclusion)
                        res.sort(key=lambda x: x.point_combination.point, reverse=True)
        score_combinations.append(res)
    
    for i in range(len(score_combinations)):
        for j in range(i + 1, len(score_combinations)):
            for p in score_combinations[i]:
                if p in score_combinations[j]:
                    score_combinations[j].remove(p)
    
    return [s for score_combination in score_combinations for s in score_combination]

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
