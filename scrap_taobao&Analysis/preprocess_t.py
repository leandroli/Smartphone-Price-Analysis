import pandas as pd
import logging
import re
logging.Logger(__name__)

info = pd.read_csv('phone_info_t_raw.csv')
for i in range(info.shape[0]):
    # 去除标签：
    columns = ['title', 'type']
    for column in columns:
        try:
            result = re.match('【.*】(.+)', info.loc[i, column])
            info.loc[i, column] = result.group(1)
        except Exception as err:
            logging.error(info.loc[i, column] + str(err))
        try:
            result = re.match('\[.*\](.+)', info.loc[i, column])
            info.loc[i, column] = result.group(1)
        except Exception as err:
            logging.error(info.loc[i, column] + str(err))

    # 去除标题中不需要的后缀：
    suffixes = ['正品老人机', '麒麟', '极点全面屏', ' 4800万', ' 大电量', '新品', '老人机', '军工', '尊享版', ' 3200万',
                '超清全视屏', '全面屏', '移动', '6400万四摄', ' 索尼6400万', '超级', ' 快充', '儿童手机', ' 855高通',
                '高通', '骁龙', ' 全网通', 'AMOLED屏幕', '曲面屏', '老年', '青春版', ' 1亿像素', ' 6400万', '全新正品', ' 新款',
                ' 八核大电量', '超长待机', ' 6.09', ' 新SS', ' 4G', '双', '大电量', '新ss']

    for word in suffixes:
        try:
            result = re.match(f'(.+){word}.+', info.loc[i, 'title'])
            info.loc[i, 'title'] = result.group(1)
        except Exception as err:
            logging.debug(info.loc[i, 'title'] + str(err))

    prefixes = ['全网通4G', 'Huawei/', '华为旗下HONOR/', 'YEPEN/', 'Apple/', '华为HONOR/',
                'Changhong/', '新Nokia/', '华为旗下/', '5年换新/Nokia/']

    # 去除标题中不需要的前缀：
    for word in prefixes:
        try:
            result = re.match(f'{word}(.+)', info.loc[i, 'title'])
            info.loc[i, 'title'] = result.group(1)
        except Exception as err:
            logging.debug(info.loc[i, 'title'] + str(err))

    try:
        result = re.match('(.+)-.+', info.loc[i, 'price'])
        info.loc[i, 'price'] = result.group(1)
    except Exception as err:
        logging.debug(info.loc[i, 'price'] + str(err))

    info.loc[i, 'title'] = "".join(info.loc[i, 'title'].split())

# 将每个详情页的总销量平均到每个型号上，获得每个手机的总销量并排序
temp = info[['sales', 'shop', 'title']].groupby(['shop', 'title']).sum()
temp['count'] = info[['sales', 'shop', 'title']].groupby(['shop', 'title']).count()
temp['sales'] = temp['sales'] / temp['count']

temp.drop(columns=['count'], inplace=True)
phone_sales = temp.groupby('title').sum()
phone_sales.sort_values(by=['sales'], ascending=False, inplace=True)

temp['count'] = info[['sales', 'shop', 'title']].groupby(['shop', 'title']).count()
temp['sales'] = round(temp['sales'] / temp['count'], 0)


for i in range(info.shape[0]):
    info.loc[i, 'sales'] = temp.loc[(info.loc[i, 'shop'], info.loc[i, 'title']), 'sales']

phone_sales.to_csv('phone_sales_t.csv')
info.to_csv('phone_info_t.csv', index=False)

