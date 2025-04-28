import streamlit as st
from calculate_point import calculate_from_unicode

tung = '🀙🀚🀛🀜🀝🀞🀟🀠🀡'
sok = '🀐🀑🀒🀓🀔🀕🀖🀗🀘'
maan = '🀇🀈🀉🀊🀋🀌🀍🀎🀏'
faan = '🀀🀁🀂🀃🀄🀅🀆'
st.set_page_config(page_title="麻雀計番器", page_icon="🀄")
if 'hand' not in st.session_state:
    st.session_state.hand = ''
def click_button(tile):
    st.session_state['hand'] += tile
    

st.title('麻雀計番器')

cols = st.columns(9)
for i, c in enumerate(cols):
    c.button(tung[i], on_click=click_button, args=tung[i])
    c.button(sok[i], on_click=click_button, args=sok[i])
    c.button(maan[i], on_click=click_button, args=maan[i])
    if i < 7:
        c.button(faan[i], on_click=click_button, args=faan[i])

# for s in sok:
#     st.button(s, on_click=click_button, args=s)

st.write(st.session_state['hand'])

calculate_click = st.button('計算')
st.button('清除', on_click=lambda: st.session_state.update(hand='', result=''))

if calculate_click:
    try:
        result = calculate_from_unicode(st.session_state['hand'])
        st.session_state['result'] = result
        st.write(f"計算結果: {result}")
    except Exception as e:
        st.error(f"計算錯誤: {e}")

