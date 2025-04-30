from enum import Enum

class TileType(Enum):
    SOK = "s"
    TUNG = "t"
    MAAN = "m"
    FAAN = "x"

class Tile:
    def __init__(self, tile_value: int, tile_type: TileType, is_open: bool = False):
        self.tile_value = tile_value
        self.tile_type = tile_type
        self.is_open = is_open
        self.tile_string = str(tile_value) + tile_type.value
    
    @classmethod
    def from_string(cls, tile_string: str):
        tile_value_str, tile_type_str = map(str, tile_string)
        tile_value = int(tile_value_str)
        tile_type = TileType(tile_type_str)
        return cls(tile_value, tile_type)
    
    @classmethod
    def from_unicode(cls, tile_unicode: str):
        unicode_dict = {
            TileType.SOK: '🀐🀑🀒🀓🀔🀕🀖🀗🀘',
            TileType.TUNG: '🀙🀚🀛🀜🀝🀞🀟🀠🀡',
            TileType.MAAN: '🀇🀈🀉🀊🀋🀌🀍🀎🀏',
            TileType.FAAN: '🀀🀁🀂🀃🀄︎🀅🀆'}
        
        for tile_type, unicode_string in unicode_dict.items():
            if tile_unicode in unicode_string:
                tile_value = unicode_string.index(tile_unicode) + 1
                return cls(tile_value, tile_type)
        raise ValueError(f"Invalid tile unicode {tile_unicode}.")

    def set_open(self):
        self.is_open = True

    def next_tile(self):
        if self.tile_type == TileType.FAAN:
            return None
        if self.tile_value == 9:
            return None
        return Tile(self.tile_value + 1, self.tile_type)

    def __repr__(self):
        return self.to_unicode()

    def __eq__(self, other):
        return (
            isinstance(other, Tile)
            and self.tile_value == other.tile_value
            and self.tile_type == other.tile_type
        )

    def __hash__(self):
        return hash((self.tile_value, self.tile_type.value))

    def __lt__(self, other):
        if self.tile_type == other.tile_type:
            return self.tile_value < other.tile_value
        return self.tile_type.value < other.tile_type.value

    def to_unicode(self):
        unicode_dict = {
            TileType.SOK: '🀐🀑🀒🀓🀔🀕🀖🀗🀘',
            TileType.TUNG: '🀙🀚🀛🀜🀝🀞🀟🀠🀡',
            TileType.MAAN: '🀇🀈🀉🀊🀋🀌🀍🀎🀏',
            TileType.FAAN: '🀀🀁🀂🀃🀄︎🀅🀆'}

        if self.tile_string == "6x":
            return "\U0001F005"
        elif self.tile_string == "7x":
            return '🀆'
        return unicode_dict[self.tile_type][self.tile_value - 1]

    def __str__(self):
        chinese_characters = {
            TileType.SOK: "索",
            TileType.TUNG: "筒",
            TileType.MAAN: "萬",
            TileType.FAAN: "字"
        }

        faan_characters = {
            1: "東",
            2: "南",
            3: "西",
            4: "北",
            5: "中",
            6: "發",
            7: "白"
        }

        chinese_numbers = {
            1: "一",
            2: "二",
            3: "三",
            4: "四",
            5: "五",
            6: "六",
            7: "七",
            8: "八",
            9: "九"
        }

        try:
            match self.tile_type:
                case TileType.FAAN:
                    return f"{faan_characters[self.tile_value]}"
                case TileType.SOK | TileType.TUNG | TileType.MAAN:
                    return f"{chinese_numbers[self.tile_value]}{chinese_characters[self.tile_type]}"
        except KeyError:
            raise ValueError(f"Invalid tile value {self.tile_value} for tile type {self.tile_type}.")


if __name__ == "__main__":
    # Example usage
    tile = Tile.from_string("6x")
    print(tile)  
    print(tile.tile_value)
    print(tile.tile_type)  
    print(tile.tile_string)
    print(tile.to_unicode())

    tile = Tile.from_string("7x")
    print(tile)  
    print(tile.tile_value)
    print(tile.tile_type)  
    print(tile.tile_string)
    print(tile.to_unicode())

