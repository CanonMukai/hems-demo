text_css = f'''
<style>
    .hide {{
        color: rgba(0, 0, 0, 0);
    }}
    .hide:hover {{
        color: rgba(0, 255, 200, 0.15);
    }}
    .hide::selection {{
        color: lightblue;
    }}
    ::-moz-selection {{
        color: lightblue;
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
'''

text_input_css = f"""
<style>
.stTextInput>label {{
    color: rgba(0, 0, 0, 0);
}}
.stTextInput>label:hover {{
    color: rgba(0, 255, 200, 0.1);
}}
.stTextInput>label::selection {{
    color: lightblue;
}}
.stTextInput>div {{
    background-color: rgba(0, 0, 0, 0);
    border-color: rgba(0, 0, 0, 0);
    outline-color: rgba(0, 0, 0, 0);
}}
.stTextInput>div>div {{
    background-color: rgba(0, 0, 0, 0);
}}
.stTextInput>div>div>input {{
    color: rgb(100, 100, 100);
}}
.stTextInput>div>div>input::placeholder {{
    color: rgba(0, 0, 0, 0);
}}
.stTextInput>div>div>input:focus::placeholder {{
    color: rgb(200, 200, 200);
}}
.stTextInput>div>div>input:focus {{
    background-color: rgb(230, 250, 255);
}}
</style>
"""

colab_button_css = '''
<style>
.colab {
    color: #fff;
    background: linear-gradient(to bottom, darkorange, #ffc000);
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 500;
    border-radius: 100px;
    border: none;
    cursor: pointer;
}
.colab:hover {
    outline: none;
    box-shadow: 0 0 0 4px rgba(255, 197, 30, 0.4), 0 8px 10px 8px rgba(255, 197, 30, 0.10);
}
.colab:focus {
    color: orange;
    background: #fff;
    outline: none;
    box-shadow: 0 0 0 4px orange;
}
</style>
'''