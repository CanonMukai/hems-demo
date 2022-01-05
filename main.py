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
# 最適化関数 callback用
############################################

def solve():
    with st.spinner('計算中です...'):
        solve_DA()
    simple_demo_page()


############################################
# Page 関数
############################################

def create_transition_button(obj):
    # obj に st は使えない
    with obj:
        for page in st.session_state.pages:
            button = st.button(
                "{}へ".format(page.name),
                key="button{}".format(page.name),
                on_click=page.func,
            )

def create_form(obj):
    with obj.form("form"):
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
        submitted = st.form_submit_button(
            label="スケジューリング！",
            on_click=solve,
        )

def common_first():
    # タイトル
    st.title("HEMS エネルギー最適化")
    # ページ遷移ボタン
    create_transition_button(st.sidebar)

def common_last():
    pass

def simple_demo_page():
    common_first()
    params_col, result_col = st.columns([1, 4])
    create_form(params_col)
    result_col.write("結果")
    common_last()

def detailed_demo_page():
    common_first()
    col1, col2 = st.columns([2, 5])
    create_form(col1)
    col2.write("ここに結果を書くよ")
    common_last()

def explanation_page():
    common_first()
    st.markdown("""
このページでは家庭におけるエネルギー利用のスケジューリングを
アニーリングマシンで行う手法について解説します。

ハミルトニアン$H$は以下のようになります。
""")
    st.latex("H = \sum_{i, j}JS_iS_j")
    st.write("※このプロジェクトは未踏ターゲット事務局によりサポートして頂いています。")
    common_last()

def hemsq_page():
    common_first()
    st.write(
        "Pythonパッケージ `HemsQ` を使用することで"
        "より詳細なパラメータを試すことが可能です。"
        "フィックスターズ社の Fixtars Amplify AE と併用する形になります。")
    st.write("以下のコマンドでインストールしてください。")
    st.code("""
$ pip install git+https://github.com/CanonMukai/hemsq-prototype.git
$ pip install amplify
    """)
    st.write("次のようにインポートし、オブジェクトを作成します。")
    st.code("""
from hemsq import HemsQ
hq = HemsQ()
    """, language="python")
    st.write(
        "また `amplify` も同様にインポートし、"
        "マシンのクライアントの設定を行ってください。")
    st.code("""
from amplify.client import XXXClient
client = XXXClient()
hq.set_client(client)
    """, language="python")
    common_last()

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
HEMSQ_PAGE = Page("HemsQ詳細ページ", hemsq_page)


############################################
# Session State の設定
############################################

# 何かアクションを起こすたびに実行される
if "init" not in st.session_state:
    st.session_state.init = True
st.session_state.pages = [
    SIMPLE_DEMO_PAGE,
    # DETAILED_DEMO_PAGE,
    EXPLANATION_PAGE,
    HEMSQ_PAGE,
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
