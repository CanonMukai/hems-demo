import streamlit as st

from event import *
from css import *


def write(obj, text):
    obj.write(
        '<span style="color:black;">{}</span>'.format(text),
        unsafe_allow_html=True)

def write_white(obj, text):
    obj.markdown(
f'''
<span class="hide">{text}</span>
''',
        unsafe_allow_html=True)

def top():
    st.markdown('<img src="https://drive.google.com/uc?export=view&id=1Pr0SqODXkkGiG5_v1sFHQ3kobc7URdN_&usp=sharing" width="100%">',
        unsafe_allow_html=True)
    write(st, '<br>')
    fig_col, left_col, right_col = st.columns([1.8, 1, 1])
    fig_col.image("https://drive.google.com/uc?export=view&id=1JLZzu_2tgNxuhpqBj5QoXjgqeANJugMJ&usp=sharing")
    st.markdown(button_css, unsafe_allow_html=True)
    left_col.button('デモを動かそう', key='デモトップ', on_click=st.session_state.pages['デモ'].func)
    right_col.button('HemsQのねらいと定式化', key='解き方トップ', on_click=st.session_state.pages['アニーリングマシンでの解き方'].func)
    right_col.button('実行例を見てみよう', key='実行例トップ', on_click=st.session_state.pages['実行例'].func)
    left_col.button('Google Colab & pip install', key='HemsQトップ', on_click=st.session_state.pages['HemsQの詳細'].func)
    
    st.markdown('''
<br>
<span>
    ※ 本プロジェクトは、
<a href="https://www.ipa.go.jp/jinzai/target/index.html"
        target="_blank" rel="noopener noreferrer">未踏ターゲット事業</a>
    のサポートの元進めております。
</span>
''', unsafe_allow_html=True)
    st.markdown(text_css, unsafe_allow_html=True)
    st.markdown(text_input_css, unsafe_allow_html=True)
    write_white(st, sukima_text)
    event()
