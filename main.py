import streamlit as st
from amplify.client import FixstarsClient
from hemsq import HemsQ

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

def solve(tenki_name=None, demand_pattern=None, token=None):
    emoji = st.session_state.params['tenki_emoji'][tenki_name]
    with st.spinner('計算中です...{}'.format(emoji)):
        hq = HemsQ()
        # パラメータの設定
        demand = st.session_state.params['demand'][demand_pattern]
        tenki = st.session_state.params['tenki'][tenki_name]
        hq.set_params(weather_list=tenki, demand_list=demand)
        # クライアントの設定
        client = FixstarsClient()
        client.token = token
        client.parameters.timeout = 1000 # タイムアウト1秒
        client.parameters.outputs.num_outputs = 0
        client.parameters.outputs.duplicate = True # エネルギー値が同一の解を重複して出力する
        hq.set_client(client)
        hq.solve()
    simple_demo_page(hq=hq)


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
    with obj:
        with st.form("form"):
            tenki = st.selectbox(
                "天気",
                (
                    "晴れ",
                    "曇り",
                    "雨",
                )
            )
            demand_pattern = st.selectbox(
                "需要パターン",
                (
                    "少し使いすぎな2人世帯 (日中在宅0人)",
                    "省エネ上手な3人家族 (日中在宅2人)",
                    "2人世帯平均 (日中在宅2人)",
                    "3人世帯 (日中在宅2人)",
                    "5人世帯 (日中在宅3人）",
                )
            )
            token = st.text_input('Amplify のアクセストークン', type='password')
            submitted = st.form_submit_button(
                label="スケジューリング！",
                on_click=solve,
                kwargs={
                    'tenki_name': tenki,
                    'demand_pattern': demand_pattern,
                    'token': token,
                },
            )

def cost_message(val):
    # コスト
    texts = []
    if val['cost'] >= 0:
        texts.append('コスト: {} 円'.format(val['cost']))
    else:
        texts.append('売り上げ: {} 円'.format(-val['cost']))
    # CO2排出量（0.445kg/kWh)
    texts.append('CO2排出量: {} kg'.format(val['CO2']))
    return '\n'.join(texts)

def create_result(obj, hq):
    # コストの表示
    obj.write('1日のコスト')
    val = hq.cost_dict()
    obj.write(cost_message(val))
    # スケジュール表の表示
    obj.write('スケジュール')
    obj.write('pltの表')
    fig1, ax1 = hq.all_table_fig()
    obj.pyplot(fig1)
    obj.write('dfの表')
    obj.dataframe(hq.all_table_df())
    # 需要のグラフ
    fig2, ax2 = hq.demand_graph()
    obj.pyplot(fig2)
    # 太陽光のグラフ
    fig3, ax3 = hq.solar_graph()
    obj.pyplot(fig3)
    # コストと充電のグラフ
    fig4, ax4 = hq.cost_and_charge_graph()
    obj.pyplot(fig4)
    # コストと使用のグラフ
    fig5, ax5 = hq.cost_and_use_graph()
    obj.pyplot(fig5)


def common_first():
    # タイトル
    st.title("HEMS エネルギー最適化")
    # ページ遷移ボタン
    create_transition_button(st.sidebar)

def common_last():
    pass

def simple_demo_page(hq=None):
    common_first()
    params_col, result_col = st.columns([1, 4])
    create_form(params_col)
    result_col.write("結果")
    if hq:
        create_result(result_col, hq)
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
if 'params' not in st.session_state:
    st.session_state.params = {
        'tenki': {
            '晴れ': ['s' for i in range(8)],
            '曇り': ['c' for i in range(8)],
            '雨': ['r' for i in range(8)],
        },
        'tenki_emoji': {
            '晴れ': ':sunny:',
            '曇り': ':cloud:',
            '雨': ':umbrella:',
        },
        'demand': {
            '少し使いすぎな2人世帯 (日中在宅0人)': [550,450,360,350,350,400,420,710,710,620,590,450,450,410,410,410,410,440,500,670,690,670,670,650],
            '省エネ上手な3人家族 (日中在宅2人)': [230,150,130,120,110,110,130,190,340,360,340,340,260,260,270,220,240,410,430,410,430,330,310,270],
            '2人世帯平均 (日中在宅2人)': [207,177,147,157,157,167,228,330,381,391,351,311,341,341,311,310,320,331,372,542,549,509,438,318],
            '3人世帯 (日中在宅2人)': [242,207,172,184,184,195,267,536,596,607,561,364,199,199,164,163,174,187,435,634,642,596,512,372],
            '5人世帯 (日中在宅3人）': [290,248,206,220,220,234,319,462,533,547,491,435,527,527,485,484,498,513,521,759,769,713,613,445],
        },
    }

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
