import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

phone_sales_t = pd.read_csv('phone_sales_t.csv')
phone_sales_t.set_index('title', inplace=True)

phone_sales_j = pd.read_csv('phone_sales_j.csv')
phone_sales_j.set_index('title', inplace=True)

print(phone_sales_t)
print(phone_sales_j)

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['figure.dpi'] = 200
matplotlib.rcParams['savefig.dpi'] = 300

fig, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, figsize=(20, 15))
plt.subplots_adjust(hspace=0.8)
ax1.set_title('淘宝手机销量TOP20')
ax1.bar(phone_sales_t.index.values[:20], phone_sales_t['sales'].values[:20])

ax2.set_title('京东手机销量TOP20')
ax2.bar(phone_sales_j.index.values[:20], phone_sales_j['sales'].values[:20])
ax1.set_xlabel('机型', alpha=0.4)
ax2.set_xlabel('机型', alpha=0.4)
ax1.set_ylabel("销量", alpha=0.4)
ax2.set_ylabel("销量", alpha=0.4)
x = np.arange(0, 21, 1)

for a, sales_t, sales_j in zip(x, phone_sales_t['sales'].values[:20], phone_sales_j['sales'].values[:20]):
    ax1.text(a, sales_t, "%d" % sales_t, va='bottom', ha='center', fontsize=5)
    ax2.text(a, sales_j, "%d" % sales_j, va='bottom', ha='center', fontsize=5)

ax1.tick_params(direction='in', length=4, width=1, labelsize='x-small', rotation=30)
ax2.tick_params(direction='in', length=4, width=1, labelsize='x-small', rotation=30)

plt.show()
