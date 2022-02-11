import streamlit as st
import requests
import json

def event():
    st.text_input(
        'よくお気づきになられました！！この少し下をタップしてみてください',
        placeholder='来たるイベントに必須の食べ物は？',
        key='special_event',
        on_change=st.session_state.pages['TOP'].func)
    if st.session_state.special_event in [
            'チョコ', 'チョコレート', '🍫', 'ショコラ', 'chocolate', 'ちょこ',
            'ちよこれーと', 'ちよこれいと']:
        display()
        question()

def display():
    st.write('お見事！！')
    st.image('https://drive.google.com/uc?export=view&id=1W0TtWXV5O-7emlBPv5OWE3VDBN9Gr1w6&usp=sharing')

def submit():
    options = ', '.join(st.session_state.question)
    text = f'''
＜どうやって？＞
{options}

＜メッセージ＞
{st.session_state.event_message}
'''
    requests.post('https://hemsq-event.herokuapp.com/event',
        headers={"content-type": "application/json"},
        # data=json.dumps({'name': st.session_state.event_name, 'text': text}))
        data=json.dumps({'name': '名無しさん', 'text': text}))
    st.session_state.pages['TOP'].func()

def question():
    st.write('もしよろしければ、アンケートにお答えください！')
    with st.form('question_form'):
        # name = st.text_input('ニックネーム', placeholder='なしでも大丈夫 :)',
        #     key='event_name')
        how = st.multiselect(
            'どのようにして気づきましたか？(複数回答可)',
            options=[
                '適当にいじってたら偶然見つけた',
                'つよつよのダークモードを使っていてバレバレだった',
                'なにかが妙だと思って探った',
                'どれでもない',
            ],
            key='question')
        message = st.text_area('メッセージをもらえると主が嬉しくてニヤニヤします',
            placeholder='もちろんなしでも大丈夫 :)',
            key='event_message')
        st.form_submit_button(
            label='送信',
            on_click=submit,
        )

sukima_text = '...お？おおおおおお？'
