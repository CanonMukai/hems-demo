import streamlit as st
from annealing import *

############################################
# Streamlit 全体の設定
############################################

st.set_page_config(
    page_title='HEMSデモ',
    page_icon='🏠',
    layout='wide',
    initial_sidebar_state='expanded',
)


############################################
# Page 関数
############################################

def common():
    # デバッグ用session_state
    # st.session_state
    # タイトル
    st.title("HEMS エネルギー最適化")
    # ページ遷移ボタン
    for i in range(st.session_state.all_pages):
        button = st.sidebar.button(
            "{}へ".format(st.session_state.page_name[i]),
            key="button{}".format(i),
            on_click=st.session_state.page_func[i],
        )

def demo_page():
    common()
    st.write("デモ")

def explanation_page():
    common()
    st.markdown("""
このページでは家庭におけるエネルギー利用のスケジューリングを
アニーリングマシンで行う手法について解説します。

ハミルトニアン$H$は以下のようになります。
""")
    st.latex("H = \sum_{i, j}JS_iS_j")
    st.write("※このプロジェクトは未踏ターゲット事務局によりサポートして頂いています。")

############################################
# Session State の設定
############################################

# 何かアクションを起こすたびに実行される
if "init" not in st.session_state:
    st.session_state.init = True
st.session_state.all_pages = 2
st.session_state.current_page = 0
st.session_state.page_name = ["デモページ", "解説ページ"]
st.session_state.page_func = [demo_page, explanation_page]


############################################
# main
############################################

# 何かアクションを起こすたびに実行される
if __name__ == '__main__':
    if st.session_state.init:
        demo_page()
        st.session_state.init = False
