# import dimod
# import neal
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import itertools
import time
from operator import itemgetter
plt.rcParams['font.family']='Hiragino Sans GB'


### qubo作成関数　(コスト・制約項・不等式制約で分ける) ###

#行列AをDAに渡すときのQuboの形に変える関数
def AtoQubo(A):
    qubo = []
    for k1 in range(total*step):
        for k2 in range(total*step):
            if A[k1,k2] != 0:
                qubo.append({"c": A[k1,k2],"p": [k1,k2]})                
    return qubo

#コスト項
def cost_term(step,total,komoku,cost_ratio,
              conv_eff,C_ele,C_sun,C_env):
    
    A = np.zeros((total*step,total*step))
    
    C_max = max(max(C_ele,C_sun))
    C_min = min(min(C_ele,C_sun))
    bunbo = C_max - C_min
    
    #第１項：H_expence_cost(経費コスト)
    for t in range(step):
        for i in range(total):
            k1 = step * i + t
            #項目iが電源使用または充電
            if komoku[i][1]=='ele':
                #経費コスト
                A[k1,k1] += (C_ele[t]-C_min)/(C_max-C_min)*cost_ratio
                #環境コスト
                A[k1,k1] += C_env*(1 - cost_ratio)
            #項目iが光売電
            elif komoku[i][2]=='sell':
                A[k1,k1] -= (C_sun[t]-C_min)/(C_max-C_min)*cost_ratio*conv_eff
    return AtoQubo(A)

#制約項
def penalty_term(step,total,komoku,cost_ratio,conv_eff,
                D,Sun,w_a,w_io,w_d,w_s):
    A = np.zeros((total*step,total*step))
       
    #第３項：H_alloc(項目iが割り当てられるのは1枠)
    for i in range(total):
        for t in range(step):
            for t_ in range(step):
                k1 = step * i + t            
                k2 = step * i + t_
                if k1 != k2: 
                    A[k1, k2] += w_a 
    
    
    #第４項：H_inout(蓄電池の入出力を同時に行わない)
    for t in range(step):
        for i in range(total):                      
            for j in range(total):
                k1 = step * i + t 
                k2 = step * j + t                
                if (komoku[i][2]=='in')and(komoku[j][2]=='out'):
                    A[k1,k2] += w_io 
               
    #第５項：H_demand(電力需要のバランス)
    for t in range(step):
        for i in range(total):            
            for j in range(total): 
                k1 = step * i + t 
                k2 = step * j + t
                #項目i,jがuse/outのとき
                if ((komoku[i][2]=='use')or(komoku[i][2]=='out'))\
                and((komoku[j][2]=='use')or(komoku[j][2]=='out')):
                    if i != j:
                        if (komoku[i][1]=='sun')and(komoku[j][1]=='sun'):
                                A[k1,k2] += w_d*conv_eff**2
                        elif ((komoku[i][1]=='sun')and(komoku[j][1]!='sun'))\
                        or ((komoku[i][1]!='sun')and(komoku[j][1]=='sun')):                            
                                A[k1,k2] += w_d*conv_eff
                        else:
                                A[k1,k2] += w_d
                    else:
                        if komoku[i][1]=='sun':
                            A[k1,k1] += (1-2*D[t])*w_d*conv_eff**2
                        else:
                            A[k1,k1] += (1-2*D[t])*w_d

    #第６項：H_sun(太陽光のバランス)
    for t in range(step):
        for i in range(total):           
            for j in range(total): 
                k1 = step * i + t 
                k2 = step * j + t
                #項目i,jがsunのとき
                if (komoku[i][1]=='sun')and(komoku[j][1]=='sun'):
                    if i != j: 
                        A[k1,k2] += w_s
                    else: 
                        A[k1,k1] += (1-2*Sun[t])*w_s
    qubo = AtoQubo(A)
    #D(t)^2とS(t)^2の分
    D_Sun = 0
    for t in range(step):
        D_Sun += w_d*D[t]**2 + w_s*Sun[t]**2        
    qubo.append({"c":D_Sun,"p": []})  
    
    return qubo

#不等式制約項
# B(t)<=B_maxとなるquboと0<=B(t)となるquboを返す
def inequality(B_t,B_0):    
    A = np.zeros((total*step,total*step)) 
    def func(const,A,t=1):         
        #終了条件
        if t==B_t+1:
            return const, A  
        #定数部分
        const *= (1-eta)
        #変数部分
        A *= (1-eta)
        #シグマの部分
        for i in range(total):
            k1 = step * i + (t-1)
            if komoku[i][2]=='in':
                A[k1, k1] += b_in
            elif komoku[i][2]=='out':
                A[k1, k1] -= b_out    
        return func(const,A,t+1)
    const, A = func(B_0,A)
    #B(t)<=B_max
    qubo = AtoQubo(A)
    qubo.append({"c":const-B_max,"p": []})  
    #0<=B(t)
    qubo2 = AtoQubo(-A)
    qubo2.append({"c":-const,"p": []})
    return {'terms':qubo}, {'terms':qubo2}


### 制約破り判断関数 ###

#制約alloc(項目iが割り当てられるのは1枠まで)を判断
def check_alloc(dict,opt_result={}):
    satisfied = True
    for key, val in dict.items():
        if val:
            i = int(key) // step
            #項目iが既に割り当てられているなら、制約破り
            if i < total:
                if i in opt_result:                                
                    satisfied = False
                #まだ割り当てられていないならopt_result{ID:t}に追加
                else:
                    t = int(key) % step
                    opt_result[i] = t
    #opt_resultが空なら
    if not opt_result:
        print('opt_resultが空')
        satisfied = False
    return satisfied, opt_result
    
#制約inout(蓄電池の入出力は同時にしない)を判断
def check_inout(opt_result):
    satisfied = True      
    for i in range(total):
        for j in range(total):
            #項目i,jが割り当てられていて
            if i in opt_result:              
                if j in opt_result:
                    #項目iがinかつ項目jがoutで                
                    if (komoku[i][2]=='in')and(komoku[j][2]=='out'):
                        #項目iと項目jの割り当てられた時間tが同じなら
                        if opt_result[i] == opt_result[j]:                            
                            satisfied = False #制約破り
    return satisfied

#制約demand(需要のバランス)をチェック
def demandBalancePerStep(opt_result,conv_eff):
    satisfied = True
    for t in range(step):
        supply = 0 #tにおけるuse/outの項目の合計
        for i in range(total):
            #項目iが割り当てられていて
            if i in opt_result: 
                #項目iがuse/outの項目で 
                if komoku[i][2]=='use' or komoku[i][2]=='out':
                    #項目iが割り当てられた時間がtなら
                    if opt_result[i] == t:
                        if komoku[i][1]=='sun':
                            supply += conv_eff #変換効率
                        else :
                            supply += 1
        #供給-需要
        balance = supply - D[t]
        if balance < 0 or balance >1:
            #print('step=',t,'需要供給バランス',balance)
            satisfied = False
    return satisfied

#制約sun(太陽光のバランス)をチェック、上とほぼ同じ
def sunBalancePerStep(opt_result):
    satisfied = True
    for t in range(step):
        sun_sum = 0 #出力の合計
        for i in range(total):
            if i in opt_result:
                if komoku[i][1] == 'sun':
                    if opt_result[i] == t:
                        sun_sum += 1
        #出力-入力
        balance = sun_sum - Sun[t]
        if balance != 0:
            #print('step=',t,'太陽光バランス',balance)
            satisfied = False
    return satisfied

#各時間において蓄電量が蓄電池容量を超えていないかを確認する
#結果が出た後に満たされているか確認する。制約ではない
def batteryCapacity(opt_result):
    satisfied = True
    B = B_0
    for t in range(step):
        for i in range(total):
            if i in opt_result:
                if opt_result[i] == t:                    
                    if komoku[i][2] == 'in':
                        B += 1
                    elif komoku[i][2] == 'out':
                        B -= 1
        if B < 0 or B > B_max:#蓄電量が負または容量を超えていたらだめ
            satisfied = False
    return satisfied, B

#制約破り判断
def constraintPrint(sample):
    satisfied, opt_result = check_alloc(sample,{})
    if satisfied: 
        print('alloc  :項目を一つに割り当てる制約 満たす') 
    else:            
        print('alloc  :項目を一つに割り当てる制約 破る')    
        satisfied = False
    if check_inout(opt_result):
        print('inout  :蓄電池の入出力を同時にしない制約 満たす')   
    else:
        print('inout  :蓄電池の入出力を同時にしない制約　破る')
        satisfied = False    
    if demandBalancePerStep(opt_result,conv_eff):
        print('demand :需要と供給のバランス 満たす') 
    else:
        print('demand :電力需要と供給のバランス 破る')
        satisfied = False
    if sunBalancePerStep(opt_result):
        print('sun    :太陽光のバランス　満たす')
    else :
        print('sun    :太陽光のバランス　破る')
        satisfied = False    
    battery, capacity = batteryCapacity(opt_result)
    if battery:
        print('battery:時間ごとの蓄電池容量　満たす')        
    else :
        print('battery:時間ごとの蓄電池容量　破る')
        satisfied = False
    print('蓄電量は',capacity*unit,'W\n')
    return satisfied, opt_result

#制約を全て満たしたかどうかのtrue/falseだけ返す関数
def constraint(sample):
    satisfied, opt_result = check_alloc(sample,{})
    if satisfied:
        if check_inout(opt_result): 
            if demandBalancePerStep(opt_result,conv_eff):
                if sunBalancePerStep(opt_result):
                    satisfied = True
                    if batteryCapacity(opt_result)[0]:
                        satisfied = True                                       
                    else :
                        satisfied = False
                else :
                    satisfied = False
            else:
                satisfied = False
        else:
            satisfied = False            
    else:
        satisfied = False
    return satisfied, opt_result


### 入力(太陽光・需要・電気代)を用意する際使う関数 ###

#四捨五入する関数
def my_round(val, digit=0):
    p = 10 ** digit
    return (val * p * 2 + 1) // 2 / p

#リストを四捨五入してカードにする
def rounding(lst):
    #unitで割って
    lst1 = list(normalize(lst,1/unit))
    #小数点を四捨五入
    lst2 = [int(my_round(lst1[i],0)) for i in range(len(lst1))]
    lst3 = normalize(lst2,unit)
    return lst3, lst2

#リストを途中から一周する関数
def rotate(start,end,lst):
    l = len(lst)
    nlst = [0]*l
    for i in range(l):
        if start+i<l:    
            nlst[i]  = lst[start+i]
        else:
            nlst[i] = lst[start+i-l]        
    nlst = nlst[:end+1-start]
    return nlst

#開始時刻から終了時刻まで用意する
def rotateAll(start,end):#,D=D,Sun=Sun,C_ele=C_ele,C_sun=C_sun):
    D = rotate(start,end,D_0)
    Sun = rotate(start,end,Sun_0)
    C_ele = rotate(start,end,C_ele_0)
    C_sun = rotate(start,end,C_sun_0)
    return D,Sun,C_ele,C_sun

#発電量を曇りは1/3倍、雨雪は1/5倍でリストを返す
def Weather(weather,lst):
    l = [0]*len(lst)
    if weather != 's':#曇りor雨or雪
        for i in range(len(lst)):            
            if weather == 'c':
                l[i] = int(my_round(lst[i]/3))
            else:
                l[i] = int(my_round(lst[i]/5))
    else:
        l = lst
    return l

#三時間毎の天気予報を入れると太陽光の発電量を計算してくれて返す
def Weather3hours(tenki,sun):
    lst = [Weather(tenki[i],sun[i*3:(i+1)*3]) for i in range(len(tenki))]
    return list(itertools.chain.from_iterable(lst))

#辞書をリストに
def dictToLst(dict):
    list = []
    for t in dict:
        list.append(dict[t])
    return list

#コストの辞書返す
def eleCost():
    dic = {}
    for t in range(24):
        if t < 7:
            dic[t]=12
        else:
            if t < 10:
                dic[t]=26
            else:
                if t < 17:
                    dic[t]=39
                else:
                    dic[t]=26
    return dictToLst(dic)

#用意する需要パターン
#少し使いすぎな２人世帯（日中在宅０人）
D1 = [550,450,360,350,350,400,420,710,710,620,590,450,450,410,410,410,410,440,500,670,690,670,670,650]
#省エネ上手な３人家族(日中在宅２人)
D2 = [230,150,130,120,110,110,130,190,340,360,340,340,260,260,270,220,240,410,430,410,430,330,310,270]
#２人世帯平均(日中在宅２人)
D3 = [207,177,147,157,157,167,228,330,381,391,351,311,341,341,311,310,320,331,372,542,549,509,438,318]
#３人世帯(日中在宅２人)
D4 = [242, 207, 172, 184, 184, 195, 267, 536, 596, 607, 561, 364, 199, 199, 164, 163, 174, 187, 435, 634, 642, 596, 512, 372]
#５人世帯(日中在宅３人）
D5 = [290, 248, 206, 220, 220, 234, 319, 462, 533, 547, 491, 435, 527, 527, 485, 484, 498, 513, 521, 759, 769, 713, 613, 445]

#24時間分の入力データを作る
def make_input(demand,tenki,start):
    #1kWの太陽光パネル・快晴・9月
    Sun = [0,0,0,0,0,0,0,100,300,500,600,700,700,700,600,500,400,200,0,0,0,0,0,0]    
    #通常の家の発電量
    Sun = normalize(Sun,2)
    #天気で発電量を調整する
    Sun = Weather3hours(tenki,Sun)
    #丸めてunitでわる
    dem, demand = rounding(demand)
    sun, Sun = rounding(Sun)    
    D = demand
    #グラフを描く
    lineGraphSun(sun,start)
    lineGraphDemand1(dem,start)    
    C_ele = eleCost()
    C_sun = [8]*24
    normalizeRate=0.01
    C_ele = normalize(C_ele,normalizeRate*unit/1000)
    C_sun = normalize(C_sun,normalizeRate*unit/1000)
    return D,Sun,C_ele,C_sun


### 入力(太陽光・需要)をグラフにする関数
#太陽光のグラフを描く
def lineGraphSun(y,start=0):
    x = [t for t in range(len(y))]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)    
    ax.set_xticks(x)
    ax.set_xlim(0,23)
    ax.set_xlabel('時間(時)')
    ax.set_ylabel('太陽光発電量(W)')
    ax.set_ylim(0,700/unit*unit*2+unit/2)#Sun晴れの場合の最大値
    ax.plot(x,y)
    if start+step < 24:
        ax.axvspan(start,(start+step)%24,color="lightcoral",alpha=0.2)
    else :
        ax.axvspan(start,23,color="pink",alpha=0.2)
        ax.axvspan(0,(start+step)%24,color="lightcoral",alpha=0.2)
    ax.grid(axis='both')
    ax.set_title('太陽光発電量')
    plt.show()
    fig.savefig('時系列太陽光.png',bbox_inches='tight')
    
#需要のグラフを描く(3パターン全て）
def lineGraphDemand(y1,y2,y3,start=0):
    x = [t  for t in range(24)]
    l1,l2,l3 = 'パターン1','パターン2','パターン3'
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)    
    ax.plot(x,y1,color='b',label=l1)
    ax.plot(x,y2,color='g',label=l2)
    ax.plot(x,y3,color='y',label=l3)
    ax.set_xticks(x)
    ax.set_xlim(0,23)
    ax.set_xlabel('時間(時)')
    ax.set_ylabel('需要(W)')  
    ax.grid(axis='both')
    ax.legend(loc=0)
    ax.set_title('需要')
    plt.show()
    fig.savefig('時系列需要.png',bbox_inches='tight')
    
#需要のグラフを描く(1パターンのみ）
def lineGraphDemand1(y1,start=0):
    x = [t  for t in range(24)]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)    
    if start+step < 24:
        ax.axvspan(start,(start+step)%24,color="lightcoral",alpha=0.2)
    else :
        ax.axvspan(start,23,color="lightcoral",alpha=0.2)
        ax.axvspan(0,(start+step)%24,color="lightcoral",alpha=0.2)
    ax.set_ylim(0,800/unit*unit+unit/2)#Sun晴れの場合の最大値
    ax.plot(x,y1,color='r')
    ax.set_xticks(x)
    ax.set_xlim(0,23)
    ax.set_xlabel('時間(時)')
    ax.set_ylabel('需要(W)')
    ax.grid(axis='both')
    ax.set_title('需要')
    # plt.show()
    # fig.savefig('時系列需要.png',bbox_inches='tight')



### 出力結果を図示する関数 ###

#スケジュールをまとめる
def Schedule(opt_result):
    schedule = [0]*step
    B = B_0
    for t in range(step):
        #tごとの各項目数を計上するための辞書
        do = {'sun_use':0,'sun_in':0,'sun_sell':0,\
            'bat_out':0,'ele_use':0,'ele_in':0,\
             'bat':B}
        for i in range(total):
            #項目iが割り当てられていて
            if i in opt_result:
                #項目iの割り当てられたstepがtなら
                if opt_result[i] == t:
                    setsubi = komoku[i][1] #項目iの設備
                    kyodo = komoku[i][2] #項目iの挙動
                    if setsubi == 'sun':
                        if kyodo == 'use':#光使用
                            do['sun_use']+=1
                        elif kyodo == 'in':#光充電                          
                            do['sun_in']+=1
                            do['bat'] += 1
                        else:              #光売電
                            do['sun_sell']+=1
                    elif setsubi == 'bat':#蓄電池使用
                        do['bat_out']+=1
                        do['bat'] -= 1
                    else:
                        if kyodo == 'use':#商用電源使用
                            do['ele_use']+=1
                        else:             #商用電源充電　
                            do['ele_in']+=1
                            do['bat'] += 1
        schedule[t] = list(do.values())
        B = do['bat']
    #表作成の時のために転置しておく
    schedule = [list(x) for x in zip(*schedule)]
    return schedule

#データの正規化
def normalize(data,normalizeRate):
    def f(x):
        return x*normalizeRate    
    return list(map(f,data))

#項目の電力単位にする
def unitDouble(schedule):
    def normalize(schedule,normalizeRate):
        def f(x):
            return x*normalizeRate    
        return list(map(f,schedule))
    for i in range(len(schedule)):
        schedule_ = [normalize(schedule[i],unit) for i in range(len(schedule))]
    return schedule_

#表を作る
def makeTable_(start,data,labels,mode):
    if mode==0:
        loc = 'lower center'
        data_name = 'input'
    else:
        loc = 'upper center'
        data_name = 'output'
    step_labels = [str((i+start)%24)+':00' for i in list(range(step))]  
    fig = plt.figure(dpi=200)    
    ax1 = fig.add_subplot(2,1,1)
    df0 = pd.DataFrame(data,index=labels,columns=step_labels)
    ax1.axis('off')
    ax1.table(cellText=df0.values,colLabels=df0.columns,\
             rowLabels=df0.index,loc=loc,fontsize=15)
    plt.show()
    fig.savefig(data_name+'.png',bbox_inches='tight')
    
def make2Table(schedule,start):
    demand = list(map(int,normalize(D[:step],unit)))
    sun = list(map(int,normalize(Sun[:step],unit)))
    cost = list(map(int,normalize(C_ele[:step],1000/normalizeRate/unit)))
    label = ["需要(w)","太陽光発電量(w)","商用電源料金(円)"]
    makeTable_(start,[demand,sun,cost],label,0)
    label = ["太陽光使用(w)","太陽光充電(w)","太陽光売電(w)",\
             "蓄電池使用(w)","商用電源使用(w)","商用電源充電(w)",\
            "蓄電池残量(w)"]
    makeTable_(start,unitDouble(schedule),label,1)  

#最適解でかかったコストを計上してプリント出力する
def costPrint(opt_result,normalizeRate):
    cost = 0 #コストの合計
    for i in range(total):
        #項目iが割り当てられていて
        if i in opt_result:
            #項目iが電源使用なら
            if komoku[i][1]=='ele' and komoku[i][2]=='use':
                #項目iが割り当てられた時間tの商用電源コストC_e[t]を加算
                cost += C_ele[opt_result[i]]/normalizeRate
            #項目iが光売電なら
            elif komoku[i][2]=='sell':
                cost -= C_sun[opt_result[i]]/normalizeRate
    #コスト正なら
    if cost >= 0:
        print("かかったコストは",cost,"円")
    #負なら
    else:
        print(-cost,"円の売上")

#棒グラフ
def plotBar(start,schedule,Data,mode):
    step_labels = [str((i+start)%24) for i in list(range(step))]    
    if mode==1:
        data_name="需要"
        barvalue_ = list(itemgetter(0,3,4)(schedule))
        pop_lst=[1,2,5]
        title="需要と供給"
    else:
        data_name="太陽光発電量"        
        barvalue_ = list(itemgetter(0,1,2)(schedule))
        pop_lst=[3,4,5] 
        title="太陽光の収支"
    how_labels = [data_name,"太陽光使用","太陽光充電","太陽光売電",\
                     "蓄電池使用","商用電源使用","商用電源充電"]
    for i in sorted(pop_lst, reverse=True):
            how_labels.pop(i+1)
    barvalue = unitDouble(barvalue_)      
    data=list(map(int,normalize(Data,unit)))
    df0 = pd.DataFrame(barvalue,index=how_labels[1:])
    fig, ax = plt.subplots(figsize=(6, 4.8),dpi=150)
    ax.bar(step_labels, data, width=-0.3, align='edge')
    for i in range(len(df0)):
        ax.bar(step_labels, df0.iloc[i], width=0.3, \
               align='edge', bottom=df0.iloc[:i].sum())
#棒グラフに数値を入れる    
#         for j in range(len(step_labels)):
#             if df0.iloc[i,j]!=0:
#                 ax.text(x=j+0.3/2,y=df0.iloc[:i,j].sum() + (df0.iloc[i, j]/2),
#                          s=df0.iloc[i, j], ha='center',va='bottom',fontsize=3)
#             ax.text(x=j-0.3/2, y=data[j]/2, s=data[j],ha='center',
#                     va='bottom',fontsize=3)
    ax.set(xlabel='時間(時)',ylabel='電力量(w)')
    ax.set_ylim([0,max(data)+10])
    ax.legend(how_labels)
    ax.set_title(title)
    plt.show()    
    fig.savefig(data_name+'.png',bbox_inches='tight')

def plotBar_bat(start,schedule,mode):
    step_labels = [str((i+start)%24) for i in list(range(step+1))] 
    #充電のグラフ
    if mode==0:       
        data_name="充電&料金"           
        barvalue_ = list(itemgetter(1,5)(schedule))
        title="商用電源料金の推移と充電"
        how_labels = [data_name,"太陽光充電","商用電源充電","商用電源料金"]
    #使用のグラフ
    else:
        data_name="使用&料金"           
        barvalue_ = list(itemgetter(0,3,4)(schedule))
        barvalue_[1],barvalue_[2]=barvalue_[2],barvalue_[1]
        title="商用電源料金の推移と電力使用"
        how_labels = [data_name,"太陽光使用","商用電源使用","蓄電池使用","商用電源料金"]
    barvalue = unitDouble(barvalue_) 
    #時間ごとの充電・使用量の最大値を求めておきy軸の上限を定めておく
    ymax = max([sum([[barvalue[i][j] for i in range(len(barvalue))] for j in range(step)][k]) for k in range(step)])
    c_ele=normalize(C_ele,1/normalizeRate)
    df0 = pd.DataFrame(barvalue,index=how_labels[1:len(how_labels)-1])
    #ax1:使用・充電の棒グラフ
    fig, ax1 = plt.subplots(figsize=(6, 4.8),dpi=150)
    for i in range(len(df0)):
        ax1.bar(step_labels[:-1],df0.iloc[i],width=0.3,align='edge',
                bottom=df0.iloc[:i].sum(),label=how_labels[1+i])
    ax1.set(xlabel='時間(時)',ylabel='電力量(w)')
    ax1.set_title(title)  
    ax1.set_ylim(0, ymax+10)
    hans1, labs1 = ax1.get_legend_handles_labels()    
    #ax2:商用電源の折れ線グラフ
    ax2 = ax1.twinx()
    ax2.plot(step_labels[:-1],c_ele,color='red',alpha=1,label=how_labels[len(how_labels)-1])
    ax2.set(ylabel='料金(円)')    
    y_min, y_max = ax2.get_ylim()
    ax2.set_ylim(y_min, y_max)
    #凡例
    hans2, labs2 = ax2.get_legend_handles_labels()
    ax1.legend(hans1+hans2,labs1+labs2,loc="upper left",bbox_to_anchor=(1.1,1.0))
    ax1.set_xticks(step_labels)
    ax1.legend(hans1+hans2,labs1+labs2,loc="upper left",bbox_to_anchor=(1.1,1.0))
    ax1.set_xticks(step_labels)
    plt.show()    
    fig.savefig(data_name+'.png',bbox_inches='tight')
    
#グラフ4つ表示
def makeBar(schedule,start,D,Sun):
    #太陽光の収支
    plotBar(start,schedule,Sun,0)
    #需要と供給
    plotBar(start,schedule,D,1)
    #商用電源料金と充電量
    plotBar_bat(start,schedule,0)
    #商用電源料金と使用量
    plotBar_bat(start,schedule,1)
#出力
def output(opt_result,start):
    #値段の表示
    costPrint(opt_result,normalizeRate)  
    #結果を項目ごとでまとめる
    schedule = Schedule(opt_result)
    #表表示
    # make2Table(schedule,start)
    #棒グラフ表示
    # makeBar(schedule,start,D,Sun)


### 使わない値をFalseに設定する関数 ###

#蓄電池の項目を用意する（最初は初期蓄電量分だけ使えるようにする）
def B_komoku(B_max,B_0):
    B_lst = [0]*step
    B_lst[0] = B_0
    for t in range(1,step):
        B_lst[t] = sum(D[:step])
    return B_lst

#使わない変数のindexが入ったリストを返す
def disuse(kmk_lst,disuse_lst=[]):
    for k in range(len(kmk_lst)):
        #蓄電池使うx
        if k == 0:
            lst = B_komoku(B_max,B_0)            
        else:
            break
        for t in range(step):
            disuse_len = kmk_lst[k] - lst[t] 
            for i in range(disuse_len):
                disuse_lst.append(str(step*(lst[t]+sum(kmk_lst[:k])+i)+t))                
    return disuse_lst

#使わないビットfixed_configの型で1返す
def false_dic(disuse_lst):
    conf_lst={}
    for i in range(len(disuse_lst)):
        conf_lst[disuse_lst[i]]=False
    return conf_lst


### 項目を用意する関数 ###

#項目の各種類で必要な数が入ったリストを作る
def make_k_lst():
    lst = [0]*6
    #太陽光(sun_sell,sun_use,sun_in)の数
    for i in range(1,4):
        lst[i] = sum(Sun[:step])
    #蓄電池使う(bat_out)の数
    lst[0] = sum(D[:step])
    #商用電源使う(ele_use)の数
    lst[4] = sum(D[:step])
    #商用電源貯める(ele_in)の数
    lst[5] = B_max//2
    return lst

#項目を用意する関数
def newKomokuProduce(lst):
    index = 0
    total = sum(lst)
    komoku = [0]*total
    for k in range(len(lst)):
        for j in range(lst[k]):
            if k == 0:
                komoku[index]=[index,'bat','out']
            elif k==1:
                komoku[index]=[index,'sun','sell']
            elif k==2:
                komoku[index]=[index,'sun','use']
            elif k==3:
                komoku[index]=[index,'sun','in']
            elif k==4:
                komoku[index]=[index,'ele','use']
            else:
                komoku[index]=[index,'ele','in']            
            index += 1    
    return komoku, total
