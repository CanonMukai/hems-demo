import streamlit as st

_article_text = r'''
# エネルギー利用最適化

## 概要

いま脱炭素社会に向けた取り組みがさまざまなところで行われています。住宅分野では、安くエコにエネルギーを使うために太陽光発電や蓄電池を設置する住宅が増えてきています。

そのような住宅では、太陽光発電・蓄電池の設置時にHEMS(Home Energy Management System)を導入することも多いです。HEMSは住宅のエネルギーを管理するためのシステムで、電力の使用を可視化したり、住宅内の電気機器を無線で接続して制御することができます。

<img src="img/hems.png" width='300'>
<br />
<center>出典 iエネ コンソーシアム「HEMSとは？」</center>

ここではHEMSによって制御を行うことを仮定して、発電・蓄電・電力購入を最適に行うスケジュールをアニーリングマシンで作成し、住宅のエネルギー利用を最適化することを考えます。  

どの時間に、どのくらい、発電・蓄電・電力購入を行うと安く・エコになるのか、エネルギーの使い方の選択肢は無数に存在します。アニーリングマシンはこのような膨大な選択肢の中から最適解を選び出すことが得意です。アニーリングマシンを用いて最適なスケジュールを導いてみましょう。


## 作成するスケジュール

いま住宅のエネルギーが図のように運用されるとします。<br>
矢印は6つあり、それぞれ以下の6種の運用を表しています。
<img src="img/model.pdf" width='250' align="right">
<!--<ul>
    <li>太陽光使用</li>
    <li>太陽光充電</li>
    <li>太陽光売電</li>
    <li>蓄電池使用</li>
    <li>商用電源使用</li>
    <li>商用電源充電</li>
</ul>-->
- 太陽光使用 
- 太陽光充電 
- 太陽光売電 
- 蓄電池使用 
- 商用電源使用 
- 商用電源充電 
<br><br><br><br>
この6種の運用について各時間で電力量を決定しスケジュールを作成します。<br>時間解像度は1時間とします。例えばこのようなスケジュールが出力されます。
<img src="img/output.png" width='400' align="center">
スケジュールを作成するには、需要・天気予報・電気代などのデータが必要となります。<br>
入力データを受け取る→アニーリングマシンで最適化を行う→結果を出力する<br>
という流れに沿ってスケジューリングを行います。
<!-- <br>（入力ー＞出力　の図） -->
<img src="img/入力と出力.pdf" width='800' align="center">


## 定式化

### 変数定義
この問題を定式化するため、変数を定義していきます。

前であげた6種の運用それぞれについて、一定の電力量（W）を持つ「項目」を用意します。<br>
下のようなイメージです。ここでは「項目」の電力量は10Wです。

<img src="img/項目とは.pdf" width='400' align="center">

この「項目」を各時間枠に適切な数、割り当てていくことでスケジュールを作成していきます。
<img src="img/項目割り当て.pdf" width='400' align="center">
二値変数$x_{i,t}$は、項目$i$を時間枠$t$に割り当てる場合に$1$、割り当てない場合に$0$となるように定義します。  

$$
x_{i,t} =
    \begin{cases}
        1 \quad \mbox{項目$i$を時間枠$t$に割り当てるとき}\\
        0 \quad \mbox{割り当てないとき}\\
    \end{cases}
$$

項目は次のように用意しておきます。

- 太陽光使用 $i\:(\:i=1,...,n_{1}\:)$
- 太陽光充電 $i\:(\:i=1,...,n_{2}\:)$
- 太陽光売電 $i\:(\:i=1,...,n_{3}\:)$
- 蓄電池使用 $i\:(\:i=1,...,n_{4}\:)$
- 商用電源使用 $i\:(\:i=1,...,n_{5}\:)$
- 商用電源充電 $i\:(\:i=1,...,n_{6}\:)$


### コスト項

この問題では電気代（経費コスト）と二酸化炭素排出量（環境コスト）の最小化が目的となります。そのため、コスト項は経費コスト項$H_\mathrm{expc}$と環境コスト項$H_\mathrm{envc}$で構成されます。

1. 経費コスト項
$$
H_\mathrm{expc}=\,a\sum_{t=1}^{T}\left[C_\mathrm{ele}(t)\sum_{i\in\mathrm{Ele}}x_{i,t}-C_\mathrm{sun}(t)\sum_{i\in\mathrm{Sun}}x_{i,t}\right] 
$$

    <br>$C_\textrm{ele}$は商用電源料金、$C_\textrm{sun}$は太陽光売電価格、$\textrm{Ele}$は集合$\{$商用電源使用$1$ ,...,　商用電源使用$n_{5}\}$、$\rm{Sun}$は集合$\{$太陽光使用$1$ ,...,　太陽光使用$n_{1}\}$である。この項ではスケジュール通りに運用した場合の経費を計上する。
    
2. 環境コスト項
$$
H_\mathrm{envc}=\,(1-a)\,C_\mathrm{env}\sum_{t=1}^{T}\sum_{i\in\mathrm{Ele}}x_{i,t}
$$

    <br>$C_\textrm{env}$は商用電源を使用する際の$\textrm{CO}_{2}$排出量に基づく係数である。その指標として$\textrm{CO}_{2}$排出係数を用いる。この項ではスケジュール通りに運用した場合に排出される$\textrm{CO}_{2}$排出量を計上する。変数$a$は$H_\mathrm{envc}$に対し$H_\mathrm{expc}$を優先する度合いを示し、0以上1以下の値をとる。$a$を調節することでスケジューリングにおける経費面と環境面の優先度合を決定する。

### 制約項

1. 項目\$i$を割り当てる時間枠は1枠までとする制約<br><br>
$$ H_\mathrm{alloc}=\sum_{i\in\mathrm{All}}\left(\sum_{t=1}^{T}x_{i,t}\right)\left(\sum_{t=1}^{T}x_{i,t}-1\right)
$$

    $H_\mathrm{alloc}$は項目$i$を割り当てる時間枠を1枠までとする制約項である。$\textrm{All}$は項目全体の集合である。<br>
    
    
2. 蓄電池の入出力を同時に行わないようにするための制約<br><br>
$$
H_\mathrm{inout}=\sum_{t=1}^{T}\left(\sum_{i\in\mathrm{In}}x_{i,t}\right)\left(\sum_{i\in\mathrm{Out}}x_{i,t}\right)
$$

    $\textrm{In}$は集合$\{$太陽光充電$1$ ,..., 太陽光充電$n_{2}$, 商用電源充電$1$ ,..., 商用電源充電$n_{6}\}$、$\textrm{Out}$は集合$\{$蓄電池使用$1$ ,..., 蓄電池使用$n_{4}\}$である。<br><br>
    
3. 需要量を供給量が満たすための制約<br>
<p><img src="img/H_demand.pdf" width='250'align="right"><br>
$$
 H_\mathrm{demand}=\sum_{t=1}^{T}\left[\sum_{i\in\mathrm{Use}}x_{i,t}-D(t)\right]^2
$$
    <br>$D$は需要量、$\textrm{Use}$は集合$\{$太陽光使用$1$ ,..., 太陽光使用$n_{1}$, 蓄電池使用$1$ ,..., 蓄電池使用$n_{4}$, 商用電源使用$1$ ,..., 商用電源使用$n_{5}\}$である。</p><br>
    
4. 太陽光の収支が合うための制約

    この制約は各時間において太陽光発電量と太陽光使用・充電・売電量の合計が等しくなるための制約項です。
<p><img src="img/H_sun.pdf" width='250'align="right"><br>
$$
 H_\mathrm{sun}=\sum_{t=1}^{T}\left[\sum_{i\in\textrm{Sun}}x_{i,t}-S(t)\right]^2
$$
    <br>$S$は太陽光発電量、$\textrm{Sun}$は集合$\{$太陽光使用$1$ ,..., 太陽光使用$n_{1}$, 太陽光充電$1$ ,..., 太陽光充電$n_{2}$, 太陽光売電$1$ ,..., 太陽光売電$n_{3}\}$である。</p><br>
    
5. 蓄電量が蓄電容量内であるための制約<br><br>
$$
\forall t \in \{1,...,T\}, \: 0\leq B(t)\leq B_\mathrm{cap} \nonumber \\
B(0) = B_0, \:B_\mathrm{loss}(t)=\eta B(t)\nonumber\\
B(t+1) = B(t) + B_\mathrm{loss}(t) + b_\mathrm{in}\sum_{i\in\mathrm{In}}x_{i,t} - b_\mathrm{out}\sum_{i\in\mathrm{Out}}x_{i,t}\nonumber
$$

    $B_\mathrm{cap}$は蓄電池容量、$B_0$は初期蓄電量、$B_\mathrm{loss}$は蓄電池の自然放電量、$\eta$は放電率、$b_\mathrm{in},\,b_\mathrm{out}$はそれぞれ充電・放電における変換効率、$\textrm{In}$、$\textrm{Out}$は$H_\mathrm{inout}$で定義した集合と同義である。<br><br>$H_\mathrm{bat}$は上式の蓄電池容量の不等式制約を表す。変数$y_{i,t}$は0または1の値をとる二値変数である。<br><br>
$$
 H_\mathrm{bat}=\gamma_\textrm{b}\sum_{t=1}^{T}\left[B_\mathrm{cap}-B(t)-\sum_{n=0}^{\lfloor\log_2 (B_\mathrm{cap}-1)\rfloor}2^ny_{i,t}\right]^2
$$

### 最小化するハミルトニアン

制約項の重みをそれぞれ $\gamma_\mathrm{c}, \gamma_\mathrm{a},\gamma_\mathrm{io},\gamma_\mathrm{d},\gamma_\mathrm{s},\gamma_\mathrm{b}$とすると、ハミルトニアンは次のように表されます。<br>

$$
H = \gamma_\mathrm{c}H_\mathrm{expc} + \gamma_\mathrm{c}H_\mathrm{envc} + \gamma_\mathrm{a}H_\mathrm{alloc} + \gamma_\mathrm{io}H_\mathrm{inout} + \gamma_\mathrm{d}H_\mathrm{demand} + \gamma_\mathrm{s}H_\mathrm{sun} + \gamma_\mathrm{b}H_\mathrm{bat}
$$<br>
アニーリングマシンでこのハミルトニアンの最小化を行うことで、制約を満たし、かつコストの低いスケジュールを導くことができます。
'''


article_text = r'''
### コスト項

この問題では電気代（経費コスト）と二酸化炭素排出量（環境コスト）の最小化が目的となります。そのため、コスト項は経費コスト項$H_\mathrm{expc}$と環境コスト項$H_\mathrm{envc}$で構成されます。

1. 経費コスト項
$$
H_\mathrm{expc}=\,a\sum_{t=1}^{T}\left[C_\mathrm{ele}(t)\sum_{i\in\mathrm{Ele}}x_{i,t}-C_\mathrm{sun}(t)\sum_{i\in\mathrm{Sun}}x_{i,t}\right] 
$$

    <br>$C_\textrm{ele}$は商用電源料金、$C_\textrm{sun}$は太陽光売電価格、$\textrm{Ele}$は集合$\{$商用電源使用$1$ ,...,　商用電源使用$n_{5}\}$、$\rm{Sun}$は集合$\{$太陽光使用$1$ ,...,　太陽光使用$n_{1}\}$である。この項ではスケジュール通りに運用した場合の経費を計上する。
    
2. 環境コスト項
$$
H_\mathrm{envc}=\,(1-a)\,C_\mathrm{env}\sum_{t=1}^{T}\sum_{i\in\mathrm{Ele}}x_{i,t}
$$

    <br>$C_\textrm{env}$は商用電源を使用する際の$\textrm{CO}_{2}$排出量に基づく係数である。その指標として$\textrm{CO}_{2}$排出係数を用いる。この項ではスケジュール通りに運用した場合に排出される$\textrm{CO}_{2}$排出量を計上する。変数$a$は$H_\mathrm{envc}$に対し$H_\mathrm{expc}$を優先する度合いを示し、0以上1以下の値をとる。$a$を調節することでスケジューリングにおける経費面と環境面の優先度合を決定する。

### 制約項

1. 項目\$i$を割り当てる時間枠は1枠までとする制約<br><br>
$$ H_\mathrm{alloc}=\sum_{i\in\mathrm{All}}\left(\sum_{t=1}^{T}x_{i,t}\right)\left(\sum_{t=1}^{T}x_{i,t}-1\right)
$$

    $H_\mathrm{alloc}$は項目$i$を割り当てる時間枠を1枠までとする制約項である。$\textrm{All}$は項目全体の集合である。<br>
    
    
2. 蓄電池の入出力を同時に行わないようにするための制約<br><br>
$$
H_\mathrm{inout}=\sum_{t=1}^{T}\left(\sum_{i\in\mathrm{In}}x_{i,t}\right)\left(\sum_{i\in\mathrm{Out}}x_{i,t}\right)
$$

    $\textrm{In}$は集合$\{$太陽光充電$1$ ,..., 太陽光充電$n_{2}$, 商用電源充電$1$ ,..., 商用電源充電$n_{6}\}$、$\textrm{Out}$は集合$\{$蓄電池使用$1$ ,..., 蓄電池使用$n_{4}\}$である。<br><br>
    
3. 需要量を供給量が満たすための制約<br>
<p><img src="img/H_demand.pdf" width='250'align="right"><br>
$$
 H_\mathrm{demand}=\sum_{t=1}^{T}\left[\sum_{i\in\mathrm{Use}}x_{i,t}-D(t)\right]^2
$$
    <br>$D$は需要量、$\textrm{Use}$は集合$\{$太陽光使用$1$ ,..., 太陽光使用$n_{1}$, 蓄電池使用$1$ ,..., 蓄電池使用$n_{4}$, 商用電源使用$1$ ,..., 商用電源使用$n_{5}\}$である。</p><br>
    
4. 太陽光の収支が合うための制約

    この制約は各時間において太陽光発電量と太陽光使用・充電・売電量の合計が等しくなるための制約項です。
<p><img src="img/H_sun.pdf" width='250'align="right"><br>
$$
 H_\mathrm{sun}=\sum_{t=1}^{T}\left[\sum_{i\in\textrm{Sun}}x_{i,t}-S(t)\right]^2
$$
    <br>$S$は太陽光発電量、$\textrm{Sun}$は集合$\{$太陽光使用$1$ ,..., 太陽光使用$n_{1}$, 太陽光充電$1$ ,..., 太陽光充電$n_{2}$, 太陽光売電$1$ ,..., 太陽光売電$n_{3}\}$である。</p><br>
    
5. 蓄電量が蓄電容量内であるための制約<br><br>
$$
\forall t \in \{1,...,T\}, \: 0\leq B(t)\leq B_\mathrm{cap} \nonumber \\
B(0) = B_0, \:B_\mathrm{loss}(t)=\eta B(t)\nonumber\\
B(t+1) = B(t) + B_\mathrm{loss}(t) + b_\mathrm{in}\sum_{i\in\mathrm{In}}x_{i,t} - b_\mathrm{out}\sum_{i\in\mathrm{Out}}x_{i,t}\nonumber
$$

    $B_\mathrm{cap}$は蓄電池容量、$B_0$は初期蓄電量、$B_\mathrm{loss}$は蓄電池の自然放電量、$\eta$は放電率、$b_\mathrm{in},\,b_\mathrm{out}$はそれぞれ充電・放電における変換効率、$\textrm{In}$、$\textrm{Out}$は$H_\mathrm{inout}$で定義した集合と同義である。<br><br>$H_\mathrm{bat}$は上式の蓄電池容量の不等式制約を表す。変数$y_{i,t}$は0または1の値をとる二値変数である。<br><br>
$$
 H_\mathrm{bat}=\gamma_\textrm{b}\sum_{t=1}^{T}\left[B_\mathrm{cap}-B(t)-\sum_{n=0}^{\lfloor\log_2 (B_\mathrm{cap}-1)\rfloor}2^ny_{i,t}\right]^2
$$

### 最小化するハミルトニアン

制約項の重みをそれぞれ $\gamma_\mathrm{c}, \gamma_\mathrm{a},\gamma_\mathrm{io},\gamma_\mathrm{d},\gamma_\mathrm{s},\gamma_\mathrm{b}$とすると、ハミルトニアンは次のように表されます。<br>

$$
H = \gamma_\mathrm{c}H_\mathrm{expc} + \gamma_\mathrm{c}H_\mathrm{envc} + \gamma_\mathrm{a}H_\mathrm{alloc} + \gamma_\mathrm{io}H_\mathrm{inout} + \gamma_\mathrm{d}H_\mathrm{demand} + \gamma_\mathrm{s}H_\mathrm{sun} + \gamma_\mathrm{b}H_\mathrm{bat}
$$<br>
アニーリングマシンでこのハミルトニアンの最小化を行うことで、制約を満たし、かつコストの低いスケジュールを導くことができます。
'''

type_and_text = [
    {
        'type': 'text',
        'body': r'''
# エネルギー利用最適化

## 概要

いま脱炭素社会に向けた取り組みがさまざまなところで行われています。住宅分野では、安くエコにエネルギーを使うために太陽光発電や蓄電池を設置する住宅が増えてきています。

そのような住宅では、太陽光発電・蓄電池の設置時にHEMS(Home Energy Management System)を導入することも多いです。HEMSは住宅のエネルギーを管理するためのシステムで、電力の使用を可視化したり、住宅内の電気機器を無線で接続して制御することができます。
''',
    },
    {
        'type': 'image',
        'body': 'imgs/hems.png',
        'caption': '出典 iエネ コンソーシアム「HEMSとは？」',
        'width': None,
    },
    {
        'type': 'text',
        'body': r'''
ここではHEMSによって制御を行うことを仮定して、発電・蓄電・電力購入を最適に行うスケジュールをアニーリングマシンで作成し、住宅のエネルギー利用を最適化することを考えます。  

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
        'body': 'imgs/model.png',
        'caption': None,
        'width': None,
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
        'body': 'imgs/output.png',
        'caption': None,
        'width': None,
    },
    {
        'type': 'text',
        'body': r'''
スケジュールを作成するには、需要・天気予報・電気代などのデータが必要となります。

入力データを受け取る→アニーリングマシンで最適化を行う→結果を出力する

という流れに沿ってスケジューリングを行います。
''',
    },
    {
        'type': 'image',
        'body': 'imgs/入力と出力.png',
        'caption': None,
        'width': None,
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
        'body': 'imgs/項目とは.png',
        'caption': None,
        'width': None,
    },
    {
        'type': 'text',
        'body': r'''
この「項目」を各時間枠に適切な数、割り当てていくことでスケジュールを作成していきます。
''',
    },
    {
        'type': 'image',
        'body': 'imgs/項目割り当て.png',
        'caption': None,
        'width': None,
    },
    {
        'type': 'text',
        'body': r'''
二値変数$x_{i,t}$は、項目$i$を時間枠$t$に割り当てる場合に$1$、割り当てない場合に$0$となるように定義します。
''',
    },
    {
        'type': 'markdown',
        'body': r'''
$$
x_{i,t} =
    \begin{cases}
        1 \quad \mbox{項目$i$を時間枠$t$に割り当てるとき}\\
        0 \quad \mbox{割り当てないとき}\\
    \end{cases}
$$
''',
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
項目は次のように用意しておきます。

- 太陽光使用 $i\:(\:i=1,...,n_{1}\:)$
- 太陽光充電 $i\:(\:i=1,...,n_{2}\:)$
- 太陽光売電 $i\:(\:i=1,...,n_{3}\:)$
- 蓄電池使用 $i\:(\:i=1,...,n_{4}\:)$
- 商用電源使用 $i\:(\:i=1,...,n_{5}\:)$
- 商用電源充電 $i\:(\:i=1,...,n_{6}\:)$
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
            st.markdown(t['body'])
