"""組合類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination

class AllChow(PointCombination):
    """平胡"""
    def __init__(self):
        name = "平胡"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye):
        res = []
        if all(meld.meld_type == MeldType.CHOW for meld in melds) and eye[0].tile_type == TileType.FAAN:
            res.append(self.score())
        return res

def get_combo_combinations():
    yield AllChow()
