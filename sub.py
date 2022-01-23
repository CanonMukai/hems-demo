import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots as ms

def my_round(val, digit=0):
    p = 10 ** digit
    rounded = (val * p * 2 + 1) // 2 / p
    return int(rounded) if digit == 0 else rounded

def modified_df(df):
    columns = [
        '需要 (W)', '太陽光発電量 (W)', '商用電源料金 (円/W)', '太陽光売電価格 (円/W)',
        '太陽光使用量 (W)', '太陽光充電量 (W)', '太陽光売上量 (W)', '蓄電使用量 (W)',
        '商用電源使用量 (W)', '商用電源充電量 (W)', '残りの蓄電量 (W)']
    df2 = df.T
    df2.columns = columns
    return df2

def plotly_demand_graph(df):
    '''
    input: modified_df
    output: plotly fig
    '''
    fig = ms(rows=1, cols=1, specs=[[{'secondary_y': True}]])
    fig.add_bar(
        x=df.index, y=df['需要 (W)'], name='需要 (W)',
        offsetgroup='left', marker=dict(color='gray'))
    fig.add_bar(
        x=df.index, y=df['太陽光使用量 (W)'], name='太陽光使用量 (W)',
        offsetgroup='right', marker=dict(color='coral'))
    fig.add_bar(
        x=df.index, y=df['蓄電使用量 (W)'], name='蓄電使用量 (W)',
        offsetgroup='right', base=df['太陽光使用量 (W)'],
        marker=dict(color='deepskyblue'))
    fig.add_bar(
        x=df.index, y=df['商用電源使用量 (W)'], name='商用電源使用量 (W)',
        offsetgroup='right', base=df['太陽光使用量 (W)'] + df['蓄電使用量 (W)'],
        marker=dict(color='limegreen'))
    
    trace0 = go.Scatter(
        x=df.index, y=df['商用電源料金 (円/W)'], name='商用電源料金 (円/W)',
        line=dict(color='green'))
    fig.add_trace(trace0, secondary_y=True)
    trace1 = go.Scatter(
        x=df.index, y=df['太陽光売電価格 (円/W)'], name='太陽光売電価格 (円/W)',
        line=dict(color='orange'))
    fig.add_trace(trace1, secondary_y=True)

    fig.update_xaxes(title_text='時間', showgrid=False)
    fig.update_yaxes(title_text='電力量 (W)', showgrid=False)
    fig.update_yaxes(title_text='商用電源価格 (円/W)', showgrid=False, secondary_y=True)
    fig.update_layout(title='需要と供給')
    return fig

def plotly_solar_graph(df):
    '''
    input: modified_df
    output: plotly fig
    '''
    fig = ms(rows=1, cols=1, specs=[[{'secondary_y': True}]])
    fig.add_bar(
        x=df.index, y=df['太陽光発電量 (W)'], name='太陽光発電量 (W)',
        offsetgroup='left', marker=dict(color='lightgray'))
    fig.add_bar(
        x=df.index, y=df['太陽光使用量 (W)'], name='太陽光使用量 (W)',
        offsetgroup='right', marker=dict(color='coral'))
    fig.add_bar(
        x=df.index, y=df['太陽光充電量 (W)'], name='太陽光充電量 (W)',
        offsetgroup='right', base=df['太陽光使用量 (W)'],
        marker=dict(color='gold'))
    fig.add_bar(
        x=df.index, y=df['太陽光売上量 (W)'], name='太陽光売上量 (W)',
        offsetgroup='right', base=df['太陽光使用量 (W)'] + df['太陽光充電量 (W)'],
        marker=dict(color='aqua'))
    
    trace0 = go.Scatter(
        x=df.index, y=df['商用電源料金 (円/W)'], name='商用電源料金 (円/W)',
        line=dict(color='green'))
    fig.add_trace(trace0, secondary_y=True)
    trace1 = go.Scatter(
        x=df.index, y=df['太陽光売電価格 (円/W)'], name='太陽光売電価格 (円/W)',
        line=dict(color='orange'))
    fig.add_trace(trace1, secondary_y=True)

    fig.update_xaxes(title_text='時間', showgrid=False)
    fig.update_yaxes(title_text='電力量 (W)', showgrid=False)
    fig.update_yaxes(title_text='太陽光売電価格 (円/W)', showgrid=False, secondary_y=True)
    fig.update_layout(title='太陽光の収支')
    return fig
