"""龍類"""
from combinations.point_combination import PointCombination
from meld import Meld, MeldType
from tiles import Tile, TileType
from typing import List

def get_dragons(melds: List[Meld], meld_type_count: int, is_open: bool) -> List[List[Meld]]:
    dragons = []
    chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
    c_1s = [chow for chow in chows if chow.tiles[0].tile_value == 1]
    c_4s = [chow for chow in chows if chow.tiles[0].tile_value == 4]
    c_7s = [chow for chow in chows if chow.tiles[0].tile_value == 7]
    if len(c_1s) == 0 or len(c_4s) == 0 or len(c_7s) == 0:
        return dragons
    for c_1 in c_1s:
        for c_4 in c_4s:
            for c_7 in c_7s:
                used_melds = [c_1, c_4, c_7]
                res_is_open = any(meld.is_open for meld in used_melds)
                res_meld_type_count = len(set(t.tile_type for t in used_melds))
                dragons.append((res_meld_type_count, used_melds, res_is_open))
    
    return [m for c, m, o in dragons if c == meld_type_count and o == is_open]

class OpenTwoColourDragon(PointCombination):
    """兩色明雜龍"""
    def __init__(self):
        name = "兩色明雜龍"
        point = 5
        remark = "打出牌或已落地為明，全為手上牌為暗"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        dragons = get_dragons(melds, 2, True)
        res = []
        for dragon in dragons:
            res.append(self.score(used_melds = dragon))
        return res

class CloseTwoColourDragon(PointCombination):
    """兩色暗雜龍"""
    def __init__(self):
        name = "兩色暗雜龍"
        point = 10
        remark = "打出牌或已落地為明，全為手上牌為暗"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        dragons = get_dragons(melds, 2, False)
        res = []
        for dragon in dragons:
            res.append(self.score(used_melds = dragon))
        return res

class OpenThreeColourDragon(PointCombination):
    """三色明雜龍"""
    def __init__(self):
        name = "三色明雜龍"
        point = 8
        remark = "打出牌或已落地為明，全為手上牌為暗"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        dragons = get_dragons(melds, 3, True)
        res = []
        for dragon in dragons:
            res.append(self.score(used_melds = dragon))
        return res

class CloseThreeColourDragon(PointCombination):
    """三色暗雜龍"""
    def __init__(self):
        name = "三色暗雜龍"
        point = 15
        remark = "打出牌或已落地為明，全為手上牌為暗"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        dragons = get_dragons(melds, 3, False)
        res = []
        for dragon in dragons:
            res.append(self.score(used_melds = dragon))
        return res

class OpenSingleColourDragon(PointCombination):
    """明清龍"""
    def __init__(self):
        name = "明清龍"
        point = 10
        remark = "打出牌或已落地為明，全為手上牌為暗"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        dragons = get_dragons(melds, 1, True)
        res = []
        for dragon in dragons:
            res.append(self.score(used_melds = dragon))
        return res

class CloseSingleColourDragon(PointCombination):
    """暗清龍"""
    def __init__(self):
        name = "暗清龍"
        point = 20
        remark = "打出牌或已落地為明，全為手上牌為暗"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        dragons = get_dragons(melds, 1, False)
        res = []
        for dragon in dragons:
            res.append(self.score(used_melds = dragon))
        return res

def get_dragon_combinations():
    yield OpenTwoColourDragon()
    yield CloseTwoColourDragon()
    yield OpenThreeColourDragon()
    yield CloseThreeColourDragon()
    yield OpenSingleColourDragon()
    yield CloseSingleColourDragon()

def get_dragon_combinations_dict():
    for combination in get_dragon_combinations():
        yield combination.name, combination.point, combination.remark