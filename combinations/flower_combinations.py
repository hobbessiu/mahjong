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

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if len(flowers) > 0:
            return []
        return [self.score()]

class RightFlower(PointCombination):
    """正花"""
    def __init__(self):
        name = "正花"
        point = 2
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        for flower in flowers:
            if flower.tile_value % 4 == seat:
                res.append(self.score(used_tiles = [flower]))
        return res

class WrongFlower(PointCombination):
    """爛花"""
    def __init__(self):
        name = "爛花"
        point = 1
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        for flower in flowers:
            if flower.tile_value % 4 != seat:
                res.append(self.score(used_tiles = [flower]))
        return res

class NoLetterAndFlower(PointCombination):
    """無字花"""
    def __init__(self):
        name = "無字花"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        if len(flowers) > 0:
            return []
        if any(meld.tile_type == TileType.FAAN for meld in melds) or eye[0].tile_type == TileType.FAAN:
            return []
        return [self.score(exclusions=[ScoredCombination(NoFlower())])]

class SetOfFlower(PointCombination):
    """一台花"""
    def __init__(self):
        name = "一台花"
        point = 10
        remark = "即收5番，食糊時計10番"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        flower_set_1 = [f for f in flowers if f.tile_value in [1, 2, 3, 4]]
        flower_set_2 = [f for f in flowers if f.tile_value in [5, 6, 7, 8]]
        if len(flower_set_1) == 4:
            exclusions_1 = []
            for f_1 in flower_set_1:
                if f_1.tile_value % 4 == seat:
                    exclusions_1.append(ScoredCombination(RightFlower(), used_tiles=[f_1]))
                else:
                    exclusions_1.append(ScoredCombination(WrongFlower(), used_tiles=[f_1]))

            res.append(self.score(used_tiles=flower_set_1, exclusions=exclusions_1))

        if len(flower_set_2) == 4:
            exclusions_2 = []
            for f_2 in flower_set_2:
                if f_1.tile_value % 4 == seat:
                    exclusions_2.append(ScoredCombination(RightFlower(), used_tiles=[f_2]))
                else:
                    exclusions_2.append(ScoredCombination(WrongFlower(), used_tiles=[f_2]))
            res.append(self.score(used_tiles=flower_set_2, exclusions=exclusions_2))
        return res

class SetOfGrass(PointCombination):
    """一台草"""
    def __init__(self):
        name = "一台草"
        point = 3
        remark = "即收3番"
        super().__init__(name, point, remark)
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        return []

def get_flower_combinations():
    yield NoFlower()
    yield RightFlower()
    yield WrongFlower()
    yield NoLetterAndFlower()
    yield SetOfFlower()
    yield SetOfGrass()

def get_flower_combinations_dict():
    for combination in get_flower_combinations():
        yield combination.name, combination.point, combination.remark