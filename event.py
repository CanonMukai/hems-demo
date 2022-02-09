import streamlit as st


def event():
    st.text_input(
        'この下に入力欄があるよ',
        placeholder='来たるイベントに必須の食べ物は？',
        key='special_event')
    text = st.session_state.special_event
    return text in ['チョコ', 'チョコレート', '🍫', 'ショコラ', 'chocolate', 'ちょこ', 'ちよこれーと']

def display():
    st.write('お見事！！')
    st.image('https://drive.google.com/uc?export=view&id=1W0TtWXV5O-7emlBPv5OWE3VDBN9Gr1w6&usp=sharing')

sukima1_text = 'はっ！お気づきになられましたか！'
sukima2_text = 'おおっ！ここもお気づきになられましたか！'
sukima3_text = 'Super Dark Mode ユーザーには弱い...'
    
