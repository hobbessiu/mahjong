from tiles import Tile, TileType
from collections import Counter, OrderedDict
from itertools import combinations
from meld import Meld

def split_to_groups(mahjong_hand: list[str]):
    """
    Splits the mahjong hand of 17 tiles into exactly 5 melds and one eye.
    All tiles must be used.
    group of 3 tile (meld): 3 identical tiles, or 3 consecutive tiles of the same type.
    group of 2 tile (eye): 2 identical tiles.

    TODO: special cases like 7 pairs, 13 orphans, etc.
    TODO: special cases when 4 tiles are the same.
    Args:
        mahjong_hand (list[str]): A list of 17 tiles represented as strings.
    """
def is_meld(group):
    """Check if a group of 3 tiles is a valid meld."""
    if len(group) != 3:
        return False
    # Check for identical tiles
    if group[0] == group[1] == group[2]:
        return True
    # Check for consecutive tiles of the same type
    try:
        values = sorted(int(tile[:-1]) for tile in group)
        return values[1] == values[0] + 1 and values[2] == values[1] + 1 and \
                group[0][-1] == group[1][-1] == group[2][-1]
    except ValueError:
        return False

def is_eye(group):
    """Check if a group of 2 tiles is a valid eye."""
    return len(group) == 2 and group[0] == group[1]

def split_to_groups(mahjong_hand):
    def extract_chow(current_tile, remaining_tiles, remaining_tiles_count):
        melds.append(Meld([current_tile, current_tile.next_tile(), current_tile.next_tile().next_tile()]))
        remaining_tiles_count.subtract([current_tile, current_tile.next_tile(), current_tile.next_tile().next_tile()])
        remaining_tiles.remove(current_tile)
        remaining_tiles.remove(current_tile.next_tile())
        remaining_tiles.remove(current_tile.next_tile().next_tile())
    
    def extract_pong(current_tile, remaining_tiles, remaining_tiles_count):
        melds.append(Meld([current_tile, current_tile, current_tile]))
        remaining_tiles_count.subtract([current_tile, current_tile, current_tile])
        remaining_tiles.remove(current_tile)
        remaining_tiles.remove(current_tile)
        remaining_tiles.remove(current_tile)

    result = []

    """Split the mahjong hand into valid groups of melds and eyes."""
    if len(mahjong_hand) != 17:
        raise ValueError("A mahjong hand must contain exactly 17 tiles.")
    
    tiles = sorted([Tile.from_string(tile) for tile in mahjong_hand])

    tile_counts = Counter(tiles)
    possible_eyes = [tile for tile, count in tile_counts.items() if count >= 2]
    if not possible_eyes:
        raise ValueError("No possible eyes in the hand.")

    all_tiles = list(tile_counts.elements())

    possible_eye__values_dict = {0: [3,6,9],
                                 1: [2,5,8],
                                 2: [1,4,7],}

    total_value = sum(tile.tile_value for tile in tiles)
    possible_eye_values = possible_eye__values_dict[total_value % 3]

    possible_eyes = [tile for tile in possible_eyes if tile.tile_value in possible_eye_values]
    if not possible_eyes:
        raise ValueError("No possible eyes in the hand.")

    for possible_eye in possible_eyes:
        extra_attempts = []
        while True:
            melds = []
            remaining_tiles = list(all_tiles)
            remaining_tiles_count = Counter(remaining_tiles)

            eye = [possible_eye, possible_eye]
            # remaining_tiles.remove(possible_eye)
            # remaining_tiles.remove(possible_eye)
            

            

            remaining_tiles_count.subtract(eye)
            remaining_tiles.remove(possible_eye)
            remaining_tiles.remove(possible_eye)

        
            while len(remaining_tiles) != 0:
                current_tile = remaining_tiles[0]
                current_tile_count = remaining_tiles_count[current_tile]

                if current_tile_count < 3:
                    if current_tile_count > remaining_tiles_count.get(current_tile.next_tile(), 0) or \
                        current_tile_count > remaining_tiles_count.get(current_tile.next_tile().next_tile(), 0):
                        break
                    
                    for _ in range(current_tile_count):
                        extract_chow(current_tile, remaining_tiles, remaining_tiles_count)

                else:
                    if remaining_tiles_count.get(current_tile.next_tile(), 0) >= 3 and \
                        remaining_tiles_count.get(current_tile.next_tile().next_tile(), 0) >= 3:
                        if not current_tile in extra_attempts:
                            extract_pong(current_tile, remaining_tiles, remaining_tiles_count)
                            extra_attempts.append(current_tile)
                            
                        else:
                            extra_attempts.remove(current_tile)
                            for _ in range(current_tile_count):
                                extract_chow(current_tile, remaining_tiles, remaining_tiles_count)
                    else:
                        extract_pong(current_tile, remaining_tiles, remaining_tiles_count)
            
            if len(melds) == 5:
                melds.sort()
                existing_melds = [m for m,e in result]

                if melds not in existing_melds:
                    result.append((melds, eye))

        
            if len(extra_attempts) == 0:
                break

    return result




if __name__ == "__main__":
    mahjong_hand_1 = [
        "1s", "1s", "1s", "2s", "2s",
        "3s", "3s", "4s", "4s", "4s",
        "5s", "5s", "6s", "6s", "7s",
        "7s", "7s"
    ]

    mahjong_hand_2 = [
        "1s", "1s", "1s", "2s", "2s",
        "2s", "3s", "3s", "3s", "4s",
        "4s", "4s", "5s", "5s", "5s",
        "6s", "6s"
    ]

    print("Input:")
    print(sorted([Tile.from_string(tile) for tile in mahjong_hand_2]))

    print("")
    print("Output:")
    result = split_to_groups(mahjong_hand_2)
    for (melds, eye) in result:
        print(melds + eye)