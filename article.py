import streamlit as st

type_and_text = [
    {
        'type': 'text',
        'body': r'''
## 概要

いま脱炭素社会に向けた取り組みがさまざまなところで行われています。住宅分野では、安くエコにエネルギーを使うために太陽光発電や蓄電池を設置する住宅が増えてきています。

太陽光発電や蓄電池を備える住宅では、どの時間にどのくらいの電力を使い・貯め・売るのか、などエネルギー運用の選択肢が無数に存在します。「HEMS エネルギー利用最適化」はその選択肢の中から安く、かつ環境に優しい運用を選び出すことを目的としています。

近年は太陽光発電・蓄電池の設置時にHEMS(Home Energy Management System)を導入することが増えてきています。HEMSは住宅のエネルギーを管理するためのシステムで、電力の使用を可視化したり、住宅内の電気機器を無線で接続して制御することができます。
''',
    },
    {
        'type': 'markdown',
        'body': '''
<div style="text-align: center">
    <figure>
        <img src="https://drive.google.com/uc?export=view&id=1qOPQvru_tcXQ3myIAZQ7its_igPGlVSW&usp=sharing"
            width='300'>
        <figcaption>出典 iエネ コンソーシアム「HEMSとは？」</figcaption>
    </figure>
</div>
''',
    },
    {
        'type': 'text',
        'body': r'''
「HEMS エネルギー利用最適化」は、このHEMSを利用することを想定しています。アニーリングマシンを利用してエネルギーを最適に運用するスケジュールを導き、そのスケジュールをもとにHEMSでエネルギー制御を行うことで、住宅のエネルギー利用の最適化を目指します。
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
## 作成するスケジュール

いま住宅のエネルギーが図のように運用されるとします。

矢印は6つあり、それぞれ以下の6種の運用を表しています。
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=1-6ckB3YvEBIcfIwHuKf0b0mO4dtUZpoe&usp=sharing',
        'caption': None,
        'width': 300,
    },
    {
        'type': 'text',
        'body': r'''
- 太陽光使用 
- 太陽光充電 
- 太陽光売電 
- 蓄電池使用 
- 商用電源使用 
- 商用電源充電 


この6種の運用について各時間で電力量を決定しスケジュールを作成します。

時間解像度は1時間とします。例えばこのようなスケジュールが出力されます。
''',
    },
    # {
    #     'type': 'image',
    #     'body': 'https://drive.google.com/uc?export=view&id=1SuaTk4Za_SBjvJoTB01O2AsPaMR95RWu&usp=sharing',
    #     'caption': None,
    #     'width': 550,
    # },
    {
        'type': 'text',
        'body': r'''
スケジュールを作成するには、需要・天気予報・電気代などのデータが必要となります。したがって以下の流れでスケジューリングを行います。

1. 入力データを受け取る
2. アニーリングマシンで最適化を行う
3. 結果を出力する
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=187OpYfcneDDMU5PYAOmeY8V2gTdcH8RO&usp=sharing',
        'caption': None,
        'width': 700,
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
## 定式化

### 変数定義
この問題を定式化するため、変数を定義していきます。


前であげた6種の運用それぞれについて、一定の電力量（W）を持つ「項目」を用意します。

下のようなイメージです。ここでは「項目」の電力量は10Wです。

ここでは太陽光を「光」蓄電池を「電池」商用電源を「電源」と省略して表記しています。
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=1UmiR9us6WcHTEFfpUFpcmaCEQm_zUXyW&usp=sharing',
        'caption': None,
        'width': 450,
    },
    {
        'type': 'text',
        'body': r'''
この「項目」を各時間枠に適切な数、割り当てていくことでスケジュールを作成していきます。
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=1ItK9vtsgIVc-KFZWmZs2ss3u8RnbBGv9&usp=sharing',
        'caption': None,
        'width': 700,
    },
    {
        'type': 'text',
        'body': r'''
二値変数 $x_{i,t}$ は、項目 $i$ を時間枠$t$に割り当てる場合に $1$、割り当てない場合に $0$ となるように定義します。
''',
    },
    {
        'type': 'latex',
        'body': r'''
x = \begin{cases}
   1 &\text{項目 $i$ を時間枠 $t$ に割り当てるとき}\\
   0 &\text{割り当てないとき}
\end{cases}''',
    },
    {
        'type': 'text',
        'body': r'''
項目は次のように用意しておきます。

- 太陽光使用 $i\:(\:i=1,...,n_{1}\:)$
- 太陽光充電 $i\:(\:i=1,...,n_{2}\:)$
- 太陽光売電 $i\:(\:i=1,...,n_{3}\:)$
- 蓄電池使用 $i\:(\:i=1,...,n_{4}\:)$
- 商用電源使用 $i\:(\:i=1,...,n_{5}\:)$
- 商用電源充電 $i\:(\:i=1,...,n_{6}\:)$
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
### コスト項

この問題の目的は電気代（経費コスト）と $\textrm{CO}_{2}$ 排出量（環境コスト）の最小化です。そのためコスト項は経費コスト項 $H_\mathrm{expc}$ と環境コスト項 $H_\mathrm{envc}$ で構成します。
また以下式に現れる変数 $a$ は、$H_\mathrm{envc}$ と $H_\mathrm{expc}$ の重みを調節するための変数であり、$0$ 以上 $1$ 以下の値をとります。変数 $a$ の値により、スケジューリングにおける経費面と環境面の優先度合を決定することができます。

##### 1. 経費コスト項

$C_\textrm{ele}$ は商用電源の料金、$\textrm{Ele}$ は集合 $\{$商用電源使用 $1$, $\dots$ , 商用電源使用 $n_{5}$, 商用電源充電 $1$, $\ldots$ , 商用電源充電 $n_{6}\}$ であり、$C_\textrm{sun}$ は太陽光の売電価格、$\rm{Sun}$ は集合 $\{$太陽光使用 $1$, $\dots$ , 太陽光使用 $n_{1}\}$ とします。商用電源から買った分（第1項）から太陽光を売った分（第2項）を引くと、スケジュール全体でかかった料金は以下の式で表せます。
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{expc}=\,a\sum_{t=1}^{T}\left[C_\mathrm{ele}(t)\sum_{i\in\mathrm{Ele}}x_{i,t}-C_\mathrm{sun}(t)\sum_{i\in\mathrm{Sun}}x_{i,t}\right]
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
##### 2. 環境コスト項

環境コストは商用電源を買うことにより発生する $\textrm{CO}_{2}$ 排出量を示し、以下の式で表します。$C_\textrm{env}$ は商用電源を買うことで発生する [$\textrm{CO}_{2}$ 排出量](https://ghg-santeikohyo.env.go.jp/files/calc/r03_coefficient_rev.pdf)をもとにした係数です。
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{envc}=\,(1-a)\,C_\mathrm{env}\sum_{t=1}^{T}\sum_{i\in\mathrm{Ele}}x_{i,t}
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
### 制約項

##### 1. 1つの項目を割り当てる時間枠は1枠までとする制約

1つの項目はの高々1つの時間枠にしか割り当ててはいけないため、1つの項目が2つ以上の時間枠に割り当てられたとき、値が大きくなるよう制約を与えます。$\textrm{All}\:$ は項目全体の集合を表しています。
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{alloc}=\sum_{i\in\mathrm{All}}\left(\sum_{t=1}^{T}x_{i,t}\right)\left(\sum_{t=1}^{T}x_{i,t}-1\right)
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
##### 2. 蓄電池の充放電を同時に行わないための制約

蓄電池は充放電を同時にすることができません。そのため、充電の項目と放電（蓄電池の使用）の項目が同時間枠に割り当てられたとき、値が大きくなるように制約を与えます。充電の項目集合 $\:\textrm{In}\:$ は集合 $\{$太陽光充電 $1$ , $\dots$ , 太陽光充電 $n_{2}$, 商用電源充電 $1$ , $\dots$ , 商用電源充電 $n_{6}\}$、放電（蓄電池の使用）の項目集合 $\:\textrm{Out}\:$ は集合 $\{$蓄電池使用 $1$ , $\dots$ , 蓄電池使用 $n_{4}\}$ です。
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{inout}=\sum_{t=1}^{T}\left(\sum_{i\in\mathrm{In}}x_{i,t}\right)\left(\sum_{i\in\mathrm{Out}}x_{i,t}\right)
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
##### 3. 需要量を供給量が満たすための制約

需要を供給が満たす必要があるため、各時間で需要と太陽光・蓄電池・商用電源の使用量の和が等しくなるように制約を与えます。
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=1EcHxiU4FqUlQiD6evWPwXvc94zJSGpbw&usp=sharing',
        'caption': None,
        'width': 300,
    },
    {
        'type': 'text',
        'body': r'''
入力として受け取った需要のデータは項目あたりの電力量で割り、$D$（単位はW）として用意しておきます。この $D$ の値と合うように「使用」の項目を割り当てます。使用の項目集合 $\textrm{Use}$ は、集合 $\{$太陽光使用 $1$ , $\dots$ , 太陽光使用 $n_{1}$, 蓄電池使用 $1$ , $\dots$ , 蓄電池使用 $n_{4}$, 商用電源使用 $1$ , $\dots$ , 商用電源使用 $n_{5}\}$ です。需要と供給が合わないとき、項の値は大きくなります。
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{demand}=\sum_{t=1}^{T}\left[\sum_{i\in\mathrm{Use}}x_{i,t}-D(t)\right]^2
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
##### 4. 太陽光の収支が合うための制約

太陽光で発電された電力は無駄にならないよう、必ず使用か充電か売電がなされるとします。そのため、各時間枠で太陽光発電量と太陽光使用・充電・売電量の和が等しくなるように（収支が合うように）制約を与えます。
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=15kIF6UVHBH2Lr80xLq-7YZbvuwc1kbt6&usp=sharing',
        'caption': None,
        'width': 300,
    },
    {
        'type': 'text',
        'body': r'''
入力として受け取った天気予報データから太陽光発電量を算出し、項目あたりの電力量で割った $S$（単位はW）を用意し、この $S$ の値と合うように「太陽光」の項目を割り当てます。太陽光の項目集合 $\textrm{Sun}$ は集合 $\{$太陽光使用 $1$ , $\dots$ , 太陽光使用 $n_{1}$, 太陽光充電 $1$ ,..., 太陽光充電 $n_{2}$, 太陽光売電 $1$ , $\dots$ , 太陽光売電 $n_{3}\}$です。太陽光の収支が合わないとき、項の値は大きくなります。
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{sun}=\sum_{t=1}^{T}\left[\sum_{i\in\textrm{Sun}}x_{i,t}-S(t)\right]^2
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
##### 5. 蓄電量が蓄電容量内であるための制約

最後に、蓄電量が蓄電容量内であるための制約を与えます。時間枠 $t$ において蓄電池に蓄えられている電力を $B(t)$ とします。

まず初めに入力として受け取った初期蓄電量を項目あたりの電力量で割り $B_{0}$（単位はW）とします。すると初めの蓄電量 $B(0)$について、以下の式が成り立ちます。
''',
    },
#     {
#         'type': 'latex',
#         'body': r'''
# \forall t \in \{1,...,T\}, \: 0\leq B(t)\leq B_\mathrm{cap} \\
# B(0) = B_0, \:B_\mathrm{loss}(t)=\eta B(t) \\
# B(t+1) = B(t) + B_\mathrm{loss}(t) + b_\mathrm{in}\sum_{i\in\mathrm{In}}x_{i,t} - b_\mathrm{out}\sum_{i\in\mathrm{Out}}x_{i,t}
# ''',
#     },
    {
        'type': 'latex',
        'body': r'''
B(0) = B_0
''',
    },
    {
        'type': 'text',
        'body': r'''
蓄電池に蓄えられている電力は時間とともに自然放電していきます。放電率を $\eta$ とすると時間枠 $t$ における電力の損失 $B_\textrm{loss}(t)$ は以下の式で表されます。
''',
    },
    {
        'type': 'latex',
        'body': r'''
B_\mathrm{loss}(t)=\eta B(t)
''',
    },
    {
        'type': 'text',
        'body': r'''
蓄電池は太陽光や商用電源から充電されたり、蓄電池の使用や自然放電によって放電されたりして、時間とともに蓄電量の増減を繰り返していきます。$b_\mathrm{in},\,b_\mathrm{out}$ をそれぞれ充電・放電における変換効率、$\textrm{In},\,\textrm{Out}$ を2つ目の制約項 $H_\mathrm{inout}$ で定義した集合と同じものとします。時間枠 $t$ の蓄電量 $B(t)$ を用いて、次の時間枠 $t+1$ における蓄電量 $B(t+1)$ は以下の式で表すことができます。右辺の第3項は時間枠 $t$ で充電された量、第4項は放電された量を表しています。
''',
    },
    {
        'type': 'latex',
        'body': r'''
B(t+1) = B(t) - B_\mathrm{loss}(t) + b_\mathrm{in}\sum_{i\in\mathrm{In}}x_{i,t} - b_\mathrm{out}\sum_{i\in\mathrm{Out}}x_{i,t}
''',
    },
    {
        'type': 'text',
        'body': r'''
蓄電量は常に蓄電池容量内でなければいけません。蓄電池容量を $B_\textrm{cap}$ として、各時間枠で以下の不等式が成り立っている必要があります。
''',
    },
    {
        'type': 'latex',
        'body': r'''
 \: 0\leq B(t)\leq B_\mathrm{cap},\quad \:\forall t \in \{1, \dots ,T\} \tag{$\ast$}
''',
    },
    {
        'type': 'text',
        'body': r'''
式 $(\ast)$ の不等式は $0$ または $1$ の値をとる二値変数 $y_{i,t}$ を導入すると、以下のような制約項として表現することができます。式 $(\ast)$ の不等式を満たさないとき、制約項 $H_\textrm{bat}$ は正の値をとります。
''',
    },
    {
        'type': 'latex',
        'body': r'''
 H_\mathrm{bat}=\gamma_\textrm{b}\sum_{t=1}^{T}\left[B_\mathrm{cap}-B(t)-\sum_{n=0}^{\lfloor\log_2 (B_\mathrm{cap}-1)\rfloor}2^ny_{i,t}\right]^2
''',
    },
    {
        'type': 'text',
        'body': r'''
ここでは詳細を省きますが、不等式を上記のような制約項として表現する過程について知りたい方はOpenJijチュートリアルの[Knapsack問題](https://openjij.github.io/OpenJijTutorial/build/html/ja/008-KnapsackPyqubo.html)を参考にしてください。

以上でコスト項と制約項について定式化することができました。
''',
    },
    {
        'type': 'blank',
        'num': 1,
    },
    {
        'type': 'text',
        'body': r'''
### 最小化するハミルトニアン

制約項の重みをそれぞれ $\gamma_\mathrm{c}, \gamma_\mathrm{a},\gamma_\mathrm{io},\gamma_\mathrm{d},\gamma_\mathrm{s},\gamma_\mathrm{b}$ とすると、ハミルトニアンは次のように表されます。

''',
    },
    {
        'type': 'latex',
        'body': r'''
H = \gamma_\mathrm{c}H_\mathrm{expc} + \gamma_\mathrm{c}H_\mathrm{envc} + \gamma_\mathrm{a}H_\mathrm{alloc} + \gamma_\mathrm{io}H_\mathrm{inout} + \gamma_\mathrm{d}H_\mathrm{demand} + \gamma_\mathrm{s}H_\mathrm{sun} + \gamma_\mathrm{b}H_\mathrm{bat}
''',
    },
    {
        'type': 'text',
        'body': r'''
このハミルトニアンの最小化を行うことで、制約を満たすコストの低いスケジュールを導くことができます。
''',
    },
]


def convert(type_and_text):
    for t in type_and_text:
        if t['type'] == 'text':
            st.write(t['body'])
        elif t['type'] == 'image':
            st.image(t['body'], caption=t['caption'], width=t['width'])
        elif t['type'] == 'latex':
            st.latex(t['body'])
        elif t['type'] == 'markdown':
            st.markdown(t['body'], unsafe_allow_html=True)
        elif t['type'] == 'blank':
            st.markdown('<br>'*t['num'], unsafe_allow_html=True)

convert(type_and_text)