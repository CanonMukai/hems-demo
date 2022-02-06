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
    obj.write(
        '<span style="color:white;">{}</span>'.format(text),
        unsafe_allow_html=True)

def top():
    st.title('🏠💡 HemsQ 🌦🏠')
    st.markdown('''
### ~ エネルギー最適化をアニーリングマシンで ~
''')
    write(st, '<br>')
#     st.write('''
# 本ページでは、HEMS (Home Energy Management System) における「エネルギーの管理」部分を、アニーリングマシンという次世代コンピュータを用いて効率的にスケジューリングするプロジェクトについて説明しております。
# ''')
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
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
    # write(c4, 'c4')
    st.markdown(
        '<button type="button" style="color:white;border:none;background-color:white;">隠しボタン</button>',
        unsafe_allow_html=True,
    )

top()
