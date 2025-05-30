"""字牌類"""
from tiles import Tile, TileType
from combinations.point_combination import PointCombination, ScoredCombination

def get_position_character_exclusions(meld):
    """return a list of exclusions for position character"""
    return [ScoredCombination(BadPositionCharacter(), used_melds = [meld]),
            ScoredCombination(GoodPositionCharacter(), used_melds = [meld]),
            ScoredCombination(GoodSeatCharacter(), used_melds = [meld])]

class NoCharacter(PointCombination):
    """ 無字 """
    def __init__(self):
        name = "無字"
        point = 1
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        if all(meld.tile_type != TileType.FAAN for meld in melds) and all(tile.tile_type != TileType.FAAN for tile in eye):
            res.append(self.score())
        return res

class BadPositionCharacter(PointCombination):
    """風"""
    def __init__(self):
        name = f"風"
        point = 1
        remark = "正風/位 + 1番"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        for meld in melds:
            if meld.tile_type == TileType.FAAN and meld.tiles[0].tile_value <= 4:
                if meld.tiles[0].tile_value not in [position, seat]:
                    res.append(self.score(used_melds = [meld]))
        return res

class GoodPositionCharacter(PointCombination):
    """正風"""
    def __init__(self):
        name = f"正風"
        point = 2
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        for meld in melds:
            if meld.tile_type == TileType.FAAN and meld.tiles[0].tile_value == position:
                res.append(self.score(used_melds = [meld]))
        return res

class GoodSeatCharacter(PointCombination):
    """正位"""
    def __init__(self):
        name = f"正位"
        point = 2
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        for meld in melds:
            if meld.tile_type == TileType.FAAN and meld.tiles[0].tile_value == seat:
                res.append(self.score(used_melds = [meld]))
        return res

class FaanCharacter(PointCombination):
    """ 三元牌 """
    def __init__(self):
        name = "三元牌"
        point = 2
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        for meld in melds:
            if meld.tile_type == TileType.FAAN and meld.tiles[0].tile_value >= 5:
                res.append(self.score(used_melds = [meld]))
        return res

class SmallThreeCharacter(PointCombination):
    """" 小三元 """
    def __init__(self):
        name = "小三元"
        point = 20
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        isThreeCharacter = lambda t: t.tile_type == TileType.FAAN and t.tile_value >= 5

        if not isThreeCharacter(eye[0]):
            return res
        used_melds = [meld for meld in melds if isThreeCharacter(meld.tiles[0])]

        if len(used_melds) == 2:
            exclusions = []
            for meld in used_melds:
                exclusions.append(ScoredCombination(FaanCharacter(), used_melds = [meld]))
            res.append(self.score(used_melds = used_melds, used_eye = eye, exclusions = exclusions))
        return res

class BigThreeCharacter(PointCombination):
    """ 大三元 """
    def __init__(self):
        name = "大三元"
        point = 40
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        isThreeCharacter = lambda t: t.tile_type == TileType.FAAN and t.tile_value >= 5

        used_melds = [meld for meld in melds if isThreeCharacter(meld.tiles[0])]

        if len(used_melds) == 3:
            exclusions = []
            for meld in used_melds:
                exclusions.append(ScoredCombination(FaanCharacter(), used_melds = [meld]))

            res.append(self.score(used_melds = used_melds, exclusions = exclusions))
        return res

class SmallThreeDirection(PointCombination):
    """ 小三風 """
    def __init__(self):
        name = "小三風"
        point = 15
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        isDirection = lambda t: t.tile_type == TileType.FAAN and t.tile_value <= 4

        if not isDirection(eye[0]):
            return res
        used_melds = [meld for meld in melds if isDirection(meld.tiles[0])]

        if len(used_melds) == 2:
            exclusions = []
            for meld in used_melds:
                exclusions += get_position_character_exclusions(meld)

            res.append(self.score(used_melds = used_melds, used_eye = eye, exclusions = exclusions))
        return res

class BigThreeDirection(PointCombination):
    """ 大三風 """
    def __init__(self):
        name = "大三風"
        point = 30
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        isDirection = lambda t: t.tile_type == TileType.FAAN and t.tile_value <= 4

        used_melds = [meld for meld in melds if isDirection(meld.tiles[0])]

        if len(used_melds) == 3 and eye[0].tile_type != TileType.FAAN:
            exclusions = []
            for meld in used_melds:
                exclusions += get_position_character_exclusions(meld)
            res.append(self.score(used_melds = used_melds, exclusions = exclusions))
        return res

class SmallFourDirection(PointCombination):
    """ 小四喜 """
    def __init__(self):
        name = "小四喜"
        point = 60
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        isDirection = lambda t: t.tile_type == TileType.FAAN and t.tile_value <= 4

        used_melds = [meld for meld in melds if isDirection(meld.tiles[0])]

        if len(used_melds) == 3 and eye[0].tile_type == TileType.FAAN:
            exclusions = []
            for meld in used_melds:
                exclusions += get_position_character_exclusions(meld)

            res.append(self.score(used_melds = used_melds, used_eye = eye, exclusions = exclusions))
        return res

class BigFourDirection(PointCombination):
    """ 大四喜 """
    def __init__(self):
        name = "大四喜"
        point = 90
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        isDirection = lambda t: t.tile_type == TileType.FAAN and t.tile_value <= 4

        used_melds = [meld for meld in melds if isDirection(meld.tiles[0])]

        if len(used_melds) == 4:
            exclusions = []
            for meld in used_melds:
                exclusions += get_position_character_exclusions(meld)

            res.append(self.score(used_melds = used_melds, exclusions = exclusions))
        return res

class AllCharacter(PointCombination):
    """ 字一色 """
    def __init__(self):
        name = "字一色"
        point = 120
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        if all(meld.tile_type == TileType.FAAN for meld in melds) and all(tile.tile_type == TileType.FAAN for tile in eye):
            exclusions = []
            for meld in melds:
                if meld.tile_type == TileType.FAAN and meld.tiles[0].tile_value <= 4:
                    exclusions += get_position_character_exclusions(meld)
                else:
                    exclusions.append(ScoredCombination(FaanCharacter(), used_melds = [meld]))

            res.append(self.score(exclusions = exclusions))
        return res

def get_character_combinations():
    yield NoCharacter()
    yield BadPositionCharacter()
    yield GoodPositionCharacter()
    yield GoodSeatCharacter()
    yield FaanCharacter()
    yield SmallThreeCharacter()
    yield BigThreeCharacter()
    yield SmallThreeDirection()
    yield BigThreeDirection()
    yield SmallFourDirection()
    yield BigFourDirection()
    yield AllCharacter()

def get_character_combinations_dict():
    """return a list of name, value, and remark for each class return in get_character_combinations"""
    for combination in get_character_combinations():
        yield combination.name, combination.point, combination.remark
