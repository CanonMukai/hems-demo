import streamlit as st

type_and_text = [
    {
        'type': 'text',
        'body': r'''
## 概要

いま脱炭素社会に向けた取り組みがさまざまなところで行われています。住宅分野では、安くエコにエネルギーを使うために太陽光発電や蓄電池を設置する住宅が増えてきています。

そのような住宅では、太陽光発電・蓄電池の設置時に HEMS (Home Energy Management System) を導入することも多いです。HEMS は住宅のエネルギーを管理するためのシステムで、電力の使用を可視化したり、住宅内の電気機器を無線で接続して制御することができます。
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
ここでは HEMS によって制御を行うことを仮定して、発電・蓄電・電力購入を最適に行うスケジュールをアニーリングマシンで作成し、住宅のエネルギー利用を最適化することを考えます。  

どの時間に、どのくらい、発電・蓄電・電力購入を行うと安く・エコになるのか、エネルギーの使い方の選択肢は無数に存在します。アニーリングマシンはこのような膨大な選択肢の中から最適解を選び出すことが得意です。アニーリングマシンを用いて最適なスケジュールを導いてみましょう。
''',
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
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=1SuaTk4Za_SBjvJoTB01O2AsPaMR95RWu&usp=sharing',
        'caption': None,
        'width': 550,
    },
    {
        'type': 'text',
        'body': r'''
スケジュールを作成するには、需要・天気予報・電気代などのデータが必要となります。

入力データを受け取る → アニーリングマシンで最適化を行う → 結果を出力する

という流れに沿ってスケジューリングを行います。
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=187OpYfcneDDMU5PYAOmeY8V2gTdcH8RO&usp=sharing',
        'caption': None,
        'width': 900,
    },
    {
        'type': 'text',
        'body': r'''
## 定式化

### 変数定義
この問題を定式化するため、変数を定義していきます。


前であげた6種の運用それぞれについて、一定の電力量（W）を持つ「項目」を用意します。

下のようなイメージです。ここでは「項目」の電力量は10Wです。
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=1UmiR9us6WcHTEFfpUFpcmaCEQm_zUXyW&usp=sharing',
        'caption': None,
        'width': 400,
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
        'width': 550,
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
        'type': 'text',
        'body': r'''
### コスト項

この問題では電気代（経費コスト）と二酸化炭素排出量（環境コスト）の最小化が目的となります。そのため、コスト項は経費コスト項 $H_\mathrm{expc}$ と環境コスト項$H_\mathrm{envc}$で構成されます。

1. 経費コスト項
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{expc}=\,a\sum_{t=1}^{T}\left[C_\mathrm{ele}(t)\sum_{i\in\mathrm{Ele}}x_{i,t}-C_\mathrm{sun}(t)\sum_{i\in\mathrm{Sun}}x_{i,t}\right]
''',
    },
    {
        'type': 'text',
        'body': r'''
$C_\textrm{ele}$ は商用電源料金、$C_\textrm{sun}$ は太陽光売電価格、$\textrm{Ele}$ は集合 $\{$商用電源使用 $1$ ,...,　商用電源使用 $n_{5}\}$、$\rm{Sun}$ は集合 $\{$太陽光使用$1$ ,...,　太陽光使用$n_{1}\}$ である。この項ではスケジュール通りに運用した場合の経費を計上する。
    
2. 環境コスト項
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{envc}=\,(1-a)\,C_\mathrm{env}\sum_{t=1}^{T}\sum_{i\in\mathrm{Ele}}x_{i,t}
''',
    },
    {
        'type': 'text',
        'body': r'''
$C_\textrm{env}$ は商用電源を使用する際の $\textrm{CO}_{2}$ 排出量に基づく係数である。その指標として $\textrm{CO}_{2}$ 排出係数を用いる。この項ではスケジュール通りに運用した場合に排出される $\textrm{CO}_{2}$ 排出量を計上する。変数 $a$ は $H_\mathrm{envc}$に 対し $H_\mathrm{expc}$ を優先する度合いを示し、$0$ 以上 $1$ 以下の値をとる。$a$ を調節することでスケジューリングにおける経費面と環境面の優先度合を決定する。
''',
    },
    {
        'type': 'text',
        'body': r'''
### 制約項

##### 1. 項目 $i$ を割り当てる時間枠は1枠までとする制約
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{alloc}=\sum_{i\in\mathrm{All}}\left(\sum_{t=1}^{T}x_{i,t}\right)\left(\sum_{t=1}^{T}x_{i,t}-1\right)
''',
    },
    {
        'type': 'text',
        'body': r'''
$H_\mathrm{alloc}$は項目$i$を割り当てる時間枠を1枠までとする制約項である。$\textrm{All}$は項目全体の集合である。


##### 2. 蓄電池の入出力を同時に行わないようにするための制約
''',
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{inout}=\sum_{t=1}^{T}\left(\sum_{i\in\mathrm{In}}x_{i,t}\right)\left(\sum_{i\in\mathrm{Out}}x_{i,t}\right)
''',
    },
    {
        'type': 'text',
        'body': r'''
$\textrm{In}$ は集合 $\{$太陽光充電 $1$ ,..., 太陽光充電 $n_{2}$, 商用電源充電 $1$ ,..., 商用電源充電 $n_{6}\}$、$\textrm{Out}$ は集合 $\{$蓄電池使用 $1$ ,..., 蓄電池使用 $n_{4}\}$ である。

    
##### 3. 需要量を供給量が満たすための制約
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=1EcHxiU4FqUlQiD6evWPwXvc94zJSGpbw&usp=sharing',
        'caption': None,
        'width': 300,
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{demand}=\sum_{t=1}^{T}\left[\sum_{i\in\mathrm{Use}}x_{i,t}-D(t)\right]^2
''',
    },
    {
        'type': 'text',
        'body': r'''
$D$ は需要量、$\textrm{Use}$ は集合 $\{$太陽光使用 $1$ ,..., 太陽光使用 $n_{1}$, 蓄電池使用 $1$ ,..., 蓄電池使用 $n_{4}$, 商用電源使用 $1$ ,..., 商用電源使用 $n_{5}\}$である。

    
##### 4. 太陽光の収支が合うための制約

この制約は各時間において太陽光発電量と太陽光使用・充電・売電量の合計が等しくなるための制約項です。
''',
    },
    {
        'type': 'image',
        'body': 'https://drive.google.com/uc?export=view&id=15kIF6UVHBH2Lr80xLq-7YZbvuwc1kbt6&usp=sharing',
        'caption': None,
        'width': 300,
    },
    {
        'type': 'latex',
        'body': r'''
H_\mathrm{sun}=\sum_{t=1}^{T}\left[\sum_{i\in\textrm{Sun}}x_{i,t}-S(t)\right]^2
''',
    },
    {
        'type': 'text',
        'body': r'''
$S$ は太陽光発電量、$\textrm{Sun}$ は集合 $\{$太陽光使用 $1$ ,..., 太陽光使用 $n_{1}$, 太陽光充電 $1$ ,..., 太陽光充電 $n_{2}$, 太陽光売電 $1$ ,..., 太陽光売電 $n_{3}\}$である。

    
##### 5. 蓄電量が蓄電容量内であるための制約
''',
    },
    {
        'type': 'latex',
        'body': r'''
\forall t \in \{1,...,T\}, \: 0\leq B(t)\leq B_\mathrm{cap} \\
B(0) = B_0, \:B_\mathrm{loss}(t)=\eta B(t) \\
B(t+1) = B(t) + B_\mathrm{loss}(t) + b_\mathrm{in}\sum_{i\in\mathrm{In}}x_{i,t} - b_\mathrm{out}\sum_{i\in\mathrm{Out}}x_{i,t}
''',
    },
    {
        'type': 'text',
        'body': r'''
$B_\mathrm{cap}$ は蓄電池容量、$B_0$ は初期蓄電量、$B_\mathrm{loss}$ は蓄電池の自然放電量、$\eta$ は放電率、$b_\mathrm{in},\,b_\mathrm{out}$ はそれぞれ充電・放電における変換効率、$\textrm{In}$、$\textrm{Out}$ は $H_\mathrm{inout}$ で定義した集合と同義である。

$H_\mathrm{bat}$ は上式の蓄電池容量の不等式制約を表す。変数 $y_{i,t}$ は $0$ または $1$ の値をとる二値変数である。


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
アニーリングマシンでこのハミルトニアンの最小化を行うことで、制約を満たし、かつコストの低いスケジュールを導くことができます。
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

convert(type_and_text)