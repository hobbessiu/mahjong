from tiles import Tile, TileType
from enum import Enum
from typing import List


class MeldType(Enum):
    PONG = "PONG"
    CHOW = "CHOW"
    # KONG = "KONG"

    def __str__(self):
        chinese_characters = {
            MeldType.PONG: "碰",
            MeldType.CHOW: "上",
            # MeldType.KONG: "杠"
        }
        return chinese_characters.get(self, self.value)


class Meld:
    def __init__(self, tiles: List[Tile]):
        self.tiles = sorted(tiles)
        self.meld_type = self.determine_meld_type(tiles)
        self.tile_type = self.tiles[0].tile_type

        if not self.meld_type:
            raise ValueError("Invalid meld: {}".format(self))


    def is_pong_valid(self, tiles: List[Tile]):
        return all(tile == tiles[0] for tile in tiles)

    def is_chow_valid(self, tiles: List[Tile]):
        if any(tile.tile_type == TileType.FAAN for tile in tiles):
            return False
        
        tile_values = sorted(tile.tile_value for tile in tiles)
        return (tile_values[1] == tile_values[0] + 1 and
                tile_values[2] == tile_values[1] + 1 and
                all(tile.tile_type == tiles[0].tile_type for tile in tiles))

    def determine_meld_type(self, tiles: List[Tile]):
        if len(self.tiles) == 3:
            if self.is_pong_valid(tiles):
                return MeldType.PONG
            elif self.is_chow_valid(tiles):
                return MeldType.CHOW
        return None
    
    def __eq__(self, other):
        if not isinstance(other, Meld):
            return False
        return self.tiles == other.tiles and self.meld_type == other.meld_type

    def __lt__(self, other):
        if not isinstance(other, Meld):
            return NotImplemented
        return self.tiles < other.tiles

    def __repr__(self):
        return f"{self.tiles}"


if __name__ == "__main__":
    test_cases = []
    test_cases.append([Tile(1, TileType.SOK), Tile(2, TileType.SOK), Tile(3, TileType.SOK)])
    test_cases.append([Tile(1, TileType.SOK), Tile(1, TileType.SOK), Tile(1, TileType.SOK)])
    test_cases.append([Tile(1, TileType.FAAN), Tile(1, TileType.FAAN), Tile(1, TileType.FAAN)])
    test_cases.append([Tile(1, TileType.FAAN), Tile(2, TileType.FAAN), Tile(3, TileType.FAAN)])
    test_cases.append([Tile(8, TileType.MAAN), Tile(6, TileType.MAAN), Tile(7, TileType.MAAN)])


    for test in test_cases:
        try:
            meld = Meld(test)
            print(meld)
        except ValueError as e:
            print(f"Error: {e}")
