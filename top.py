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
    fig_col, sukima1_col, page_col, sukima2_col = st.columns([10, 0.5, 9, 0.5])
    fig_col.image('https://drive.google.com/uc?export=view&id=1JLZzu_2tgNxuhpqBj5QoXjgqeANJugMJ&usp=sharing')
    
    page_col.button('デモ', key='デモトップ', on_click=st.session_state.pages['デモ'].func)
    page_col.write('お天気、需要パターンを選択して簡単なシミュレーションができます！')
    page_col.button('実行例', key='実行例トップ', on_click=st.session_state.pages['実行例'].func)
    page_col.write('HemsQを用いて得たスケジュールを簡単に可視化しています。')
    page_col.button('アニーリングマシンでの解き方', key='解き方トップ', on_click=st.session_state.pages['アニーリングマシンでの解き方'].func)
    page_col.write('アニーリングマシンで HEMS の最適化をするにあたって、どのような定式化を行なっているのかを解説しています。')
    page_col.button('HemsQの詳細', key='HemsQトップ', on_click=st.session_state.pages['HemsQの詳細'].func)
    page_col.write('Python で動かすことのできる HemsQ の使い方について解説しています。')
    page_col.markdown('''
<span>
<a href="https://colab.research.google.com/drive/18BPHExIrYWZrwwYUFU4KvRjNbFCvrDi3?usp=sharing"
        target="_blank" rel="noopener noreferrer">Google Colab</a>
    で実行できるコードもあります。
</span>
''', unsafe_allow_html=True)
    st.markdown('''
<br><br>
<span>
    ※ 本プロジェクトは、
<a href="https://www.ipa.go.jp/jinzai/target/index.html"
        target="_blank" rel="noopener noreferrer">未踏ターゲット事業</a>
    のサポートにより進めさせていただいています。
</span>
''', unsafe_allow_html=True)
    st.markdown(text_css, unsafe_allow_html=True)
    st.markdown(text_input_css, unsafe_allow_html=True)
    for c in sukima1_text:
        write_white(sukima1_col, c)
    for c in sukima2_text:
        write_white(sukima2_col, c)
    write_white(st, sukima3_text)
    event()
