"""一色類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination

class SameTypeNeibourhood(PointCombination):
    """般高"""
    def __init__(self):
        name = "般高"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers):
        res = []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 2:
            return res
        for i in range(len(chows) - 1):
            for j in range(i + 1, len(chows)):
                if chows[i].tiles[0].tile_value == chows[j].tiles[0].tile_value and chows[i].tiles[0].tile_type == chows[j].tiles[0].tile_type:
                    res.append(self.score(used_melds = [chows[i], chows[j]]))
        return res

def get_one_colour_combinations():
    yield SameTypeNeibourhood()