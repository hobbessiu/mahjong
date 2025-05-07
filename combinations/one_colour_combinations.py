"""一色類"""
from tiles import Tile, TileType
from meld import Meld, MeldType
from combinations.point_combination import PointCombination, ScoredCombination
from collections import Counter

class FourInOne(PointCombination):
    """四歸一"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}四歸一"
        point = 5 if is_open else 10
        remark = "5/10"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        pongs = [meld for meld in melds if meld.is_pong_or_kong() and meld.tile_type != TileType.FAAN]
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(pongs) == 0 or len(chows) == 0:
            return []
        for pong in pongs:
            chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
            for chow in chows:
                if pong.tiles[0] in chow.tiles:
                    used_melds = [pong, chow]
                    is_open = any(meld.is_open for meld in used_melds)
                    res.append(FourInOne(is_open).score(used_melds = [pong, chow]))
        
        return res
                
class FourInTwo(PointCombination):
    """四歸二"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}四歸二"
        point = 10 if is_open else 20
        remark = "10/20"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if eye[0].tile_type == TileType.FAAN:
            return []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) == 0:
            return []
        
        used_melds = []
        for chow in chows:
            if eye[0] in chow.tiles:
                used_melds.append(chow)
        
        if len(used_melds) == 2:
            is_open = any(meld.is_open for meld in used_melds)
            return [FourInTwo(is_open).score(used_melds = used_melds, used_eye= eye)]
        
        return []

class FourInFour(PointCombination):
    """四歸四"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}四歸四"
        point = 30 if is_open else 60
        remark = "30/60"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 4:
            return []
        
        res = []
        chow_tiles = [t for chow in chows for t in chow.tiles]
        chow_tiles_count = Counter(chow_tiles)
        for tile, count in chow_tiles_count.items():
            if count == 4:
                used_melds = [chow for chow in chows if tile in chow.tiles]
                is_open = any(meld.is_open for meld in used_melds)
                res.append(FourInFour(is_open).score(used_melds = used_melds))
        return res

class EightConsecutivePairs(PointCombination):
    """八連對"""
    def __init__(self):
        name = "八連對"
        point = 150
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if any(meld.tile_type == TileType.FAAN or meld.tile_type != melds[0].tile_type for meld in melds):
            return []
        tiles = [t for meld in melds for t in meld.tiles] + eye
        if any(t for t in tiles if t.is_open and not t.is_scoring_tile):
            return []
        tiles_count = Counter(tiles)
        if len(tiles_count) != 8:
            return []
        if any(count not in [2, 3]  for count in tiles_count.values()):
            return []
        tile_values = sorted([t.tile_value for t in tiles_count.keys()])
        value_diff = [j-i for i, j in zip(tile_values[:-1], tile_values[1:])]
        if any(diff != 1 for diff in value_diff):
            return []
        return [self.score()]
        
class SameTypeNeibourhood(PointCombination):
    """般高"""
    def __init__(self):
        name = "般高"
        point = 5
        super().__init__(name, point)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 2:
            return res
        for i in range(len(chows) - 1):
            for j in range(i + 1, len(chows)):
                if chows[i].tiles[0].tile_value == chows[j].tiles[0].tile_value and chows[i].tiles[0].tile_type == chows[j].tiles[0].tile_type:
                    res.append(self.score(used_melds = [chows[i], chows[j]]))
        return res

class SmallTwoNeibourhood(PointCombination):
    """小雙般高"""
    def __init__(self):
        name = "小雙般高"
        point = 10
        remark = "例：11223344"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        if eye[0].tile_type == TileType.FAAN:
            return []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW and meld.tile_type == eye[0].tile_type]
        if len(chows) < 2:
            return []
        res = []
        smaller_chows = [chow for chow in chows if chow.tiles[2].tile_value == eye[0].tile_value - 1]
        if len(smaller_chows) == 2:
            used_tiles = sorted(eye + [t for chow in smaller_chows for t in chow.tiles])
            exclusions = [ScoredCombination(SameTypeNeibourhood(), used_melds = smaller_chows)]
            res.append(self.score(used_tiles=used_tiles, exclusions=exclusions))
        
        larger_chows = [chow for chow in chows if chow.tiles[0].tile_value == eye[0].tile_value + 1]
        if len(larger_chows) == 2:
            used_tiles = sorted(eye + [t for chow in larger_chows for t in chow.tiles])
            exclusions = [ScoredCombination(SameTypeNeibourhood(), used_melds = larger_chows)]
            res.append(self.score(used_tiles=used_tiles, exclusions=exclusions))
        
        return res

class BigTwoNeibourhood(PointCombination):
    """大雙般高"""
    def __init__(self):
        name = "大雙般高"
        point = 20
        remark = "例：112233 667788"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        neibourhoods = SameTypeNeibourhood().evaluate(melds, eye, flowers, position, seat)
        if len(neibourhoods) < 2:
            return []
        res = []
        for i in range(len(neibourhoods) - 1):
            for j in range(i + 1, len(neibourhoods)):
                if neibourhoods[i].used_melds[0].tiles[0].tile_value != neibourhoods[j].used_melds[0].tiles[0].tile_value \
                    and neibourhoods[i].used_melds[0].tiles[0].tile_type == neibourhoods[j].used_melds[0].tiles[0].tile_type:
                    used_melds = neibourhoods[i].used_melds + neibourhoods[j].used_melds
                    res.append(self.score(used_melds=used_melds, exclusions=[neibourhoods[i], neibourhoods[j]]))

        return res

class SuperNeibourhood(PointCombination):
    """超般高"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}超般高"
        point = 20 if is_open else 40
        remark = "20/40"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 3:
            return []
        for chow in chows:
            current_chows = [c for c in chows if c == chow]
            if len(current_chows) == 3:
                used_melds = current_chows
                is_open = any(meld.is_open for meld in used_melds)
                exclusions =[]
                exclusions.append(ScoredCombination(SameTypeNeibourhood(), used_melds = used_melds[0:2]))
                exclusions.append(ScoredCombination(SameTypeNeibourhood(), used_melds = used_melds[0:2]))
                exclusions.append(ScoredCombination(SameTypeNeibourhood(), used_melds = used_melds[0:2]))
                return [SuperNeibourhood(is_open).score(used_melds = used_melds, exclusions = exclusions)]

class GrandNeibourhood(PointCombination):
    """太般高"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}太般高"
        point = 40 if is_open else 80
        remark = "40/80"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 4:
            return []
        for chow in chows:
            current_chows = [c for c in chows if c == chow]
            if len(current_chows) == 4:
                used_melds = current_chows
                is_open = any(meld.is_open for meld in used_melds)
                exclusions =[]
                exclusions.append(ScoredCombination(SameTypeNeibourhood(), used_melds = used_melds[0:2]))
                exclusions.append(ScoredCombination(SameTypeNeibourhood(), used_melds = used_melds[0:2]))
                exclusions.append(ScoredCombination(SameTypeNeibourhood(), used_melds = used_melds[0:2]))
                exclusions.append(ScoredCombination(SameTypeNeibourhood(), used_melds = used_melds[0:2]))
                return [GrandNeibourhood(is_open).score(used_melds = used_melds, exclusions = exclusions)]

class SameColourStepUp(PointCombination):
    """清步步高"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}清步步高"
        point = 10 if is_open else 20
        remark = "10/20"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 3:
            return []
        chows.sort(key=lambda x: x.tiles[0].tile_value)
        for chow in chows:
            next_chows = [c for c in chows if c.tiles[0].tile_value == chow.tiles[0].tile_value + 1 and c.tiles[0].tile_type == chow.tiles[0].tile_type]
            for next_chow in next_chows:
                next_next_chows = [c for c in chows if c.tiles[0].tile_value == next_chow.tiles[0].tile_value + 1 and c.tiles[0].tile_type == next_chow.tiles[0].tile_type]
                for next_next_chow in next_next_chows:
                    used_melds = [chow, next_chow, next_next_chow]
                    is_open = any(meld.is_open for meld in used_melds)
                    res.append(SameColourStepUp(is_open=is_open).score(used_melds = used_melds))
        
        return res

class SameColourTwoStepUp(PointCombination):
    """清二步高"""
    def __init__(self, is_open = True):
        name = f"{'明' if is_open else '暗'}清二步高"
        point = 10 if is_open else 20
        remark = "10/20"
        super().__init__(name, point, remark)

    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        res = []
        chows = [meld for meld in melds if meld.meld_type == MeldType.CHOW]
        if len(chows) < 3:
            return []
        chows.sort(key=lambda x: x.tiles[0].tile_value)
        for chow in chows:
            next_chows = [c for c in chows if c.tiles[0].tile_value == chow.tiles[0].tile_value + 2 and c.tiles[0].tile_type == chow.tiles[0].tile_type]
            for next_chow in next_chows:
                next_next_chows = [c for c in chows if c.tiles[0].tile_value == next_chow.tiles[0].tile_value + 2 and c.tiles[0].tile_type == next_chow.tiles[0].tile_type]
                for next_next_chow in next_next_chows:
                    used_melds = [chow, next_chow, next_next_chow]
                    is_open = any(meld.is_open for meld in used_melds)
                    res.append(SameColourTwoStepUp(is_open=is_open).score(used_melds = used_melds))
        return res

class MixedOneColour(PointCombination):
    """混一色"""
    def __init__(self):
        name = "混一色"
        point = 30
        super().__init__(name, point)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        tiles = [t for meld in melds for t in meld.tiles] + eye
        tiles_exclude_faan = [t for t in tiles if t.tile_type != TileType.FAAN]
        tile_types = set(t.tile_type for t in tiles_exclude_faan)
        if len(tile_types) == 1 and any(t for t in tiles if t.tile_type == TileType.FAAN):
            return [self.score()]

class AllOneColour(PointCombination):
    """清一色"""
    def __init__(self):
        name = "清一色"
        point = 80
        super().__init__(name, point)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        tiles = [t for meld in melds for t in meld.tiles] + eye
        tile_types = set(t.tile_type for t in tiles)
        if len(tile_types) == 1 and not TileType.FAAN in tile_types:
            return [self.score()]

class AllGreen(PointCombination):
    """綠一色"""
    def __init__(self):
        name = "綠一色"
        point = 30
        remark = "另計清一色/混一色/嚦咕/對對"
        super().__init__(name, point, remark)
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        tiles = [t for meld in melds for t in meld.tiles] + eye
        green_tiles_str = ['2s', '3s', '4s', '6s', '8s', '6x']
        green_tiles = [Tile.from_string(t) for t in green_tiles_str]
        if any(t for t in tiles if t not in green_tiles):
            return []
        return [self.score()]

class NineGate(PointCombination):
    """九蓮寶燈"""
    def __init__(self, is_authentic = False):
        name = f"{"純正" if is_authentic else ""}九蓮寶燈"
        point = 60 if is_authentic else 50
        super().__init__(name, point)
    
    def examine_nine_gate( matching_melds, eye):
        is_authentic = False
        nine_gates = [1,1,1,2,3,4,5,6,7,8,9,9,9]
        nine_gate_checks = Counter(nine_gates)
        tiles = [t for meld in matching_melds for t in meld.tiles] + eye
        tile_values = [t.tile_value for t in tiles]
        tiles_count = Counter(tile_values)
        if len(tiles_count.keys()) != 9:
            return []
        for tile_value, count in tiles_count.items():
            if count < nine_gate_checks[tile_value]:
                return []
            if count == nine_gate_checks[tile_value]:
                is_authentic = not any(t for t in tiles if t.is_scoring_tile and t.tile_value == tile_value)
        return [NineGate(is_authentic).score()]
    
    def evaluate(self, melds, eye, flowers, position, seat, **kwargs):
        
        if eye[0].tile_type == TileType.FAAN:
            return []
        
        matching_melds = [m for m in melds if m.tile_type == eye[0].tile_type and (not m.is_open or any(t for t in m.tiles if t.is_scoring_tile))]
        
        if len(matching_melds) < 4:
            return []
        if len(matching_melds) == 4:
            return NineGate.examine_nine_gate(matching_melds, eye)
        if len(matching_melds) == 5:
            res = []
            for meld_to_exclude in melds:
                melds_to_examine = matching_melds.copy()
                melds_to_examine.remove(meld_to_exclude)
                res += NineGate.examine_nine_gate(melds_to_examine, eye)
            if len(res) == 0:
                return []
            res.sort(key=lambda x: x.point_combination.point, reverse=True)
            return [res[0]]

        return []
        

def get_one_colour_combinations():
    yield SameTypeNeibourhood()
    yield FourInOne()
    yield FourInTwo()
    yield FourInFour()
    yield EightConsecutivePairs()
    yield SmallTwoNeibourhood()
    yield BigTwoNeibourhood()
    yield SuperNeibourhood()
    yield GrandNeibourhood()
    yield SameColourStepUp()
    yield SameColourTwoStepUp()
    yield MixedOneColour()
    yield AllOneColour()
    yield AllGreen()
    yield NineGate()
