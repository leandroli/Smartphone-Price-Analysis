import pandas as pd
import numpy as np
import re
import logging

logging.Logger(__name__)

info = pd.read_csv("phone_info_j2.csv", na_values='None')

r_num, c_num = info.shape
# 对爬到的title进行初步处理
for i in range(r_num):
    try:
        result = re.match('(\\\\n[ ]+).*', info.loc[i, 'title'])
        info.loc[i, 'title'] = info.loc[i, 'title'][len(result.group(1)):]
    except Exception as err:
        logging.debug(str(info.loc[i, 'title']) + str(err))
    else:
        try:
            result2 = re.match('([^ ]+ [^ ]+ [^ ]+ [^ ]+ [^ ]+ [^ ]+).*', info.loc[i, 'title'])
            info.loc[i, 'title'] = result2.group(1)
        except Exception as err:
            logging.debug(str(info.loc[i, 'title']) + str(err))
# 将销量变为数字，例："3万+"变为"30000.0"
r_num, c_num = info.shape
for i in range(r_num):
    try:
        result = re.match('\(([^ ]+)\)', info.loc[i, 'sales'])
        info.loc[i, 'sales'] = result.group(1)
    except Exception as err:
        logging.debug(str(info.loc[i, 'title']) + str(err))
    try:
        info.loc[i, 'sales'] = info.loc[i, 'sales'][:-1]
        if info.loc[i, 'sales'][-1] != np.nan and info.loc[i, 'sales'][-1] == "万":
            info.loc[i, 'sales'] = float(info.loc[i, 'sales'][:-1]) * 10000
        elif info.loc[i, 'sales'][-1] != np.nan:
            info.loc[i, 'sales'] = float(info.loc[i, 'sales'])
    except Exception as err:
        logging.debug(str(info.loc[i, 'title']) + str(err))

info.dropna(axis='index', how='any', inplace=True)
# 用正则表达式处理title，删去不需要的字段
for i in range(info.shape[0]):
    suffixes = [' \(A', ' 5G', ' 游戏', ' 2K\+', ' 李现', ' 骁龙', ' 麒麟', ' 尊享', ' 双卡', ' 幻彩', ' 5G 双模',
                ' 6GB\+', ' 8GB\+', ' 90Hz', ' 前置', ' 索尼', ' 4GB+', ' 超感光']
    for word in suffixes:
        try:
            result = re.match(f'(.+){word}.*', info.loc[i, 'title'])
            info.loc[i, 'title'] = result.group(1)
            print(info.loc[i, 'title'])
        except Exception as err:
            logging.error(err)
# 去除型号的标签并转换形式，例：去掉【白条12期免息】，将（8GB 128GB）转为8GB+128GB
for i in range(info.shape[0]):
    try:
        result = re.match('.*（(.+)）', info.loc[i, 'phone_type'])
        info.loc[i, 'phone_type'] = "+".join(result.group(1).split())
    except Exception as err:
        logging.error(err)
    try:
        result2 = re.match('【.*】(.+)', info.loc[i, 'phone_type'])
        info.loc[i, 'phone_type'] = result2.group(1)
    except Exception as err:
        logging.error(err)


info.to_csv(index=False, path_or_buf='phone_info_j_w.csv')
