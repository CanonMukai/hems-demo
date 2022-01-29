import streamlit as st
from hemsq import HemsQ

from sub import *
from sample_result import *

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
    tenki_name = st.session_state['tenki_name']
    demand_pattern = st.session_state['demand_pattern']
    emoji = st.session_state.params['tenki_emoji'][tenki_name]
    with st.spinner('計算中です...{}'.format(emoji)):
        hq = HemsQ()
        # パラメータの設定
        demand = st.session_state.params['demand'][demand_pattern]
        tenki = st.session_state.params['tenki'][tenki_name]
        hq.set_params(weather_list=tenki, demand_list=demand)
        hq.set_params(unit=250, step=8, reschedule_span=8)
        # クライアントの設定
        hq.solve('SA')
    st.session_state.form_expanded = False
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

def create_form():
    with st.expander('パラメータ', expanded=st.session_state.form_expanded):
        with st.form('form'):
            c1, c2, c3 = st.columns([0.5, 2, 3])
            c1.selectbox('お天気', ['晴れ', '曇り', '雨'], key='tenki_name')
            c2.selectbox(
                '需要パターン',
                (
                    '少し使いすぎな2人世帯 (日中在宅0人)',
                    '省エネ上手な3人家族 (日中在宅2人)',
                    '2人世帯平均 (日中在宅2人)',
                    '3人世帯 (日中在宅2人)',
                    '5人世帯 (日中在宅3人）',
                ),
                key='demand_pattern',
            )
            c3.text('ボタンを押すと最適化スタート')
            with c3:
                st.form_submit_button(label="スケジューリング！", on_click=solve)

def create_result(hq):
    # column を分ける
    col1, col2, col5 = st.columns([1, 1.5, 3])
    # 天気
    emoji = st.session_state.params['tenki_emoji'][st.session_state.tenki_name]
    col1.metric(label='お天気', value=emoji)
    # 需要パターン
    family = st.session_state.params['family'][st.session_state.demand_pattern]
    col2.metric(label=family[0], value=family[1])
    col5.metric(label=family[2], value=family[3])
    # コストの表示
    val = hq.cost_dict()
    cost = my_round(val['cost'], digit=1)
    if cost >= 0:
        col1.metric(label='コスト', value='{} 円'.format(cost))
    else:
        col1.metric(label='売り上げ', value='{} 円'.format(-cost))
    # CO2排出量（0.445kg/kWh)
    col2.metric(label='CO2排出量', value='{} kg'.format(val['CO2']))

    # スケジュール表の表示
    with st.expander('全スケジュール表'):
        fig1, ax1 = hq.all_table_fig()
        st.pyplot(fig1)

    # plotly
    df = modified_df(hq.all_table_df())
    plotly_fig1 = plotly_demand_graph(df)
    st.plotly_chart(plotly_fig1, use_container_width=True)
    plotly_fig2 = plotly_solar_graph(df)
    st.plotly_chart(plotly_fig2, use_container_width=True)
    plotly_fig3 = plotly_charge_graph(df)
    st.plotly_chart(plotly_fig3, use_container_width=True)

def common_first():
    # タイトル
    st.title("HEMS エネルギー最適化")
    # ページ遷移ボタン
    create_transition_button(st.sidebar)

def common_last():
    pass

def simple_demo_page(hq=None):
    if hq == None:
        st.session_state.form_expanded = True
    common_first()
    create_form()
    if hq:
        create_result(hq)
    common_last()

def demo_example_page():
    common_first()
    st.markdown('''
### 初期蓄電量による違い
初期蓄電量とは、最初に蓄電池に残っている電力量のことです。

今回は 4500 (W) のときと 0 (W) のときの結果を比較しています。

まずは、需要に対して、商用電源、太陽光、蓄電池の電力のそれぞれの使用量をグラフにしました。
''')
    st.image('imgs/legend_demand.png', width=150)
    plotly_fig_demand = plotly_demand_compare(result_bat4500['df'], result_bat0['df'])
    st.plotly_chart(plotly_fig_demand, use_container_width=True)

    st.markdown('''
次に、蓄電使用量と残量のグラフです。

- レッド系の棒：初期蓄電量 4500 (W)
- ブルー系の棒：初期蓄電量 0 (W)

- 濃い色：残量
- 薄い色：使用量
''')
    plotly_fig_bat = plotly_bat_compare(result_bat4500['df'], result_bat0['df'])
    st.plotly_chart(plotly_fig_bat, use_container_width=True)

    st.markdown('''
### 天気による違い
''')
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
DEMO_EXAMPLE_PAGE = Page("デモの例", demo_example_page)
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
    DEMO_EXAMPLE_PAGE,
    EXPLANATION_PAGE,
    HEMSQ_PAGE,
]
if 'form_expanded' not in st.session_state:
    st.session_state.form_expanded = True
if 'params' not in st.session_state:
    st.session_state.params = {
        'tenki': {
            '晴れ': ['s' for i in range(8)],
            '曇り': ['c' for i in range(8)],
            '雨': ['r' for i in range(8)],
        },
        'tenki_emoji': {
            '晴れ': '☀️',
            '曇り': '☁️',
            '雨': '☂️',
        },
        'demand': {
            '少し使いすぎな2人世帯 (日中在宅0人)': [550,450,360,350,350,400,420,710,710,620,590,450,450,410,410,410,410,440,500,670,690,670,670,650],
            '省エネ上手な3人家族 (日中在宅2人)': [230,150,130,120,110,110,130,190,340,360,340,340,260,260,270,220,240,410,430,410,430,330,310,270],
            '2人世帯平均 (日中在宅2人)': [207,177,147,157,157,167,228,330,381,391,351,311,341,341,311,310,320,331,372,542,549,509,438,318],
            '3人世帯 (日中在宅2人)': [242,207,172,184,184,195,267,536,596,607,561,364,199,199,164,163,174,187,435,634,642,596,512,372],
            '5人世帯 (日中在宅3人）': [290,248,206,220,220,234,319,462,533,547,491,435,527,527,485,484,498,513,521,759,769,713,613,445],
        },
        'family': {
            '少し使いすぎな2人世帯 (日中在宅0人)': ['少し使いすぎな2人世帯', '👨 👩', '日中在宅0人', '🐶'],
            '省エネ上手な3人家族 (日中在宅2人)': ['省エネ上手な3人家族', '👨 👩', '日中在宅2人', '👨 👩'],
            '2人世帯平均 (日中在宅2人)': ['2人世帯平均', '👨 👩', '日中在宅2人', '👨 👩'],
            '3人世帯 (日中在宅2人)': ['3人世帯', '👨 👩 👦', '日中在宅2人', '👨 👩'],
            '5人世帯 (日中在宅3人）': ['5人世帯', '👴 👵 👨 👩 👶', '日中在宅3人', '👴 👵 👶'],
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
