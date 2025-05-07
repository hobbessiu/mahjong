"""三色類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination
from combinations.one_colour_combinations import SameTypeNeibourhood

class Neibourhood(PointCombination):
    """相逢"""
    def __init__(self):
        name = "相逢"
        point = 3
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 2:
            return res
        for i in range(len(chows) - 1):
            for j in range(i + 1, len(chows)):
                if chows[i].tiles[0].tile_value == chows[j].tiles[0].tile_value and chows[i].tiles[0].tile_type != chows[j].tiles[0].tile_type:
                    res.append(self.score(used_melds = [chows[i], chows[j]]))
        return res

class Three_neibourhood(PointCombination):
    """三相逢"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}三相逢"
        point = 10 if is_open else 20
        remark = "10/20"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 3:
            return res
        maan_chows = [meld for meld in chows if meld.tiles[0].tile_type == TileType.MAAN]
        sok_chows = [meld for meld in chows if meld.tiles[0].tile_type == TileType.SOK]
        tung_chows = [meld for meld in chows if meld.tiles[0].tile_type == TileType.TUNG]
        if len(maan_chows) == 0 or len(sok_chows) == 0 or len(tung_chows) == 0:
            return res
        for maan_chow in maan_chows:
            for sok_chow in sok_chows:
                for tung_chow in tung_chows:
                    if maan_chow.tiles[0].tile_value == sok_chow.tiles[0].tile_value and maan_chow.tiles[0].tile_value == tung_chow.tiles[0].tile_value:
                        exclusions = []
                        exclusions.append(ScoredCombination(Neibourhood(), used_melds = [maan_chow, sok_chow]))
                        exclusions.append(ScoredCombination(Neibourhood(), used_melds = [maan_chow, tung_chow]))
                        exclusions.append(ScoredCombination(Neibourhood(), used_melds = [sok_chow, tung_chow]))
                        is_open = any(meld.is_open for meld in [maan_chow, sok_chow, tung_chow])
                        res.append(Three_neibourhood(is_open=is_open).score(used_melds = [maan_chow, sok_chow, tung_chow], exclusions = exclusions))

        return res

class DoubleSister(PointCombination):
    """雙姊妹"""
    def __init__(self):
        name = "雙姊妹"
        point = 10
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        neibourhoods = Neibourhood().evaluate(melds, eye, flowers, position, seat)
        if len(neibourhoods) < 2:
            return res
        for i in range(len(neibourhoods) - 1):
            for j in range(i + 1, len(neibourhoods)):
                if neibourhoods[i].used_melds[0].tiles[0].tile_value != neibourhoods[j].used_melds[0].tiles[0].tile_value:
                    exclusions = [neibourhoods[i], neibourhoods[j]]
                    res.append(self.score(used_melds = neibourhoods[i].used_melds + neibourhoods[j].used_melds, exclusions = exclusions))

        return res

class AllSister(PointCombination):
    """全姊妹"""
    def __init__(self):
        name = "全姊妹"
        point = 30
        remark = "另計平糊，可另計三相逢"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        neibourhoods_dict = {}
        if len(chows) < 5:
            return []
        for c in chows:
            tile_value = c.tiles[0].tile_value
            neibourhoods_dict[tile_value] = neibourhoods_dict.get(tile_value, 0) + 1

        if len(neibourhoods_dict.keys()) > 2:
            return []
        elif len(neibourhoods_dict.keys()) == 2:
            if any(v > 3 for v in neibourhoods_dict.values()):
                return []

        return [self.score()]

class Stair(PointCombination):
    """樓梯"""
    def __init__(self):
        name = "樓梯"
        point = 30
        remark = "另計平糊，可另計步步高/二步高"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 5:
            return []
        
        chow_number = sorted([chow.tiles[0].tile_value for chow in chows])
        chow_diff = [j-i for i, j in zip(chow_number[:-1], chow_number[1:])]
        if any(diff != 1 for diff in chow_diff):
            return []
        return [self.score()]


def get_brother(brother_class, melds, eye):
    pongs = [meld for meld in melds if meld.is_pong_or_kong() and meld.tile_type != TileType.FAAN]
    pong_count_dict = {Brother().__class__.__name__: [], SmallThreeBrother().__class__.__name__: [], BigThreeBrother().__class__.__name__: []}

    while pongs:
        meld = pongs[0]
        tile_value = meld.tiles[0].tile_value
        current_pongs = [p for p in pongs if p.tiles[0].tile_value == tile_value]
        for p in current_pongs:
            pongs.remove(p)
        if len(current_pongs) == 3:
            pong_count_dict[BigThreeBrother().__class__.__name__].append(current_pongs)
        elif len(current_pongs) == 2:
            if eye[0].tile_value == tile_value:
                pong_count_dict[SmallThreeBrother().__class__.__name__].append(current_pongs)
            else:
                pong_count_dict[Brother().__class__.__name__].append(current_pongs)
    return pong_count_dict[brother_class.__class__.__name__]

class Brother(PointCombination):
    """兄弟"""
    def __init__(self):
        name = "兄弟"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        combinations = get_brother(self, melds, eye)
        for c in combinations:
            res.append(self.score(used_melds = c))
        return res

class SmallThreeBrother(PointCombination):
    """小三兄弟"""
    def __init__(self):
        name = "小三兄弟"
        point = 10
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        combinations = get_brother(self, melds, eye)
        for c in combinations:
            res.append(self.score(used_melds = c, used_eye= eye))
        return res

class BigThreeBrother(PointCombination):
    """大三兄弟"""
    def __init__(self):
        name = "大三兄弟"
        point = 15
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        combinations = get_brother(self, melds, eye)
        for c in combinations:
            res.append(self.score(used_melds = c))
        return res

class StepUp(PointCombination):
    """步步高"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}步步高"
        point = 5 if is_open else 10
        remark = "5/10"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 3:
            return []
        chows.sort(key=lambda x: x.tiles[0].tile_value)
        for chow in chows:
            next_chows = [c for c in chows if c.tiles[0].tile_value == chow.tiles[0].tile_value + 1 and c.tiles[0].tile_type != chow.tiles[0].tile_type]
            for next_chow in next_chows:
                next_next_chows = [c for c in chows if c.tiles[0].tile_value == next_chow.tiles[0].tile_value + 1 and c.tiles[0].tile_type != next_chow.tiles[0].tile_type]
                for next_next_chow in next_next_chows:
                    used_melds = [chow, next_chow, next_next_chow]
                    is_open = any(meld.is_open for meld in used_melds)
                    res.append(StepUp(is_open=is_open).score(used_melds = used_melds))
        
        return res

class TwoStepUp(PointCombination):
    """二步高"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}二步高"
        point = 5 if is_open else 10
        remark = "5/10"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 3:
            return []
        chows.sort(key=lambda x: x.tiles[0].tile_value)
        for chow in chows:
            next_chows = [c for c in chows if c.tiles[0].tile_value == chow.tiles[0].tile_value + 2 and c.tiles[0].tile_type != chow.tiles[0].tile_type]
            for next_chow in next_chows:
                next_next_chows = [c for c in chows if c.tiles[0].tile_value == next_chow.tiles[0].tile_value + 2 and c.tiles[0].tile_type != next_chow.tiles[0].tile_type]
                for next_next_chow in next_next_chows:
                    used_melds = [chow, next_chow, next_next_chow]
                    is_open = any(meld.is_open for meld in used_melds)
                    res.append(TwoStepUp(is_open=is_open).score(used_melds = used_melds))
        return res

def get_three_colour_combinations():
    yield Neibourhood()
    yield Three_neibourhood()
    yield DoubleSister()
    yield AllSister()
    yield Stair()
    yield Brother()
    yield SmallThreeBrother()
    yield BigThreeBrother()
    yield StepUp()
    yield TwoStepUp()