import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots as ms

def my_round(val, digit=0):
    p = 10 ** digit
    rounded = (val * p * 2 + 1) // 2 / p
    return int(rounded) if digit == 0 else rounded


def plotly_demand_graph(df):
    columns = [
        '需要 (W)', '太陽光発電量 (W)', '商用電源料金 (円/W)', '太陽光売電価格 (円/W)',
        '太陽光使用量 (W)', '太陽光充電量 (W)', '太陽光売上量 (W)', '蓄電使用量 (W)',
        '商用電源使用量 (W)', '商用電源充電量 (W)', '残りの蓄電量 (W)']
    df2 = df.T
    df2.columns = columns
    df['時間'] = df.index
    # df.index = pd.RangeIndex(start=0, stop=24, step=1)
    fig = ms(rows=1, cols=1, specs=[[{'secondary_y': True}]])
    fig.add_bar(
        x=df2.index, y=df2['需要 (W)'], name='需要 (W)',
        offsetgroup='left', marker=dict(color="gray"))
    fig.add_bar(
        x=df2.index, y=df2['太陽光使用量 (W)'], name='太陽光使用量 (W)',
        offsetgroup='right', marker=dict(color='red'))
    fig.add_bar(
        x=df2.index, y=df2['蓄電使用量 (W)'], name='蓄電使用量 (W)',
        offsetgroup='right', base=df2['太陽光使用量 (W)'], marker=dict(color='lime'))
    fig.add_bar(
        x=df2.index, y=df2['商用電源使用量 (W)'], name='商用電源使用量 (W)',
        offsetgroup='right',base=df2['蓄電使用量 (W)'], marker=dict(color='blue'))
    fig.update_yaxes(title_text='Production or Consumption')
    return fig
