import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

tb = pd.read_csv('phone_info_t.csv')
jd = pd.read_csv('phone_info_j.csv')

jd['type'] = jd['phone_type']
jd.drop(columns=['phone_type'], inplace=True)

sum_info = tb.append(jd, ignore_index=True)

# 根据被售卖量进行排序。（可根据title匹配，每一种型号的手机名称已经统一）
temp = sum_info.groupby(['shop', 'title']).count()
temp = temp.droplevel(0)
temp['count'] = 1
shop_num = temp.groupby('title').sum()
shop_num.sort_values(by=['count', 'type'], ascending=False, inplace=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(shop_num)

# 选择前num个，修改num值即可生成num个箱型图
num = 5

x = shop_num.loc[shop_num.index.to_list()[0], 'price']
box = pd.DataFrame(np.full((x, num), np.nan), columns=shop_num.index.to_list()[:num])
count = pd.DataFrame(np.zeros((1, num)), columns=shop_num.index.to_list()[:num])
for title in shop_num.index.values[:num]:
    for j in range(sum_info.shape[0]):
        if sum_info.loc[j, 'title'] == title:
            box.loc[count.loc[0, title], title] = sum_info.loc[j, 'price']
            count.loc[0, title] += 1
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(box)

matplotlib.rcParams['figure.dpi'] = 180

matplotlib.rcParams['font.sans-serif'] = ['SimHei']

axes = box.boxplot(column=box.columns.to_list(), return_type='axes')
plt.xticks(rotation=30)
plt.show()
