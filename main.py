import streamlit as st
from annealing import *

# ページ全体の設定
st.set_page_config(
    page_title='HEMSデモ',
    page_icon='🏠',
    layout='wide',
    initial_sidebar_state='expanded',
)

def main():
    make_body()
    make_sidebar()

def make_body():
    st.text('Coming soon.')

def make_sidebar():
    st.sidebar.text('Coming soon.')

if __name__ == '__main__':
    main()
