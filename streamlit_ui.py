import streamlit as st
from calculate_point import calculate
from combinations.character_combinations import get_character_combinations_dict
from tiles import *
from meld import Meld

st.set_page_config(page_title="麻雀計番器", page_icon="🀄")
st.title('麻雀計番器')


if 'is_score_from_other' not in st.session_state:
    st.session_state.is_score_from_other = False
if 'is_self_score' not in st.session_state:
    st.session_state.is_self_score = False
if 'is_chow' not in st.session_state:
    st.session_state.is_chow = False
if 'is_pong' not in st.session_state:
    st.session_state.is_pong = False
if 'is_open_kong' not in st.session_state:
    st.session_state.is_open_kong = False
if 'is_close_kong' not in st.session_state:
    st.session_state.is_close_kong = False
if 'hand' not in st.session_state:
    st.session_state.hand = []
if 'open_melds' not in st.session_state:
    st.session_state.open_melds = []
if 'result' not in st.session_state:
    st.session_state.result = []
if 'input_queue' not in st.session_state:
    st.session_state.input_queue = []
if 'position' not in st.session_state:
    st.session_state.position = 1

st.session_state['all_tiles'] = st.session_state.hand + [tile for meld in st.session_state.open_melds for tile in meld.tiles]

def tile_to_html(tile: Tile):
    button_style = "background-color: black; color: white;" if not (tile.is_open or tile.tile_type == TileType.FLOWER) else "background-color: white; color: black;"
    return f'<div style="{button_style} font-size: 40px; height: 40px; {"transform: rotate(90deg);" if tile.is_scoring_tile else ""} display: flex; justify-content: center; align-items: center; border: 1px solid #ccc; border-radius: 5px; text-align: center;">{tile.to_unicode()}</div>'

def hand_to_html(tiles: list[Tile], open_melds: list[Meld]):
    close_hand =  ''.join([tile_to_html(tile) for tile in tiles if not tile.is_open and not tile.is_scoring_tile and not tile.tile_type == TileType.FLOWER])
    open_melds_tiles = ''.join([tile_to_html(tile) for meld in open_melds for tile in meld.tiles])
    flower_hand =  ''.join([tile_to_html(tile) for tile in tiles if tile.tile_type == TileType.FLOWER])
    scoring_tile = ''.join([tile_to_html(tile) for tile in tiles if tile.is_scoring_tile])
    return f"""<div style='display: flex; flex-wrap: wrap;'>{close_hand}</div>
            <div style='display: flex; flex-wrap: wrap;'>{open_melds_tiles}</div>
            <div style='display: flex; flex-wrap: wrap;'>{flower_hand}</div>
            <div style='display: flex; flex-wrap: wrap;'>{scoring_tile}</div>
    """

def update_buttons_state(button_str):
    current = st.session_state[button_str]
    st.session_state.is_score_from_other = False
    st.session_state.is_self_score = False
    st.session_state.is_chow = False
    st.session_state.is_pong = False
    st.session_state.is_open_kong = False
    st.session_state.is_close_kong = False
    st.session_state[button_str] = not current


def click_tile_button(tile_str):
    if len([t for t in st.session_state['all_tiles'] if t == Tile.from_unicode(tile_str)]) >= (4 if tile_str not in Tile.unicode_dict[TileType.FLOWER] else 1):
        st.error(f"{str(Tile.from_unicode(tile_str))} 已有{4 if tile_str not in Tile.unicode_dict[TileType.FLOWER] else 1}張，無法再加入！")
        return

    if tile_str not in Tile.unicode_dict[TileType.FLOWER]:
        if len(st.session_state['hand']) + 3 * len(st.session_state['open_melds']) >= 17:
            st.error("手牌已滿，無法再加入！")
            return

    if any([t for t in st.session_state['all_tiles'] if t.is_scoring_tile]) and (st.session_state.is_self_score or st.session_state.is_score_from_other):
        st.error("已經有胡牌，無法再加入！")
        st.session_state.is_self_score = False
        st.session_state.is_score_from_other = False
        return
    
    t = Tile.from_unicode(tile_str)
    if st.session_state.is_chow:
        if len(st.session_state['hand']) + 3 * len(st.session_state['open_melds']) > 14:
            st.error("手牌已滿，無法再加入！")
            return
        if not t.next_tile() or not t.next_tile().next_tile():
            st.error("呢隻上唔到！")
            return
        if len([at for at in st.session_state['all_tiles'] if at == t.next_tile()]) >= 4:
            st.error(f"{str(t.next_tile())} 已有4張，無法再加入！")
            return
        if len([at for at in st.session_state['all_tiles'] if at == t.next_tile().next_tile()]) >= 4:
            st.error(f"{str(t.next_tile().next_tile())} 已有4張，無法再加入！")
            return
        t.set_open()
        tiles_to_add = [t, t.next_tile(), t.next_tile().next_tile()]
        meld = Meld(tiles_to_add)
        st.session_state.open_melds.append(meld)
        st.session_state.is_chow = False
        st.session_state.input_queue.append('open_melds')
        return
    elif st.session_state.is_pong:
        if len(st.session_state['hand']) + 3 * len(st.session_state['open_melds']) > 14:
            st.error("手牌已滿，無法再加入！")
            return
        t.set_open()
        current_tiles_count = len([at for at in st.session_state['all_tiles'] if at == t])
        if current_tiles_count > 1:
            st.error(f"{str(t)} 已有{current_tiles_count}張，呢隻碰唔到！")
            return
        tiles_to_add = [t, t, t]
        meld = Meld(tiles_to_add)
        st.session_state.open_melds.append(meld)
        st.session_state.is_pong = False
        st.session_state.input_queue.append('open_melds')
        return
    elif st.session_state.is_open_kong or st.session_state.is_close_kong:
        if len(st.session_state['hand']) + 3 * len(st.session_state['open_melds']) > 14:
            st.error("手牌已滿，無法再加入！")
            return
        if st.session_state.is_open_kong:
            t.set_open()
        current_tiles_count = len([at for at in st.session_state['all_tiles'] if at == t])
        if current_tiles_count > 0:
            st.error(f"已有{str(t)}，呢隻杠唔到！")
            return
        tiles_to_add = [t, t, t, t]
        meld = Meld(tiles_to_add)
        st.session_state.open_melds.append(meld)
        st.session_state.is_open_kong = False
        st.session_state.is_close_kong = False
        st.session_state.input_queue.append('open_melds')
        return
    elif st.session_state.is_self_score:
        t.set_scoring_tile()
        t.is_open = False
        st.session_state.is_self_score = False
    elif st.session_state.is_score_from_other:
        t.set_scoring_tile()
        t.is_open = True
        st.session_state.is_score_from_other = False

    st.session_state['hand'].append(t)
    st.session_state.input_queue.append('hand')

def backspace():
    st.session_state.result = ''
    if st.session_state['input_queue']:
        last_input = st.session_state['input_queue'].pop()
        st.session_state[last_input].pop()

def create_tile_button(c, tile_type: TileType, tile_value: int):
    label = f"$ \\large {Tile.unicode_dict[tile_type][tile_value]} $"
    c.button(label, on_click=click_tile_button, args=Tile.unicode_dict[tile_type][tile_value], help=str(Tile.from_unicode(Tile.unicode_dict[tile_type][tile_value])))

def on_calculate_click():
    try:
        check_count = len(st.session_state['hand']) + 3 * len(st.session_state['open_melds'])
        if check_count != 17:
            st.error(f"未夠牌，差{17 - check_count}張！")
            return
        if not any([t for t in st.session_state['hand'] if t.is_scoring_tile]):
            st.error("食邊隻？")
            return

        result = calculate(st.session_state['hand'], st.session_state['open_melds'], st.session_state['position'])
        st.session_state['result'] = result
        st.write(f"計算結果: {sum([r.point_combination.point for r in result])} 番")
        for r in result:
            st.write(r)
    except Exception as e:
        st.error(f"計算錯誤: {e}")

def print_all_character_combinations():

    for name, point, remark in get_character_combinations_dict():
        explain_cols[0].write(f'{name}{'' if remark is None else f" ({remark})"}')
        explain_cols[1].write(point)

st.button('東南西北'[st.session_state['position']-1] + '圈', on_click=lambda: st.session_state.update(position=(st.session_state['position'] % 4) + 1))
option_button_cols = st.columns(6)
option_button_cols[0].button(':red[自摸]' if st.session_state['is_self_score'] else '自摸', on_click=lambda: st.session_state.update(is_self_score= not st.session_state['is_self_score'], is_score_from_other = False))
option_button_cols[1].button(':red[食出]' if st.session_state['is_score_from_other'] else '食出', on_click=lambda: st.session_state.update(is_score_from_other= not st.session_state['is_score_from_other'], is_self_score = False))
option_button_cols[2].button(':red[上]' if st.session_state['is_chow'] else '上', on_click=update_buttons_state, args=['is_chow'])
option_button_cols[3].button(':red[碰]' if st.session_state['is_pong'] else '碰', on_click=update_buttons_state, args=['is_pong'])
option_button_cols[4].button(':red[明槓]' if st.session_state['is_open_kong'] else '明槓', on_click=update_buttons_state, args=['is_open_kong'])
option_button_cols[5].button(':red[暗槓]' if st.session_state['is_close_kong'] else '暗槓', on_click=update_buttons_state, args=['is_close_kong'])

st.write('''
    <style>
    [data-testid="stColumn"] {
        width: 6vw; /* Fixed width based on proportions */
        min-width: 6vw; /* Prevent shrinking below this width */
    }
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important; /* Prevent wrapping of columns */
    }
    body {
        overflow-x: auto !important; /* Allow horizontal scrolling if needed */
    }
    </style>
    ''', unsafe_allow_html=True)

cols = st.columns(9)
for i, c in enumerate(cols):
    create_tile_button(c, TileType.TUNG, i)
    create_tile_button(c, TileType.SOK, i)
    create_tile_button(c, TileType.MAAN, i)

    if i < 7:
        create_tile_button(c, TileType.FAAN, i)
    if i < 4:
        create_tile_button(c, TileType.FLOWER, i)
        create_tile_button(c, TileType.FLOWER, i+4)

st.markdown(
    hand_to_html(st.session_state['hand'], st.session_state['open_melds']),
    unsafe_allow_html=True
)

button_col = st.columns(3)
calculate_click = button_col[0].button('計算')
button_col[1].button('清除', on_click=lambda: st.session_state.update(hand=[], open_melds=[], result=''))
button_col[2].button('⌫', on_click=backspace)
st.button('字牌類', on_click=print_all_character_combinations)

if calculate_click:
    on_calculate_click()

explain_cols = st.columns(2)
