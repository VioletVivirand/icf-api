import pandas as pd
import numpy as np
from flask_restful import abort

dt_dict = {'age': np.int8, 'description': object, 's7_class_codet': object, 's7_level_code': object, 'sex': object, 'TOWN': object}
data = pd.read_csv('./dataset.csv', dtype=dt_dict)

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
            df = data[eval(' & '.join(cons))].groupby('TOWN').size()
            return df.to_json(orient='index')
        except Exception as e:
            return abort(404)
    else:
        df = data.groupby('TOWN').size()
        return df.to_json(orient='index')