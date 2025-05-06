"""組合類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination
from combinations.character_combinations import NoCharacter
from combinations.flower_combinations import NoLetterAndFlower

class AllChow(PointCombination):
    """平胡"""
    def __init__(self):
        name = "平胡"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        res = []
        if all(meld.meld_type == MeldType.CHOW for meld in melds):
            res.append(self.score())
        return res

class AllChowNoLetterAndFlower(PointCombination):
    """無字花大平胡"""
    def __init__(self):
        name = "無字花大平胡"
        point = 15
        remark = "不另計平胡/無字花"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position):
        res = []
        if all(meld.meld_type == MeldType.CHOW for meld in melds) and eye[0].tile_type != TileType.FAAN and len(flowers) == 0:
            res.append(self.score(exclusions = [ScoredCombination(NoCharacter()), ScoredCombination(AllChow()), ScoredCombination(NoLetterAndFlower())]))
        return res

class MissingOneTileType(PointCombination):
    """缺一門"""
    def __init__(self):
        name = "缺一門"
        point = 5
        remark = "不能有番子"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position):
        res = []
        tile_types = set(t.tile_type for t in melds + eye)
        if TileType.FAAN in tile_types:
            return []

        if len(tile_types) == 2:
            res.append(self.score())
        return res

def get_all_five_types_checks():
    has_direction = lambda tiles: any(t for t in tiles if t.tile_value <= 4 and t.tile_type == TileType.FAAN)
    has_three_character = lambda tiles: any(t for t in tiles if t.tile_value >=5 and t.tile_type == TileType.FAAN)
    has_sok = lambda tiles: any(t for t in tiles if t.tile_type == TileType.SOK)
    has_maan = lambda tiles: any(t for t in tiles if t.tile_type == TileType.MAAN)
    has_tung = lambda tiles: any(t for t in tiles if t.tile_type == TileType.TUNG)

    return [
        has_direction,
        has_three_character,
        has_sok,
        has_maan,
        has_tung
    ]

class SmallAllFiveTileType(PointCombination):
    """小五門齊"""
    def __init__(self):
        name = "小五門齊"
        point = 8
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        res = []

        checks = get_all_five_types_checks()
        counter = 0
        missing_check = None
        for check in checks:
            if check([m.tiles[0] for m in melds]):
                counter += 1
            else:
                missing_check = check
        if counter == 4 and missing_check(eye):
            res.append(self.score())
        
        return res



class BigAllFiveTileType(PointCombination):
    """大五門齊"""
    def __init__(self):
        name = "大五門齊"
        point = 15
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        res = []
        checks = get_all_five_types_checks()
        if all(check([m.tiles[0] for m in melds]) for check in checks):
            res.append(self.score(exclusions=[ScoredCombination(SmallAllFiveTileType())]))
        return res

class SmallAllSevenTileType(PointCombination):
    """小七門齊"""
    def __init__(self):
        name = "小七門齊"
        point = 10
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        res = []

        checks = get_all_five_types_checks()
        counter = 0
        missing_check = None
        for check in checks:
            if check([m.tiles[0] for m in melds]):
                counter += 1
            else:
                missing_check = check
        if counter == 4 and missing_check(eye):
            if any(f for f in flowers if f.tile_value <= 4) and any(f for f in flowers if f.tile_value >=5):
                res.append(self.score(exclusions=[ScoredCombination(SmallAllFiveTileType())]))
        return res

class BigAllSevenTileType(PointCombination):
    """大七門齊"""
    def __init__(self):
        name = "大七門齊"
        point = 20
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        res = []
        checks = get_all_five_types_checks()
        if all(check([m.tiles[0] for m in melds]) for check in checks):
            if any(f for f in flowers if f.tile_value <= 4) and any(f for f in flowers if f.tile_value >=5):
                res.append(self.score(exclusions=[ScoredCombination(BigAllFiveTileType())]))
        return res

class HalfFromOthers(PointCombination):
    """半求人"""
    def __init__(self):
        name = "半求人"
        point = 8
        remark = "不另計自摸/獨獨"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position):
        if all(m.is_open for m in melds):
            return [self.score()]

class FullFromOthers(PointCombination):
    """全求人"""
    def __init__(self):
        name = "全求人"
        point = 15
        remark = "不另計獨獨"
        super().__init__(name, point, remark)
    def evaluate(self, melds, eye, flowers, position):
        if all(m.is_open for m in melds) and all(e.is_open for e in eye):
            return [self.score(exclusions=[ScoredCombination(HalfFromOthers())])]


def get_combo_combinations():
    yield AllChow()
    yield AllChowNoLetterAndFlower()
    yield MissingOneTileType()
    yield SmallAllFiveTileType()
    yield BigAllFiveTileType()
    yield SmallAllSevenTileType()
    yield BigAllSevenTileType()
    yield HalfFromOthers()
    yield FullFromOthers()