# 字牌類
from tiles import Tile, TileType
from point_combination import PointCombination, ScoredCombination


# 無字
class NoCharacter(PointCombination):
    def __init__(self):
        name = "無字"
        point = 1
        super().__init__(name, point)

    def evaluate(self, melds, eye):
        res = []
        if all(meld.tile_type != TileType.FAAN for meld in melds) and all(tile.tile_type != TileType.FAAN for tile in eye):
            res += self.score()
        return res

# 風/位
class PositionCharacter(PointCombination):
    def __init__(self):
        name = "風"
        point = 1
        remark = "正風/位 + 1番"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye):
        res = []
        for meld in melds:
            if meld.tile_type == TileType.FAAN and meld.tiles[0].tile_value <= 4:
                res.append(self.score(used_melds = [meld]))
        return res

# 三元牌
class FaanCharacter(PointCombination):
    def __init__(self):
        name = "三元牌"
        point = 2
        super().__init__(name, point)

    def evaluate(self, melds, eye):
        res = []
        for meld in melds:
            if meld.tile_type == TileType.FAAN and meld.tiles[0].tile_value >= 5:
                res.append(self.score(used_melds = [meld]))
        return res

# 小三元
class SmallThreeCharacter(PointCombination):
    def __init__(self):
        name = "小三元"
        point = 20
        super().__init__(name, point)

    def evaluate(self, melds, eye):
        res = []
        isThreeCharacter = lambda t: t.tile_type == TileType.FAAN and t.tile_value >= 5

        if not isThreeCharacter(eye[0]):
            return res
        used_melds = [meld for meld in melds if isThreeCharacter(meld.tiles[0])]

        if len(used_melds) == 2:
            res.append(self.score(used_melds = used_melds, used_eye = eye))
        return res

# 大三元
class BigThreeCharacter(PointCombination):
    def __init__(self):
        name = "大三元"
        point = 40
        super().__init__(name, point)

    def evaluate(self, melds, eye):
        res = []
        isThreeCharacter = lambda t: t.tile_type == TileType.FAAN and t.tile_value >= 5

        used_melds = [meld for meld in melds if isThreeCharacter(meld.tiles[0])]

        if len(used_melds) == 3:
            exclusions = []
            for meld in used_melds:
                exclusions.append(ScoredCombination(FaanCharacter(), used_melds = [meld]))

            res.append(self.score(used_melds = used_melds, exclusions = exclusions))
        return res

def get_character_combinations():
    yield NoCharacter()
    yield PositionCharacter()
    yield FaanCharacter()
    yield SmallThreeCharacter()
    yield BigThreeCharacter()

