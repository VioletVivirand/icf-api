import pandas as pd
import numpy as np
from flask_restful import abort

data_dtypes = {'age': np.int8, 'description': object, 's7_class_codet': object, 's7_level_code': object, 'sex': object, 'TOWN': object}
data = pd.read_csv('./dataset.csv', dtype=data_dtypes)

pops_dtypes = {'CITYNAME': object, 'TOWNNAME': object, 'TOTAL': np.int32 ,'MALE': np.int32, 'FEMALE': np.int32, 'TOWN': object}
pops = pd.read_csv('./town_pops.csv', dtype=pops_dtypes)

# Test with: 
# testargs = {'sex': '1', 'smallerAge': 18, 'biggerAge': 30, 'level': '1,2', 'codet': '1,2,3,4,5,6,7,8,9', 'desc': ''}
# createjson(testargs)
def createjson(args):
    cons = []

    if (args['sex']):
        cons.append('con_sex')
        ans_sex = args['sex'].split(',')
        con_sex = data['sex'].isin(ans_sex)

    if (args['smallerAge'] and args['biggerAge']):
        cons.append('con_age')
        ans_smallerAge = int(args['smallerAge'])
        ans_biggerAge = int(args['biggerAge'])
        con_age = (data['age'] >= ans_smallerAge) & (data['age'] <= ans_biggerAge)

    if (args['level']):
        cons.append('con_level')
        ans_level = args['level'].split(',')
        con_level = data['s7_level_code'].isin(ans_level)

    if (args['codet']):
        cons.append('con_codet')
        ans_codet = args['codet'].split(',')
        con_codet = data['s7_class_codet'].isin(ans_codet)

    if (args['desc']):
        cons.append('con_desc')
        ans_desc = args['desc'].split(',')
        con_desc = data['description'].isin(ans_desc)

    if(cons):
        try:
            disabilities = data[eval(' & '.join(cons))].groupby('TOWN').size()
        except Exception as e:
            return abort(404)
    else:
        disabilities = data.groupby('TOWN').size()
    
    # 運算完以後的資料是 Series，為了等一下可以跟鄉鎮市區人口數資料合併，先轉換為 DataFrame
    disabilities = disabilities.reset_index()
    disabilities.columns=['TOWN', 'DISABILITIES']

    # 將 disabilities（依據條件計算出的身心障礙人口數資料）跟 pops（鄉鎮市區人口資料）做 left outer join
    merge = pd.merge(disabilities, pops, how='left', on='TOWN')
    # 新增一個欄位 prevalence，計算盛行率到千分位，再四捨五入到小數點以下第三位
    merge['prevalence'] = (merge['DISABILITIES']/merge['TOTAL']*1000).round(3)

    # 最後只取盛行率跟鄉鎮市區代碼，轉換為 Series，其中資料為盛行率資料，索引欄位則為鄉鎮市區代碼
    output = merge['prevalence']
    output.index = merge['TOWN']

    return output.to_json(orient='index')

