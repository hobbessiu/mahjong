"""叫胡牌型類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination
from calculate import split_to_groups

class ScroingInPong(PointCombination):
    """對碰"""
    def __init__(self):
        name = "對碰"
        point = 1
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        winning_pong = [m for m in melds if any(t.is_scoring_tile for t in m.tiles) and m.meld_type == MeldType.PONG]
        if len(winning_pong) == 0:
            return []
        return [self.score()]

class SelfScoring(PointCombination):
    """自摸"""
    def __init__(self):
        name = "自摸"
        point = 1
        super().__init__(name, point)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        all_tiles = [t for meld in melds for t in meld.tiles] + eye
        scoring_tile = [t for t in all_tiles if t.is_scoring_tile][0]
        if scoring_tile.is_open:
            return []
        return [self.score()]

class ScroingInSinglePossiblity(PointCombination):
    """獨獨"""
    def __init__(self):
        name = "獨獨"
        point = 2
        remark = "卡窿/單吊/偏章"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if any(t.is_scoring_tile for t in eye):
            return [self.score()]
        winning_chow = [m for m in melds if any(t.is_scoring_tile for t in m.tiles) and m.meld_type == MeldType.CHOW]
        if len(winning_chow) == 0:
            return []
        winning_chow = winning_chow[0]
        if winning_chow.tiles[1].is_scoring_tile:
            return [self.score()]
        return []

class ScroingInFakeSinglePossiblity(PointCombination):
    """假獨"""
    def __init__(self):
        name = "假獨"
        point = 1
        remark = "只要可砌成單吊即算假獨"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        scroingInSinglePossiblity = ScroingInSinglePossiblity().evaluate(melds, eye, flowers, position, seat)
        if len(scroingInSinglePossiblity) == 0:
            return []
        all_open_melds = [m for m in melds if all(t.is_open for t in m.tiles)]
        remaining_melds = [m for m in melds if any(not t.is_open for t in m.tiles)]
        remaining_tiles = [t for meld in remaining_melds for t in meld.tiles] + eye
        remaining_tiles = [t for t in remaining_tiles if not t.is_scoring_tile]

        possible_scoring_tiles = []

        all_tiles = ''.join(Tile.unicode_dict.values())
        for t in all_tiles:
            try:
                current_tile = Tile.from_unicode(t)
                current_tile.set_scoring_tile()
                res = split_to_groups(remaining_tiles + [current_tile], all_open_melds)
                if res and len(res) >= 1:
                    possible_scoring_tiles.append(current_tile)
            except:
                continue
        
        if len(possible_scoring_tiles) > 1:
            return [self.score(exclusions=[ScoredCombination(ScroingInSinglePossiblity())])]
        return []

class SpecialEye(PointCombination):
    """將眼"""
    def __init__(self):
        name = "將眼"
        point = 1
        remark = "2/5/8作眼"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if eye[0].tile_type == TileType.FAAN:
            return []
        if eye[0].tile_value in [2, 5, 8]:
            return [self.score()]
        return []

class AllFromSelf(PointCombination):
    """門清"""
    def __init__(self):
        name = "門清"
        point = 5
        super().__init__(name, point)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        all_tiles = [t for meld in melds for t in meld.tiles] + eye
        if any(t.is_open for t in all_tiles if not t.is_scoring_tile):
            return []
        return [self.score()]

class AllFromSelfAndSelfScoring(PointCombination):
    """門清一摸八"""
    def __init__(self):
        name = "門清一摸八"
        point = 8
        remark = "不需另計門清,如食糊牌型必為門清,計一摸三"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        all_tiles = [t for meld in melds for t in meld.tiles] + eye
        if any(t.is_open for t in all_tiles):
            return []
        return [self.score(exclusions=[ScoredCombination(AllFromSelf()), ScoredCombination(SelfScoring())])]

class AllFromSelfAndSelfScoringThree(PointCombination):
    """門清一摸三"""
    def __init__(self):
        name = "門清一摸三"
        point = 3
        remark = "不需另計門清,如食糊牌型必為門清,計一摸三"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        allFromSelfAndSelfScoring = AllFromSelfAndSelfScoring()
        if len(allFromSelfAndSelfScoring.evaluate(melds, eye, flowers, position, seat)) > 0:
            return [self.score(exclusions=[ScoredCombination(AllFromSelfAndSelfScoring())])]
        return []

class AllFromSelfAndDing(PointCombination):
    """門叮"""
    def __init__(self):
        name = "門叮"
        point = 5
        super().__init__(name, point)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if kwargs.get("is_ding", False) and len(AllFromSelf().evaluate(melds, eye, flowers, position, seat)) > 0:
            return [self.score()]

class Ding(PointCombination):
    """叮"""
    def __init__(self):
        name = "叮"
        point = 5
        super().__init__(name, point)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if kwargs.get("is_ding", False):
            return [self.score()]
        return []

class BaseScore(PointCombination):
    """底"""
    def __init__(self):
        name = "底"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        return [self.score()]

class ConsecutiveWin(PointCombination):
    """連莊"""
    def __init__(self, consecutive_win = 0):
        name = f"連{consecutive_win if consecutive_win > 0 else '莊'}"
        point = 2 * consecutive_win
        remark = "2n"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if not kwargs.get("scoring_dealer", False):
            return []
        consecutive_win = kwargs.get("consecutive_win", 0)
        if consecutive_win != 0:
            return [ConsecutiveWin(consecutive_win).score()]
        return []

class ScoreDealer(PointCombination):
    """莊/食莊"""
    def __init__(self):
        name = "莊/食莊"
        point = 1
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if kwargs.get("scoring_dealer", False):
            return [self.score()]
        return []

def get_scoring_combinations():
    yield ScroingInPong()
    yield SelfScoring()
    yield ScroingInSinglePossiblity()
    yield ScroingInFakeSinglePossiblity()
    yield SpecialEye()
    yield AllFromSelf()
    yield AllFromSelfAndSelfScoring()
    yield AllFromSelfAndDing()
    yield Ding()
    yield BaseScore()
    yield ConsecutiveWin()
    yield ScoreDealer()

def get_scoring_combinations_dict():
    for combination in get_scoring_combinations():
        yield combination.name, combination.point, combination.remark