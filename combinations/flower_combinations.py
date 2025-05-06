"""花牌類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination

class NoFlower(PointCombination):
    """無花"""
    def __init__(self):
        name = "無花"
        point = 1
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        if len(flowers) > 0:
            return []
        return [self.score()]

class RightFlower(PointCombination):
    """正花"""
    def __init__(self):
        name = "正花"
        point = 2
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        res = []
        for flower in flowers:
            if flower.tile_value % 4 == position:
                res.append(self.score(used_tiles = [flower]))
        return res

class WrongFlower(PointCombination):
    """爛花"""
    def __init__(self):
        name = "爛花"
        point = 1
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        res = []
        for flower in flowers:
            if flower.tile_value % 4 != position:
                res.append(self.score(used_tiles = [flower]))
        return res

class NoLetterAndFlower(PointCombination):
    """無字花"""
    def __init__(self):
        name = "無字花"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position):
        res = []
        if len(flowers) > 0:
            return []
        if any(meld.tile_type == TileType.FAAN for meld in melds) or eye[0].tile_type == TileType.FAAN:
            return []
        return [self.score(exclusions=[ScoredCombination(NoFlower())])]

def get_flower_combinations():
    yield NoFlower()
    yield RightFlower()
    yield WrongFlower()
    yield NoLetterAndFlower()