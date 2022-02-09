import streamlit as st

def event():
    st.text_input(
        'この下に入力欄があるよ',
        placeholder='来たるイベントに必須の食べ物は？',
        key='special_event',
        on_change=st.session_state.pages['TOP'].func)
    if st.session_state.special_event in [
            'チョコ', 'チョコレート', '🍫', 'ショコラ', 'chocolate', 'ちょこ',
            'ちよこれーと', 'ちよこれいと']:
        display()

def display():
    st.write('お見事！！')
    st.image('https://drive.google.com/uc?export=view&id=1W0TtWXV5O-7emlBPv5OWE3VDBN9Gr1w6&usp=sharing')

sukima1_text = 'はっ！お気づきになられましたか！'
sukima2_text = 'ここもお気づきになられましたか！もう一息'
sukima3_text = 'Super Dark Mode ユーザーには弱い...'
