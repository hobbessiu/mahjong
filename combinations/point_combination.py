from typing import Callable
from tiles import Tile, TileType
from meld import Meld, MeldType

class PointCombination:
    def __init__(self, name: str, point: float, remark = None):
        self.point = point
        self.name = name
        self.remark = remark

    def __eq__(self, value):
        if isinstance(value, PointCombination):
            return self.name == value.name and self.point == value.point
        return False
    
    def __repr__(self):
        res =  f"{self.name}: {self.point}"
        if self.remark:
            res += f" ({self.remark})"
        return res

    def score(self, used_melds: list[Meld] = None, used_eye: list[Tile] = None, exclusions = None, used_tiles: list[Tile] = None) -> 'ScoredCombination':
        return ScoredCombination(self, used_melds, used_eye, exclusions, used_tiles)
    
    def evaluate(self, melds: list[Meld], eye: list[Tile], flowers: list[Tile], position: int, seat: int, **kwargs) -> list['ScoredCombination']:
        NotImplementedError(self.__class__.__name__ + " must implement evaluate method.")

class ScoredCombination():
    def __init__(self, point_combination: PointCombination, used_melds: list[Meld] = None, used_eye: list[Tile] = None, exclusions: list['ScoredCombination'] = None, used_tiles: list[Tile] = None):
        self.point_combination = point_combination
        self.used_melds = used_melds
        self.used_eye = used_eye
        self.used_tiles = used_tiles
        self.exclusions = exclusions if exclusions else []
    
    def __eq__(self, value):
        if isinstance(value, ScoredCombination):
            return self.point_combination == value.point_combination and \
                self.used_melds == value.used_melds and self.used_eye == value.used_eye and \
                self.used_tiles == value.used_tiles
        return False
    
    def __repr__(self):
        res = f"{self.point_combination.__repr__()}"
        if self.used_melds:
            res += f" {self.used_melds}"
        if self.used_eye:
            res += f" {self.used_eye}"
        if self.used_tiles:
            res += f" {self.used_tiles}"
        return res