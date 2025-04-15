from calculate import split_to_groups
from character_combinations import get_character_combinations

# mahjong_hand_2 = [
#         "1x", "1x", "1x", "2x", "2x",
#         "2x", "3x", "3x", "3x", "4x",
#         "4x", "4x", "5x", "5x", "5x",
#         "6x", "6x"
#     ]

mahjong_hand = [
        "1x", "1x", "1x", "2x", "2x",
        "2x", "3x", "3x", "6x", "7x",
        "7x", "7x", "5x", "5x", "5x",
        "6x", "6x"
    ]

result = split_to_groups(mahjong_hand)

for m, e in result:
    print(m, e)
    points = []
    for combination in get_character_combinations():
        s = combination.evaluate(m, e)
        if s and len(s) > 0:
            points.extend(s)
    for point in points:
        if point.exclusions:
            for exclusion in point.exclusions:
                if exclusion in points:
                    points.remove(exclusion)

    for f in points:
        print(f)