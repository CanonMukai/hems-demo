import time

import streamlit as st
from hemsq import HemsQ

from sub import *
from top import write, top
from sample_result import *
from article import convert, type_and_text
from css import *

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
    spinner_text = '''
デモを使用していただき、誠にありがとうございます！

現在計算中です...{} すこーーーーしお待ちください...

お天気が悪いほど時間がかかるかもしれません...「☂️」のときなんか最悪ですね...

「少し使いすぎな2人世帯」「5人世帯」の場合もちょっとお時間いただくかもしれません...

初期蓄電量が少ない場合もちょっとかかるかも...

速いと10秒ちょいで終わるのですが、遅いと数分かかるかも...？

このページは dwave-neal (https://docs.ocean.dwavesys.com/projects/neal/) という、シミュレーテッド・アニーリングの Python パッケージをありがたく使わせていただいています。
マシンに比べると少し時間がかかってしまいます...

ここまでお読みになっているということは、結構かかっていますよね...
最悪の場合、答えが出ない場合もあります...
そのときは、もう一度同じパラメータで最適化ボタンを押し直してみてくださいね...

それにしても、かかっていますね...この文章を読まれるのは何度目でしょうか...
お、1回目ですか？とってもかわいいです...数十秒後、またこの場所でお逢いしましょう()

私(メンバー2)はうっかり「☂️」「5人」「0 (W)」を選択してしまったことがあって、そのときは10回やそこらじゃ足りませんでした...

暇で暇で気が狂いそうな方は、このページを別タブでも開いていただいて、「アニーリングマシンでの解き方」という項目をご覧になってお待ちください...
読み終わる頃にはきっと計算が終わっている...はず....です☆

暇で暇で気が狂ってしまった方は、このページをリロードして別のパラメータでやり直していただくのもありですし、寂しいけれど、そっとこのページを閉じていただくのもありです、そうです、それがきっと最善策です...

非常にご迷惑をおかけしております...ここまでお待ちくださり、本当にありがとうございます...

右上のピクトグラム、いろいろと蘇りますね、かわいいですね...
'''.format(emoji)
    spinner_text = '計算中です...{}'.format(emoji)
    start_time = time.time()
    with st.spinner(spinner_text):
        hq = HemsQ()
        # パラメータの設定
        demand = st.session_state.params['demand'][demand_pattern]
        tenki = st.session_state.params['tenki'][tenki_name]
        bat_ini = st.session_state['bat_ini']
        hq.set_params(weather_list=tenki, demand_list=demand)
        hq.set_params(initial_battery_amount=bat_ini)
        hq.set_params(unit=200, step=8, reschedule_span=8)
        if st.session_state.cost_ratio == '環境優先':
            hq.set_params(cost_ratio=0.0)
        successful = False
        for _ in range(10):
            result = hq.solve('SA')
            if result:
                successful = True
                break
    end_time = time.time()
    st.session_state.long_time = (end_time - start_time) > 60
    st.session_state.form_expanded = False
    simple_demo_page(hq=hq, successful=successful)


############################################
# Page 関数
############################################

def create_transition_button(obj):
    # obj に st は使えない
    with obj:
        for page in st.session_state.pages.values():
            button = st.button(
                "{}".format(page.name),
                key="button{}{}".format(page.name, time.time()),
                on_click=page.func,
            )

def create_form():
    with st.expander('パラメータ', expanded=st.session_state.form_expanded):
        with st.form('form'):
            c1, c2, c3, c4, c5 = st.columns([0.7, 2, 1, 1, 0.5])
            c1.selectbox('お天気', ['晴れ', '曇り', '雨'], key='tenki_name')
            c2.selectbox(
                '需要パターン',
                (
                    '省エネ上手な3人家族 (日中在宅2人)',
                    '少し使いすぎな2人世帯 (日中在宅0人)',
                    '2人世帯平均 (日中在宅2人)',
                    '3人世帯 (日中在宅2人)',
                    '5人世帯 (日中在宅3人）',
                ),
                key='demand_pattern',
            )
            c3.number_input(
                '初期蓄電量 (W)',
                min_value=0,
                max_value=5000,
                value=4500,
                step=500,
                key='bat_ini',
                help='最初に蓄電池にたまっている電力',
            )
            c4.radio(
                '優先度',
                ['コスト優先', '環境優先'],
                key='cost_ratio',
            )
            c5.text('最適化')
            with c5:
                st.form_submit_button(label='GO!!', on_click=solve)

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
    st.markdown('<img src="https://drive.google.com/uc?export=view&id=1G3dz52ZxDkXJUXVBvJ-itZnCB6WZGZsJ&usp=sharing" width="100%"><br>',
        unsafe_allow_html=True)
    # ページ遷移ボタン
    st.markdown(side_button_css, unsafe_allow_html=True)
    create_transition_button(st.sidebar)

def common_last():
    pass

def top_page():
    st.session_state.last_page = 'TOP'
    # common_first()
    top()
    common_last()

def simple_demo_page(hq=None, successful=None):
    st.session_state.last_page = 'デモ'
    if hq == None or successful == False:
        st.session_state.form_expanded = True
    common_first()
    create_form()
    if hq:
        if successful:
            if st.session_state.long_time:
                st.success('''
大変長らくお待たせいたしました m(_ _)m
環境にもおサイフにも優しいハッピーなエネルギーライフを♪
''')
            create_result(hq)
        else:
            st.error('''
ごめんなさい、最適化に失敗してしまいました m(_ _)m
もう一度ボタンを押して試してみてください。次はうまくいきますように。。
''')
    common_last()

def demo_example_page():
    st.session_state.last_page = '実行例'
    common_first()
    st.markdown('''
### 初期蓄電量による違い
初期蓄電量とは、最初に蓄電池に残っている電力量のことです。

今回は 4500 (W) のときと 0 (W) のときの結果を比較しています。

まずは、需要に対して、商用電源、太陽光、蓄電池の電力のそれぞれの使用量をグラフにしました。
''')
    st.image('https://drive.google.com/uc?export=view&id=1MxkWWsZixF4q0JxVCdBIXbH2P2AsnvRM&usp=sharing', width=300)
    plotly_fig_demand = plotly_demand_compare(result_bat4500['df'], result_bat0['df'])
    st.plotly_chart(plotly_fig_demand, use_container_width=True)

    st.markdown('''
次に、蓄電使用量と残量のグラフです。
''')
    plotly_fig_bat = plotly_bat_compare(result_bat4500['df'], result_bat0['df'])
    st.plotly_chart(plotly_fig_bat, use_container_width=True)

    st.markdown('''
### コスト優先 or 環境優先 による違い
''')
    col1, col2, col3 = st.columns([1, 1.5, 3])
    col1.metric(label='お天気', value='☀️')
    col2.metric(label='少し使いすぎな2人世帯', value='👨 👩')
    col3.metric(label='日中在宅0人', value='🐶')
    st.markdown('''
##### コスト優先
''')
    col21, col22, col23 = st.columns([1, 1.5, 3])
    col21.metric(label='コスト', value='{} 円'.format(result_cost10env0['cost']))
    col22.metric(label='CO2排出量', value='{} kg'.format(result_cost10env0['CO2']))
    col23.write(' ')
    st.markdown('''
##### 環境優先
''')
    col31, col32, col33 = st.columns([1, 1.5, 3])
    col31.metric(label='コスト', value='{} 円'.format(result_cost0env10['cost']))
    col32.metric(label='CO2排出量', value='{} kg'.format(result_cost0env10['CO2']))
    col33.write(' ')
    st.write('※ コスト：環境の比による最適化は完全でなく、現在模索中です。')

    st.markdown('''
### 天気による違い
''')
    common_last()

def explanation_page():
    st.session_state.last_page = 'アニーリングマシンでの解き方'
    common_first()
    convert(type_and_text)
    common_last()

def hemsq_page():
    st.session_state.last_page = 'HemsQの詳細'
    common_first()
    st.write(
        "Pythonパッケージ `HemsQ` を使用することで"
        "より詳細なパラメータを試すことが可能です。"
        "フィックスターズ社の Fixtars Amplify AE と併用する形になります。")
    
    st.markdown(colab_button_css, unsafe_allow_html=True)
    st.markdown('''
    <a href="https://colab.research.google.com/drive/18BPHExIrYWZrwwYUFU4KvRjNbFCvrDi3?usp=sharing"
        target="_blank" rel="noopener noreferrer">
            <button type="button" class="colab">Google Colabで開く</button>
    </a>''',
        unsafe_allow_html=True)
    st.write("以下のコマンドでインストールしてください。")
    st.code("""
$ pip install git+https://github.com/HemsQ/hemsq.git
    """)
    st.write("次のようにインポートし、オブジェクトを作成します。")
    st.code("""
from hemsq import HemsQ
hq = HemsQ()
    """, language="python")
    st.write(
        "また `amplify` のクライアントも同様にインポートし、"
        "マシンのクライアントの設定を行ってください。")
    st.code("""
# Fixstars の場合
from amplify.client import Fixstarslient

client = FixstarsClient()
client.token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # アクセストークン
client.parameters.timeout = 1000 # タイムアウト1秒
client.parameters.outputs.num_outputs = 0
client.parameters.outputs.duplicate = True # エネルギー値が同一の解を重複して出力する
hq.set_client(client)
    """, language="python")
    st.write("まずはデフォルトのパラメータで実行してみましょう！")
    st.code("""
# 最適化
hq.solve()
# 可視化
hq.show_all()
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

TOP_PAGE = Page("TOP", top_page)
SIMPLE_DEMO_PAGE = Page("デモ", simple_demo_page)
DEMO_EXAMPLE_PAGE = Page("実行例", demo_example_page)
EXPLANATION_PAGE = Page("アニーリングマシンでの解き方", explanation_page)
HEMSQ_PAGE = Page("HemsQの詳細", hemsq_page)


############################################
# Session State の設定
############################################

# 何かアクションを起こすたびに実行される
if "init" not in st.session_state:
    st.session_state.init = True
if 'pages' not in st.session_state:
    st.session_state.pages = {
        TOP_PAGE.name: TOP_PAGE,
        SIMPLE_DEMO_PAGE.name: SIMPLE_DEMO_PAGE,
        DEMO_EXAMPLE_PAGE.name: DEMO_EXAMPLE_PAGE,
        EXPLANATION_PAGE.name: EXPLANATION_PAGE,
        HEMSQ_PAGE.name: HEMSQ_PAGE,
    }
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
if 'last_page' not in st.session_state:
    st.session_state.last_page = 'TOP'


############################################
# main
############################################

# 何かアクションを起こすたびに実行される
if __name__ == '__main__':
    # デバッグ用session_state
    # st.session_state
    if st.session_state.init:
        # simple_demo_page()
        # top_page()
        page = st.session_state.last_page
        st.session_state.pages[page].func()
        st.session_state.init = False
