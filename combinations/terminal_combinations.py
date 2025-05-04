"""么九類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination

class AllTerminalAndChracter(PointCombination):
    """混帶么"""
    def __init__(self):
        name = "混帶么"
        point = 20
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers):

        if not (eye[0].tile_type == TileType.FAAN or eye[0].tile_value in [1, 9]):
            return []
        for meld in melds:
            if not (meld.tile_type == TileType.FAAN or any(t for t in meld.tiles if t.tile_value in [1, 9])):
                return []
        return [self.score()]

class AllTerminal(PointCombination):
    """全帶么"""
    def __init__(self):
        name = "全帶么"
        point = 40
        remark = "另帶缺五"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers):
        if eye[0].tile_type == TileType.FAAN or not eye[0].tile_value in [1, 9]:
            return []
        for meld in melds:
            if meld.tile_type == TileType.FAAN or not any(t for t in meld.tiles if t.tile_value in [1, 9]):
                return []
        return [self.score(exclusions=[ScoredCombination(AllTerminalAndChracter())])]

class MixOldHead(PointCombination):
    """混老頭"""
    def __init__(self):
        name = "混老頭"
        point = 40
        remark = "另計對對胡/嚦咕"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers):

        if not (eye[0].tile_type == TileType.FAAN or eye[0].tile_value in [1, 9]):
            return []
        for meld in melds:
            if not meld.meld_type == MeldType.PONG or not (meld.tile_type == TileType.FAAN or any(t for t in meld.tiles if t.tile_value in [1, 9])):
                return []
        return [self.score(exclusions=[ScoredCombination(AllTerminalAndChracter())])]

class AllOldHead(PointCombination):
    """清老頭"""
    def __init__(self):
        name = "清老頭"
        point = 80
        remark = "另計對對胡/嚦咕"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers):
        if eye[0].tile_type == TileType.FAAN or not eye[0].tile_value in [1, 9]:
            return []
        for meld in melds:
            if meld.tile_type == TileType.FAAN or not meld.meld_type == MeldType.PONG or not any(t for t in meld.tiles if t.tile_value in [1, 9]):
                return []
        return [self.score(exclusions=[ScoredCombination(MixOldHead()), ScoredCombination(AllTerminal())])]

class PongOldAndYoung(PointCombination):
    """老少 (碰)"""
    def __init__(self):
        name = "老少 (碰)"
        point = 5
        remark = "同色111 999"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers):
        res = []

        for meld in melds:
            if meld.tile_type != TileType.FAAN and meld.tiles[0].tile_value == 1 and meld.meld_type == MeldType.PONG:
                matching_melds = [m for m in melds if m.tile_type == meld.tile_type and m.meld_type == meld.meld_type and m.tiles[-1].tile_value == 9]
                for matching_meld in matching_melds:
                    res.append(self.score(used_melds=[meld, matching_meld]))
        return res

class ChowOldAndYoung(PointCombination):
    """老少 (上)"""
    def __init__(self):
        name = "老少 (上)"
        point = 3
        remark = "同色123 789"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers):
        res = []

        for meld in melds:
            if meld.tile_type != TileType.FAAN and meld.tiles[0].tile_value == 1 and meld.meld_type == MeldType.CHOW:
                matching_melds = [m for m in melds if m.tile_type == meld.tile_type and m.meld_type == meld.meld_type and m.tiles[-1].tile_value == 9]
                for matching_meld in matching_melds:
                    res.append(self.score(used_melds=[meld, matching_meld]))
        return res
                    
class NoTerminal(PointCombination):
    """斷么九"""
    def __init__(self):
        name = "斷么九"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers):
        res = []
        if eye[0].tile_type == TileType.FAAN or eye[0].tile_value in [1, 9]:
            return []
        for meld in melds:
            if meld.tile_type == TileType.FAAN or any(t for t in meld.tiles if t.tile_value in [1, 9]):
                return []
        return [self.score()]

class AllWithOneTileOrCharacter(PointCombination):
    """混帶X"""
    def __init__(self, tile_value: int = 0, scored_times: int = 1):
        name = "混帶X" if tile_value == 0 else f"混帶{tile_value}"
        point_mapping = {1: 30, 2: 20, 3: 10}
        point = point_mapping.get(scored_times, 0)
        remark = "1-9任一數字，除番子外每章包含X，混帶1/9可另計混帶么, 如超過一種，計算方法為2種50番，3種60番"
        super().__init__(name, point, remark)
    
    def __eq__(self, value):
        if isinstance(value, AllWithOneTileOrCharacter):
            return self.name == value.name
        return False

    def evaluate(self, melds, eye, flowers):
        res = []
        class StopLooping(Exception): pass
        scored_times = 0
        for i in range(1, 10):
            try:
                if not (eye[0].tile_type == TileType.FAAN or eye[0].tile_value == i):
                    raise StopLooping()
                for meld in melds:
                    if not (meld.tile_type == TileType.FAAN or any(t for t in meld.tiles if t.tile_value == i)):
                        raise StopLooping()
            except StopLooping:
                continue

            scored_times += 1
            res.append(AllWithOneTileOrCharacter(tile_value=i, scored_times=scored_times).score())
        return res

class AllWithOneTile(PointCombination):
    """全帶X"""
    def __init__(self, tile_value: int = 0):
        name = "全帶X" if tile_value == 0 else f"全帶{tile_value}"
        point = 60
        remark = "1-9任一數字,沒有番子,每章包含X, 全帶1/9可另計全帶么"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers):
        res = []
        class StopLooping(Exception): pass
        for i in range(1, 10):
            try:
                if eye[0].tile_type == TileType.FAAN or eye[0].tile_value != i:
                    raise StopLooping()
                for meld in melds:
                    if meld.tile_type == TileType.FAAN or not any(t for t in meld.tiles if t.tile_value == i):
                        raise StopLooping()
            except StopLooping:
                continue
            res.append(AllWithOneTile(tile_value=i).score(exclusions=[ScoredCombination(AllWithOneTileOrCharacter(tile_value=i, scored_times=1))]))
        return res

class NoFive(PointCombination):
    """缺5"""
    def __init__(self):
        name = "缺5"
        point = 10
        remark = "不能有番子"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers):
        res = []
        if eye[0].tile_type == TileType.FAAN or eye[0].tile_value == 5:
            return []
        for meld in melds:
            if meld.tile_type == TileType.FAAN or any(t for t in meld.tiles if t.tile_value == 5):
                return []
        return [self.score()]

def get_terminal_combinations():
    yield AllTerminalAndChracter()
    yield AllTerminal()
    yield MixOldHead()
    yield AllOldHead()
    yield PongOldAndYoung()
    yield ChowOldAndYoung()
    yield NoTerminal()
    yield AllWithOneTileOrCharacter()
    yield AllWithOneTile()
    yield NoFive()
    