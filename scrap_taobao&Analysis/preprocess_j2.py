import pandas as pd
import logging
logging.Logger(__name__)

info = pd.read_csv('phone_info_j_raw2.csv')

for i in range(info.shape[0]):
    info.loc[i, 'title'] = "".join(info.loc[i, 'title'].split())

# 将每个详情页的总销量平均到每个型号上，获得每个手机的总销量并排序
temp = info[['shop', 'title', 'sales']].groupby(['shop', 'title']).mean()

phone_sales = temp.groupby('title').sum()
phone_sales.sort_values(by=['sales'], ascending=False, inplace=True)
phone_sales.to_csv('phone_sales_j.csv')

temp['count'] = info[['shop', 'title', 'sales']].groupby(['shop', 'title']).count()

temp['sales'] = round(temp['sales'] / temp['count'], 0)

for i in range(info.shape[0]):
    info.loc[i, 'sales'] = temp.loc[(info.loc[i, 'shop'], info.loc[i, 'title']), 'sales']


info.to_csv('phone_info_j.csv', index=False)

with pd.option_context('display.max_columns', None, 'display.max_rows', None):
    print(temp)
    print(phone_sales)
