### 変数の値設定 ###

#変換効率
conv_eff=1
#正規化何倍
normalizeRate=0.01
#環境コスト
C_env=0.5
#重み
w_d=1.0 #需要と供給のバランス
w_a=1.0 #項目は一つ割り当てる
w_io=1.0 #蓄電池の入出力は同時にしない
w_s=1.0 #太陽光の収支を合わせる
#蓄電池関連
b_in = 0.95 #変換効率
b_out = 0.95 #変換効率
eta = 0.05 #放電率


### 問題を解く ###

apikey = 'd639b177fad92845b7f642eb1ac573eebdecccfa5fe3c0a4cd4a8f73aa8524b5'
url = 'https://api.aispf.global.fujitsu.com/dai/v1/type0101/async/solve'
url_get = 'https://api.aispf.global.fujitsu.com/dai/v1/type0101/async/jobs/result/'

headers = {'X-Api-Key': apikey,
    'Accept': 'application/json',
    'Content-type': 'application/json'}

payload = {
    #コスト項
    "binary_polynomial": {
        "terms": []     
    },
    #制約項
    "penalty_binary_polynomial": {
        "terms": []     
    },
    #不等式制約
      "inequalities": [],
    #DAパラメータ
    "fujitsuDA3": {
    "time_limit_sec": 30,
#     "penalty_coef": 10000,
    "gs_cutoff":100,#グローバル探索の収束判定レベル
    }
}
#項目あたり電力量(W)
unit=100
#蓄電池
B_0 = int(0/unit) #初期貯蓄
B_max = int(5000/unit) #貯蓄可能容量 家庭用蓄電池しては5kWh~7kWh程度が一般的
#経費コストと環境コストの比率(ここでは1:1)
cost_ratio=0.5
#スケジュールの始まりの時間
startTime = 0
#スケジュール時間
step = 12
print(startTime,'時から',(startTime+step-1)%24,'時まで')
#天気
tenki = ['r' for i in range(8)]
#入力（太陽光・需要・料金）について開始時間から終了時間分だけ用意する
D_0,Sun_0,C_ele_0,C_sun_0 = make_input(D3,tenki,startTime)
D,Sun,C_ele,C_sun = rotateAll(startTime,(startTime+step-1)%24)
#項目を作る
kmk_lst=make_k_lst()
komoku, total = newKomokuProduce(kmk_lst)
print(kmk_lst)
#QUBO作成
Q_cost = cost_term(step,total,komoku,cost_ratio,conv_eff,
                    C_ele,C_sun,C_env)
Q_penalty  = penalty_term(step,total,komoku,cost_ratio,conv_eff,D,Sun,
                    w_a=w_a,w_io=w_io,w_d=w_d,w_s=w_s)
#Falseに変数を固定
config_x = false_dic(disuse(kmk_lst,[]))
print(total*step-len(config_x),'用意したビット数 - 固定したビット数')
payload["fujitsuDA3"]["fixed_config"]= config_x
#payloadに入れる
payload["binary_polynomial"]["terms"] = Q_cost
payload["penalty_binary_polynomial"]["terms"] = Q_penalty
for t in range(1,step+1):
    term1, term2 = inequality(t,B_0)
    payload["inequalities"].extend([term1,term2])   
#job_idの取得
job_id = requests.post(url, data=json.dumps(payload), headers=headers).json()["job_id"]
r = requests.get(url_get+job_id, headers=headers)
#jobの結果の取得
while "qubo_solution" not in r.json():
    r = requests.get(url_get+job_id, headers=headers)
r = requests.get(url_get+job_id, headers=headers)
print('Done!')
#結果もらう
answer = r.json()["qubo_solution"]["solutions"]
for i in range(len(answer)):
    opt_result = {}
    sample = answer[i]['configuration']
    print('energy',answer[i]['energy'])
    print('penalty energy',answer[i]['penalty_energy'])
    satisfied,opt_result = constraintPrint(sample)
    #結果出力
    output(opt_result,startTime)
    #成功したら
    if satisfied:                                            
        print(i+1,'番目の解で成功')
        break
if not satisfied:
    print('失敗')

