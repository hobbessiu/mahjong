import streamlit as st
from calculate_point import calculate_from_unicode
from combinations.character_combinations import get_character_combinations_dict

st.set_page_config(page_title="麻雀計番器", page_icon="🀄")
st.title('麻雀計番器')

tung = '🀙🀚🀛🀜🀝🀞🀟🀠🀡'
sok = '🀐🀑🀒🀓🀔🀕🀖🀗🀘'
maan = '🀇🀈🀉🀊🀋🀌🀍🀎🀏'
faan = '🀀🀁🀂🀃🀄🀅🀆'

if 'is_open' not in st.session_state:
    st.session_state.is_open = False
if 'hand' not in st.session_state:
    st.session_state.hand = ''
if 'result' not in st.session_state:
    st.session_state.result = []

def click_button(tile):
    st.session_state['hand'] += tile
    
def print_all_character_combinations():

    for name, point, remark in get_character_combinations_dict():
        explain_cols[0].write(f'{name}{'' if remark is None else f" ({remark})"}')
        explain_cols[1].write(point)

st.button('明' if st.session_state['is_open'] else '暗', on_click=lambda: st.session_state.update(is_open= not st.session_state['is_open']))

cols = st.columns(9)
for i, c in enumerate(cols):
    button_style = "background-color: black; color: white;" if not st.session_state['is_open'] else ""
    c.markdown(
        f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child({i + 1}) button {{
            {button_style}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    c.button(tung[i], on_click=click_button, args=tung[i])
    c.button(sok[i], on_click=click_button, args=sok[i])
    c.button(maan[i], on_click=click_button, args=maan[i])
    if i < 7:
        c.button(faan[i], on_click=click_button, args=faan[i])

st.write(st.session_state['hand'])

button_col = st.columns(2)
calculate_click = button_col[0].button('計算', use_container_width=True)
button_col[1].button('清除', on_click=lambda: st.session_state.update(hand='', result=''), use_container_width=True)
st.button('字牌類', on_click=print_all_character_combinations)

if calculate_click:
    try:
        result = calculate_from_unicode(st.session_state['hand'])
        st.session_state['result'] = result
        st.write(f"計算結果: ")
        for r in result:
            st.write(r)
    except Exception as e:
        st.error(f"計算錯誤: {e}")

explain_cols = st.columns(2)
