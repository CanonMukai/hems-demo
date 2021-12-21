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
    # タイトル
    st.title("HEMS エネルギー最適化")
    # ページ遷移ボタン
    for page in st.session_state.pages:
        button = st.sidebar.button(
            "{}へ".format(page.name),
            key="button{}".format(page.name),
            on_click=page.func,
        )

def simple_demo_page():
    common()
    col1, col2, col3 = st.columns([1, 3, 2])
    with col1.form("form"):
        tenki = st.selectbox(
            "天気",
            (
                "現在の天気予報",
                "晴れ",
                "曇り",
                "雨",
            )
        )
        demand_pattern = st.selectbox(
            "需要パターン",
            (
                "少し使いすぎな2人世帯 (日中在宅2人)",
                "省エネ上手な3人家族 (日中在宅2人)",
                "2人世帯平均 (日中在宅2人)",
                "3人世帯 (日中在宅2人)",
                "5人世帯 (日中在宅3人）",
            )
        )
        machine = st.radio(
            "マシン",
            ["デジタルアニーラ", "Amplify"],
        )
        submitted = st.form_submit_button("スケジューリング！")
        if submitted: pass

    col2.write("アニーリングマシンの結果")
    col3.write("従来法の結果")

def detailed_demo_page():
    common()
    st.write("Coming soon.")

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
# Page Class の設定と constant 化
############################################
class Page:
    def __init__(self, name, func):
        self._name = name
        self._func = func

    @property
    def name(self):
        return self._name

    @property
    def func(self):
        return self._func

SIMPLE_DEMO_PAGE = Page("簡易デモページ", simple_demo_page)
DETAILED_DEMO_PAGE = Page("詳細デモページ", detailed_demo_page)
EXPLANATION_PAGE = Page("説明ページ", explanation_page)


############################################
# Session State の設定
############################################

# 何かアクションを起こすたびに実行される
if "init" not in st.session_state:
    st.session_state.init = True
st.session_state.pages = [
    SIMPLE_DEMO_PAGE,
    DETAILED_DEMO_PAGE,
    EXPLANATION_PAGE,
]


############################################
# main
############################################

# 何かアクションを起こすたびに実行される
if __name__ == '__main__':
    # デバッグ用session_state
    # st.session_state
    if st.session_state.init:
        simple_demo_page()
        st.session_state.init = False
