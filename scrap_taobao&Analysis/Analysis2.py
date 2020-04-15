import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

tb = pd.read_csv('phone_info_t.csv')
jd = pd.read_csv('phone_info_j.csv')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    price_shop_j = jd[['price', 'shop']].groupby('price').count()
    price_shop_t = tb[['price', 'shop']].groupby('price').count()
    print(price_shop_j)
    print(price_shop_t)

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
plt.subplots_adjust(hspace=0.5)

area = np.pi ** 3
ax1.set_title("京东价格-商家数对应图")
ax1.scatter(price_shop_j.index.values, price_shop_j['shop'].values, s=area, c='b', alpha=0.5)
ax2.set_title("淘宝价格-商家数对应图")
ax2.scatter(price_shop_t.index.values, price_shop_t['shop'].values, s=area, c='b', alpha=0.5)

ax1.set_xlabel('价格', alpha=0.4)
ax2.set_xlabel('价格', alpha=0.4)
ax1.set_ylabel("商家数", alpha=0.4)
ax2.set_ylabel("商家数", alpha=0.4)

ax1.grid(True, linestyle='--', alpha=0.8)
ax2.grid(True, linestyle='--', alpha=0.8)
plt.show()
