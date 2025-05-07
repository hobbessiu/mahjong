"""刻槓類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination
from combinations.scoring_combinations import ScroingInPong, ScroingInSinglePossiblity, AllFromSelf, AllFromSelfAndSelfScoringThree
from combinations.one_colour_combinations import AllOneColour

class ClosedKong(PointCombination):
    """暗槓"""
    def __init__(self):
        name = "暗槓"
        point = 2
        remark = "即收5"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        closed_kong = [m for m in melds if m.meld_type == MeldType.KONG and not m.is_open]
        res = []
        for kong in closed_kong:
                res.append(self.score(used_melds=[kong]))
        return res

class OpenKong(PointCombination):
    """明槓"""
    def __init__(self):
        name = "明槓"
        point = 2
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        open_kong = [m for m in melds if m.meld_type == MeldType.KONG and m.is_open]
        res = []
        for kong in open_kong:
                res.append(self.score(used_melds=[kong]))
        return res

class AllPongKong(PointCombination):
    """對對胡"""
    def __init__(self):
        name = "對對胡"
        point = 30
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if any(not m.is_pong_or_kong() for m in melds):
            return []
        return [self.score()]

class TwoClosePong(PointCombination):
    """兩暗刻"""
    def __init__(self):
        name = "兩暗刻"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        close_pong_kong = [m for m in melds if m.is_pong_or_kong() and not m.is_open]
        if len(close_pong_kong) == 2:
            return [self.score(used_melds=close_pong_kong)]
        return []

class ThreeClosePong(PointCombination):
    """三暗刻"""
    def __init__(self):
        name = "三暗刻"
        point = 15
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        close_pong_kong = [m for m in melds if m.is_pong_or_kong() and not m.is_open]
        if len(close_pong_kong) == 3:
            return [self.score(used_melds=close_pong_kong)]
        return []
    
class FourClosePong(PointCombination):
    """四暗刻"""
    def __init__(self):
        name = "四暗刻"
        point = 30
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        close_pong_kong = [m for m in melds if m.is_pong_or_kong() and not m.is_open]
        if len(close_pong_kong) == 4:
            return [self.score(used_melds=close_pong_kong)]
        return []

class AllClosePong(PointCombination):
    """坎坎胡"""
    def __init__(self):
        name = "坎坎胡"
        point = 120
        remark = "不另計對對胡，打出只可單吊，自摸可叫兩飛，一律不另計單吊/對碰"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        close_pong_kong = [m for m in melds if m.is_pong_or_kong() and not m.is_open]
        res = []
        if len(close_pong_kong) == 5:
            res += [self.score(exclusions=[ScoredCombination(AllFromSelf()) ,ScoredCombination(AllPongKong()), ScoredCombination(ScroingInPong()), ScoredCombination(ScroingInSinglePossiblity())])]
        allFromSelfAndSelfScoringThree = AllFromSelfAndSelfScoringThree()
        res += allFromSelfAndSelfScoringThree.evaluate(melds, eye, flowers, position, seat, **kwargs)
        return res

class ThreeKong(PointCombination):
    """三槓子"""
    def __init__(self):
        name = "三槓子"
        point = 40
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        kongs = [m for m in melds if m.meld_type == MeldType.KONG]
        if len(kongs) == 3:
            return [self.score()]
        return []

class FourKong(PointCombination):
    """四槓子"""
    def __init__(self):
        name = "四槓子"
        point = 80
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        kongs = [m for m in melds if m.meld_type == MeldType.KONG]
        if len(kongs) == 4:
            return [self.score()]
        return []

class FiveKong(PointCombination):
    """五槓子"""
    def __init__(self):
        name = "五槓子"
        point = 200
        remark = "五槓子不另計對對胡，不另計單吊/槓"
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        kongs = [m for m in melds if m.meld_type == MeldType.KONG]
        if len(kongs) != 5:
            return []
        exclusions = [ScoredCombination(AllPongKong()), ScoredCombination(ScroingInPong()), ScoredCombination(ScroingInSinglePossiblity())]
        for kong in kongs:
            if kong.is_open:
                exclusions.append(ScoredCombination(OpenKong(used_melds=[kong])))
            else:
                exclusions.append(ScoredCombination(ClosedKong(used_melds=[kong])))
        return [self.score(exclusions=exclusions)]

class SmallTwoConsecutivePong(PointCombination):
    """小兩連刻"""
    def __init__(self):
        name = "小兩連刻"
        point = 5
        remark = "例：同色333 444"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        pong_kongs = [m for m in melds if m.is_pong_or_kong() and m.tile_type != TileType.FAAN]
        if len(pong_kongs) < 2:
            return []
        pong_kongs.sort(key=lambda x: x.tiles[0].tile_type.value)
        res = []
        for i in range(len(pong_kongs) - 1):
            if pong_kongs[i].tiles[0].tile_type == pong_kongs[i + 1].tiles[0].tile_type and pong_kongs[i].tiles[0].tile_value + 1 == pong_kongs[i + 1].tiles[0].tile_value:
                res.append(self.score(used_melds=[pong_kongs[i], pong_kongs[i + 1]]))
        return res

class BigTwoConsecutivePong(PointCombination):
    """大兩連刻"""
    def __init__(self):
        name = "大兩連刻"
        point = 10
        remark = "例：同色333 444 2或5作眼"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if eye[0].tile_type == TileType.FAAN:
            return []
        pong_kongs = [m for m in melds if m.is_pong_or_kong() and m.tile_type == eye[0].tile_type]
        if len(pong_kongs) < 2:
            return []
        res = []
        next_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 1]
        next_2_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 2]
        if len(next_pong) != 0 and len(next_2_pong) != 0:
            exclusions = [ScoredCombination(SmallTwoConsecutivePong(), used_melds=[next_pong[0], next_2_pong[0]])]
            res.append(self.score(used_melds=[next_pong[0], next_2_pong[0]], used_eye=eye, exclusions=exclusions))
        
        prev_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 1]
        prev_2_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 2]
        if len(prev_pong) != 0 and len(prev_2_pong) != 0:
            exclusions = [ScoredCombination(SmallTwoConsecutivePong(), used_melds=[prev_2_pong[0], prev_pong[0]])]
            res.append(self.score(used_melds=[prev_2_pong[0], prev_pong[0]], used_eye=eye, exclusions=exclusions))
        return res

class SmallThreeConsecutivePong(PointCombination):
    """小三連刻"""
    def __init__(self):
        name = "小三連刻"
        point = 20
        remark = "例：同色333 444 555"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        pong_kongs = [m for m in melds if m.is_pong_or_kong() and m.tile_type != TileType.FAAN]
        if len(pong_kongs) < 3:
            return []
        pong_kongs.sort(key=lambda x: x.tiles[0].tile_type.value)
        res = []
        for i in range(len(pong_kongs) - 2):
            if pong_kongs[i].tiles[0].tile_type == pong_kongs[i + 1].tiles[0].tile_type and pong_kongs[i + 1].tiles[0].tile_type == pong_kongs[i + 2].tiles[0].tile_type and \
                pong_kongs[i].tiles[0].tile_value + 1 == pong_kongs[i + 1].tiles[0].tile_value and pong_kongs[i + 1].tiles[0].tile_value + 1 == pong_kongs[i + 2].tiles[0].tile_value:
                exclusions = []
                exclusions.append(ScoredCombination(SmallTwoConsecutivePong(), used_melds=[pong_kongs[i], pong_kongs[i + 1]]))
                exclusions.append(ScoredCombination(SmallTwoConsecutivePong(), used_melds=[pong_kongs[i + 1], pong_kongs[i + 2]]))
                res.append(self.score(used_melds=[pong_kongs[i], pong_kongs[i + 1], pong_kongs[i + 2]], exclusions=exclusions))
        return res

class BigThreeConsecutivePong(PointCombination):
    """大三連刻"""
    def __init__(self):
        name = "大三連刻"
        point = 40
        remark = "例：同色333 444 555 2或6作眼"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if eye[0].tile_type == TileType.FAAN:
            return []
        pong_kongs = [m for m in melds if m.is_pong_or_kong() and m.tile_type == eye[0].tile_type]
        if len(pong_kongs) < 3:
            return []
        res = []
        next_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 1]
        next_2_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 2]
        next_3_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 3]

        if len(next_pong) != 0 and len(next_2_pong) != 0 and len(next_3_pong) != 0:
            exclusions = []
            exclusions.append(ScoredCombination(BigTwoConsecutivePong(), used_melds=[next_pong[0], next_2_pong[0]], used_eye=eye))
            exclusions.append(ScoredCombination(SmallThreeConsecutivePong(), used_melds=[next_pong[0], next_2_pong[0], next_3_pong[0]]))
            res.append(self.score(used_melds=[next_pong[0], next_2_pong[0], next_3_pong[0]], used_eye=eye, exclusions=exclusions))
        
        prev_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 1]
        prev_2_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 2]
        prev_3_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 3]

        if len(prev_pong) != 0 and len(prev_2_pong) != 0 and len(prev_3_pong) != 0:
            exclusions = []
            exclusions.append(ScoredCombination(BigTwoConsecutivePong(), used_melds=[prev_2_pong[0], prev_pong[0]], used_eye=eye))
            exclusions.append(ScoredCombination(SmallThreeConsecutivePong(), used_melds=[prev_3_pong[0], prev_2_pong[0], prev_pong[0]]))
            res.append(self.score(used_melds=[prev_3_pong[0], prev_2_pong[0], prev_pong[0]], used_eye=eye, exclusions=exclusions))
        return res

class SmallFourConsecutivePong(PointCombination):
    """小四連刻"""
    def __init__(self):
        name = "小四連刻"
        point = 60
        remark = "例：同色333 444 555 666"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        pong_kongs = [m for m in melds if m.is_pong_or_kong() and m.tile_type != TileType.FAAN]
        if len(pong_kongs) < 4:
            return []
        pong_kongs.sort(key=lambda x: x.tiles[0].tile_type.value)
        res = []
        for i in range(len(pong_kongs) - 3):
            if pong_kongs[i].tiles[0].tile_type == pong_kongs[i + 1].tiles[0].tile_type and pong_kongs[i + 1].tiles[0].tile_type == pong_kongs[i + 2].tiles[0].tile_type and \
                pong_kongs[i + 2].tiles[0].tile_type == pong_kongs[i + 3].tiles[0].tile_type and \
                pong_kongs[i].tiles[0].tile_value + 1 == pong_kongs[i + 1].tiles[0].tile_value and pong_kongs[i + 1].tiles[0].tile_value + 1 == pong_kongs[i + 2].tiles[0].tile_value and \
                pong_kongs[i + 2].tiles[0].tile_value + 1 == pong_kongs[i + 3].tiles[0].tile_value:
                exclusions = []
                exclusions.append(ScoredCombination(SmallThreeConsecutivePong(), used_melds=[pong_kongs[i], pong_kongs[i + 1], pong_kongs[i + 2]]))
                exclusions.append(ScoredCombination(SmallThreeConsecutivePong(), used_melds=[pong_kongs[i + 1], pong_kongs[i + 2], pong_kongs[i + 3]]))
                res.append(self.score(used_melds=[pong_kongs[i], pong_kongs[i + 1], pong_kongs[i + 2], pong_kongs[i + 3]], exclusions=exclusions))
        return res

class BigFourConsecutivePong(PointCombination):
    """大四連刻"""
    def __init__(self):
        name = "大四連刻"
        point = 90
        remark = "例：同色333 444 555 666 2或7作眼"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if eye[0].tile_type == TileType.FAAN:
            return []
        pong_kongs = [m for m in melds if m.is_pong_or_kong() and m.tile_type == eye[0].tile_type]
        if len(pong_kongs) < 4:
            return []
        res = []
        next_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 1]
        next_2_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 2]
        next_3_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 3]
        next_4_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value + 4]

        if len(next_pong) != 0 and len(next_2_pong) != 0 and len(next_3_pong) != 0 and len(next_4_pong) != 0:
            exclusions = []
            exclusions.append(ScoredCombination(BigThreeConsecutivePong(), used_melds=[next_pong[0], next_2_pong[0], next_3_pong[0]], used_eye=eye))
            exclusions.append(ScoredCombination(SmallFourConsecutivePong(), used_melds=[next_pong[0], next_2_pong[0], next_3_pong[0], next_4_pong[0]]))
            res.append(self.score(used_melds=[next_pong[0], next_2_pong[0], next_3_pong[0], next_4_pong[0]], used_eye=eye, exclusions=exclusions))
        
        prev_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 1]
        prev_2_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 2]
        prev_3_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 3]
        prev_4_pong = [p for p in pong_kongs if p.tiles[0].tile_value == eye[0].tile_value - 4]

        if len(prev_pong) != 0 and len(prev_2_pong) != 0 and len(prev_3_pong) != 0 and len(prev_4_pong) != 0:
            exclusions = []
            exclusions.append(ScoredCombination(BigThreeConsecutivePong(), used_melds=[prev_3_pong[0], prev_2_pong[0], prev_pong[0]], used_eye=eye))
            exclusions.append(ScoredCombination(SmallFourConsecutivePong(), used_melds=[prev_4_pong[0], prev_3_pong[0], prev_2_pong[0], prev_pong[0]]))
            res.append(self.score(exclusions=exclusions))
        
        return res

class SmallFiveConsecutivePong(PointCombination):
    """小五連刻"""
    def __init__(self):
        name = "小五連刻"
        point = 120
        remark = "不另計對對胡, 例：同色333 444 555 666 777"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        pong_kongs = [m for m in melds if m.is_pong_or_kong() and m.tile_type != TileType.FAAN]
        pong_kongs.sort(key=lambda x: x.tiles[0].tile_value)
        if len(pong_kongs) < 5:
            return []
        if any(p for p in pong_kongs if p.tile_type != pong_kongs[0].tile_type):
            return []
        pong_values = [p.tiles[0].tile_value for p in pong_kongs]
        pong_values_diff = [j-i for i, j in zip(pong_values[:-1], pong_values[1:])]
        if any(diff != 1 for diff in pong_values_diff):
            return []
        exclusions = []
        exclusions.append(ScoredCombination(AllPongKong()))
        exclusions.append(ScoredCombination(SmallFourConsecutivePong(), used_melds=pong_kongs[:-1]))
        exclusions.append(ScoredCombination(SmallFourConsecutivePong(), used_melds=pong_kongs[1:]))
        return [self.score(exclusions=exclusions)]

class BigFiveConsecutivePong(PointCombination):
    """大五連刻"""
    def __init__(self):
        name = "大五連刻"
        point = 240
        remark = "不另計清一色/對對胡 例：同色333 444 555 666 777 2或8作眼"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if eye[0].tile_type == TileType.FAAN:
            return []
        pong_kongs = [m for m in melds if m.is_pong_or_kong() and m.tile_type == eye[0].tile_type]
        if len(pong_kongs) < 5:
            return []
        res = []
        pong_values = sorted([p.tiles[0].tile_value for p in pong_kongs])
        pong_values_diff = [j-i for i, j in zip(pong_values[:-1], pong_values[1:])]
        if any(diff != 1 for diff in pong_values_diff):
            return []
        if (eye[0].tile_value == pong_values[0] - 1 or eye[0].tile_value == pong_values[-1] + 1):
            exclusions = []
            exclusions.append(ScoredCombination(AllPongKong()))
            exclusions.append(ScoredCombination(AllOneColour()))
            exclusions.append(ScoredCombination(SmallFiveConsecutivePong()))
            return [self.score(exclusions=exclusions)]
        return []

def get_pong_kong_combinations():
    yield ClosedKong()
    yield OpenKong()
    yield AllPongKong()
    yield TwoClosePong()
    yield ThreeClosePong()
    yield FourClosePong()
    yield AllClosePong()
    yield ThreeKong()
    yield FourKong()
    yield FiveKong()
    yield SmallTwoConsecutivePong()
    yield BigTwoConsecutivePong()
    yield SmallThreeConsecutivePong()
    yield BigThreeConsecutivePong()
    yield SmallFourConsecutivePong()
    yield BigFourConsecutivePong()
    yield SmallFiveConsecutivePong()
    yield BigFiveConsecutivePong()