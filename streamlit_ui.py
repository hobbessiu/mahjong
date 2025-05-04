import streamlit as st
from calculate_point import calculate
from combinations.character_combinations import get_character_combinations_dict
from tiles import *

st.set_page_config(page_title="麻雀計番器", page_icon="🀄︎")
st.title('麻雀計番器')


if 'is_open' not in st.session_state:
    st.session_state.is_open = False
if 'is_score_from_other' not in st.session_state:
    st.session_state.is_score_from_other = False
if 'is_self_score' not in st.session_state:
    st.session_state.is_self_score = False
if 'hand' not in st.session_state:
    st.session_state.hand = []
if 'result' not in st.session_state:
    st.session_state.result = []

def tile_to_html(tile: Tile):
    button_style = "background-color: black; color: white;" if not (tile.is_open or tile.tile_type == TileType.FLOWER) else "background-color: white; color: black;"
    return f'<div style="{button_style} font-size: 40px; height: 40px; {"transform: rotate(90deg);" if tile.is_scoring_tile else ""} display: flex; justify-content: center; align-items: center; border: 1px solid #ccc; border-radius: 5px; text-align: center;">{tile.to_unicode()}</div>'

def hand_to_html(tiles: list[Tile]):
    close_hand =  ''.join([tile_to_html(tile) for tile in tiles if not tile.is_open and not tile.is_scoring_tile])
    open_hand =  ''.join([tile_to_html(tile) for tile in tiles if tile.is_open and tile.tile_type != TileType.FLOWER and not tile.is_scoring_tile])
    flower_hand =  ''.join([tile_to_html(tile) for tile in tiles if tile.tile_type == TileType.FLOWER])
    scoring_tile = ''.join([tile_to_html(tile) for tile in tiles if tile.is_scoring_tile])
    return f"""<div style='display: flex; flex-wrap: wrap;'>{close_hand}</div>
            <div style='display: flex; flex-wrap: wrap;'>{open_hand}</div>
            <div style='display: flex; flex-wrap: wrap;'>{flower_hand}</div>
            <div style='display: flex; flex-wrap: wrap;'>{scoring_tile}</div>
    """

def click_tile_button(tile_str):
    if len([t for t in st.session_state['hand'] if t == Tile.from_unicode(tile_str)]) >= (4 if tile_str not in Tile.unicode_dict[TileType.FLOWER] else 1):
        st.error(f"{str(Tile.from_unicode(tile_str))} 已有{4 if tile_str not in Tile.unicode_dict[TileType.FLOWER] else 1}張，無法再加入！")
        return

    if len([t for t in st.session_state['hand'] if t.tile_type != TileType.FLOWER]) >= 17 and tile_str not in Tile.unicode_dict[TileType.FLOWER]:
        st.error("手牌已滿，無法再加入！")
        return

    if any([t for t in st.session_state['hand'] if t.is_scoring_tile]) and (st.session_state.is_self_score or st.session_state.is_score_from_other):
        st.error("已經有食胡，無法再加入！")
        return
    
    t = Tile.from_unicode(tile_str)
    if st.session_state.is_self_score:
        t.set_scoring_tile()
        t.is_open = False
        st.session_state.is_self_score = False
    elif st.session_state.is_score_from_other:
        t.set_scoring_tile()
        t.is_open = True
        st.session_state.is_score_from_other = False
    elif st.session_state['is_open']:
        t.set_open()

    st.session_state['hand'].append(t)

def create_tile_button(c, tile_type: TileType, tile_value: int):
    label = f"$ \\large {Tile.unicode_dict[tile_type][tile_value]} $"
    c.button(label, on_click=click_tile_button, args=Tile.unicode_dict[tile_type][tile_value], help=str(Tile.from_unicode(Tile.unicode_dict[tile_type][tile_value])))
    
def print_all_character_combinations():

    for name, point, remark in get_character_combinations_dict():
        explain_cols[0].write(f'{name}{'' if remark is None else f" ({remark})"}')
        explain_cols[1].write(point)

st.button('明' if st.session_state['is_open'] else '暗', on_click=lambda: st.session_state.update(is_open= not st.session_state['is_open']))
st.button(':red[自摸]' if st.session_state['is_self_score'] else '自摸', on_click=lambda: st.session_state.update(is_self_score= not st.session_state['is_self_score'], is_score_from_other = False))
st.button(':red[食]' if st.session_state['is_score_from_other'] else '食', on_click=lambda: st.session_state.update(is_score_from_other= not st.session_state['is_score_from_other'], is_self_score = False))

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
    hand_to_html(st.session_state['hand']),
    unsafe_allow_html=True
)

button_col = st.columns(3)
calculate_click = button_col[0].button('計算')
button_col[1].button('清除', on_click=lambda: st.session_state.update(hand=[], result=''))
button_col[2].button('⌫', on_click=lambda: st.session_state.update(hand=st.session_state.hand[:-1], result=''))
st.button('字牌類', on_click=print_all_character_combinations)

if calculate_click:
    try:
        result = calculate(st.session_state['hand'])
        st.session_state['result'] = result
        st.write(f"計算結果: {sum([r.point_combination.point for r in result])} 番")
        for r in result:
            st.write(r)
    except Exception as e:
        st.error(f"計算錯誤: {e}")

explain_cols = st.columns(2)
