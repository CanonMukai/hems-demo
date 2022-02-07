import streamlit as st

st.set_page_config(
    page_title='HEMSデモ',
    page_icon='🏠',
    layout='wide',
    initial_sidebar_state='expanded',
)

def write(obj, text):
    obj.write(
        '<span style="color:black;">{}</span>'.format(text),
        unsafe_allow_html=True)

def write_white(obj, text):
    obj.markdown(
f'''
<span class="hide">
{text}
</span>
''',
        unsafe_allow_html=True)

def top():
    st.markdown(
f'''
<head>
    <style>
        .hide {{
            color: rgba(0, 0, 0, 0);
        }}
        .hide::selection {{
            color: blue;
        }}
        ::-moz-selection {{
            color: blue;
        }}
        @media (prefers-color-scheme: dark) {{
            body {{
                background-color: #000;
                color: #fff;
            }}
            .hide {{
                color: rgba(0, 0, 0, 0);
            }}
        }}
    </style>
</head>
''',
        unsafe_allow_html=True)
    st.title('🏠💡 HemsQ 🌦🏠')
    st.markdown('''
### ~ エネルギー最適化をアニーリングマシンで ~
''')
    write(st, '<br>')
#     st.write('''
# 本ページでは、HEMS (Home Energy Management System) における「エネルギーの管理」部分を、アニーリングマシンという次世代コンピュータを用いて効率的にスケジューリングするプロジェクトについて説明しております。
# ''')
    c1, c3, c2, c4 = st.columns([1, 0.1, 1, 1])
    c1.image('https://drive.google.com/uc?export=view&id=1qOPQvru_tcXQ3myIAZQ7its_igPGlVSW&usp=sharing')
    c2.button('デモ')
    c2.write('お天気、需要パターンを選択して簡単なシミュレーションができます！')
    c2.button('実行例')
    c2.write('HemsQを用いて得たスケジュールを簡単に可視化しています。')
    c2.button('アニーリングマシンでの解き方')
    c2.write('アニーリングマシンで HEMS の最適化をするにあたって、どのような定式化を行なっているのかを解説しています。')
    c2.button('HemsQの詳細')
    c2.write('Python で動かすことのできる HemsQ の使い方について解説しています。')
    c2.markdown('''
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
    # write(c3, 'c3')
    c1.code('''
NEWS

22.02.11
 - サイトがオープンしました！
 - HemsQ の試用を開始しました。
''')
    # write(c4, 'c4')
    write_white(c3, 'は')
    write_white(c3, 'っ')
    write_white(c3, '！')
    write_white(c3, 'お')
    write_white(c3, '気')
    write_white(c3, 'づ')
    write_white(c3, 'き')
    write_white(c3, 'に')
    write_white(c3, 'な')
    write_white(c3, 'ら')
    write_white(c3, 'れ')
    write_white(c3, 'ま')
    write_white(c3, 'し')
    write_white(c3, 'た')
    write_white(c3, 'か')
    st.markdown(
        '<button class="hide" type="button" style="color:rgba(0,0,0,0);border:none;background-color:rgba(0,0,0,0);">隠しボタン</button>',
        unsafe_allow_html=True,
    )

top()

# button_css = f"""
# <style>
# @media (prefers-color-scheme: dark) {{
#   body {{
#     background-color: #000;
#     color: #fff;
#   }}
# }}
#   div.stButton > button:first-child  {{
#     font-weight  : bold                ;/* 文字：太字                   */
#     border       :  5px solid #f36     ;/* 枠線：ピンク色で5ピクセルの実線 */
#     border-radius: 10px 10px 10px 10px ;/* 枠線：半径10ピクセルの角丸     */
#     background   : #ddd                ;/* 背景色：薄いグレー            */
#   }}
# </style>
# """
# st.markdown(button_css, unsafe_allow_html=True)
action = st.button('このボタンを押してください')

css = '''
<style>
:root {
  --main-text: #333;
  --main-bg: #fff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --main-text: #ddd;
    --main-bg: #000;
  }
}
body {
  color: var(--main-text);
  background-color: var(--main-bg);
  transition: .5s;
}

@import url('https://fonts.googleapis.com/css?family=Playfair+Display&display=swap');
.wrap {
  text-align: center;
  padding: 2rem;
  font-family: 'Playfair Display', serif;
}
h1 {
  font-size: 3rem;
}
p {
  font-size: 1.5rem;
  line-height: 1.5;
  
}
h1, p {
  margin-bottom: 1rem;
}
a {
  color: #0bd
}
.btn {
  background: #0bd;
  padding: 6px 20px;
  border-radius: 5px;
  display: inline-block;
  color: #fff;
  text-decoration: none;
}
</style>
'''
# st.markdown(css, unsafe_allow_html=True)