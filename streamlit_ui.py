import streamlit as st
from calculate_point import calculate
from combinations.character_combinations import get_character_combinations_dict
from tiles import *

st.set_page_config(page_title="麻雀計番器", page_icon="🀄")
st.title('麻雀計番器')


if 'is_open' not in st.session_state:
    st.session_state.is_open = False
if 'hand' not in st.session_state:
    st.session_state.hand = []
if 'result' not in st.session_state:
    st.session_state.result = []

def tile_to_html(tile: Tile):
    button_style = "background-color: black; color: white;" if not (tile.is_open or tile.tile_type == TileType.FLOWER) else "background-color: white; color: black;"
    return f'<div style="{button_style} padding: 10px; display: inline-block; border: 1px solid #ccc; border-radius: 5px; text-align: center;">{tile.to_unicode()}</div>'

def hand_to_html(tiles: list[Tile]):
    hand =  ''.join([tile_to_html(tile) for tile in tiles])
    return f"<div style='display: flex; '>{hand}</div>"

def click_tile_button(tile_str):
    if len([t for t in st.session_state['hand'] if t == Tile.from_unicode(tile_str)]) >= (4 if tile_str not in Tile.unicode_dict[TileType.FLOWER] else 1):
        st.error(f"{str(Tile.from_unicode(tile_str))} 已有{4 if tile_str not in Tile.unicode_dict[TileType.FLOWER] else 1}張，無法再加入！")
        return

    if len([t for t in st.session_state['hand'] if t.tile_type != TileType.FLOWER]) >= 17 and tile_str not in Tile.unicode_dict[TileType.FLOWER]:
        st.error("手牌已滿，無法再加入！")
        return

    t = Tile.from_unicode(tile_str)
    if st.session_state['is_open']:
        t.set_open()

    st.session_state['hand'].append(t)

def create_tile_button(c, tile_type: TileType, tile_value: int):
    c.button(Tile.unicode_dict[tile_type][tile_value], on_click=click_tile_button, args=Tile.unicode_dict[tile_type][tile_value], help=str(Tile.from_unicode(Tile.unicode_dict[tile_type][tile_value])))
    
def print_all_character_combinations():

    for name, point, remark in get_character_combinations_dict():
        explain_cols[0].write(f'{name}{'' if remark is None else f" ({remark})"}')
        explain_cols[1].write(point)

st.button('明' if st.session_state['is_open'] else '暗', on_click=lambda: st.session_state.update(is_open= not st.session_state['is_open']))

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

button_col = st.columns(2)
calculate_click = button_col[0].button('計算', use_container_width=True)
button_col[1].button('清除', on_click=lambda: st.session_state.update(hand=[], result=''), use_container_width=True)
st.button('字牌類', on_click=print_all_character_combinations)

if calculate_click:
    try:
        result = calculate(st.session_state['hand'])
        st.session_state['result'] = result
        st.write(f"計算結果: ")
        for r in result:
            st.write(r)
    except Exception as e:
        st.error(f"計算錯誤: {e}")

explain_cols = st.columns(2)
