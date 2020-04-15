from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

file = open('../phone_info.json', 'w', encoding='utf-8')
file.write('[\n')

opt = webdriver.ChromeOptions()
opt.headless = False
driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=opt)

driver.get('https://www.taobao.com/')

# 在输入框输入“手机”，回车，搜索成功后点击按销量排序。
elem = driver.find_element_by_xpath('//*[@id="q"]')
elem.send_keys("手机")
elem.send_keys(Keys.RETURN)
time.sleep(15)
sort = driver.find_element_by_xpath('//*[@id="J_relative"]/div[1]/div/ul/li[2]/a')
item_list = []
sort.click()
time.sleep(3)

# 找到列出搜索结果的地方

# 爬取前2页
for page_num in range(2):

    items = driver.find_element_by_xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]')
    for item in range(1, 45):
        # 点进详情页
        print(item)
        detail = items.find_element_by_xpath(f'./div[{item}]/div[1]/div/div[1]/a')
        detail.click()
        time.sleep(2)
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        # 寻找标签tb-metatit
        try:
            metas = driver.find_elements_by_class_name('tb-metatit')
        except Exception as err:
            print(err)
        else:
            types = []
            storage = []
            # 有的手机根据存储容量分不同版本，有的手机根据版本类型分别
            for meta in metas:
                if str(meta.text).startswith("存储容量"):
                    print(meta.text)
                    storage = meta.find_elements_by_xpath('..//li')
                if str(meta.text).startswith('版本类型'):
                    types = meta.find_elements_by_xpath('..//li')
            print(types)
            print(storage)
            if len(storage) == 0:
                pass
            elif len(storage) == 1 and len(types) <= 1:  # 只有一种存储容量，不分版本类型或只有一种。
                phone_info = {'type': str(storage[0].find_element_by_xpath('.//a/span').text)}
                try:  # 尝试在促销价栏里找价格，如果没找到就再去J_StrPriceModBox里找
                    phone_info['price'] = str(driver.find_element_by_xpath('//div[contains(@class, "tm-promo-price")]/span').text)
                except Exception as err:
                    print(err)
                    phone_info['price'] = str(driver.find_element_by_id('J_StrPriceModBox').find_element_by_xpath('.//span[@class="tm-price"]').text)
                phone_info['sales'] = str(driver.find_element_by_id('J_ItemRates').find_element_by_class_name('tm-count').text)
                phone_info['shop'] = str(driver.find_element_by_class_name('slogo-shopname').text)
                title = driver.find_element_by_class_name('tb-detail-hd')
                phone_info['title'] = str(title.find_element_by_xpath('.//a').text)
                item_list.append(phone_info)
                json_str = '\t\t' + json.dumps(phone_info, ensure_ascii=False) + ',\n'
                file.write(json_str)

            elif len(storage) == 1 and len(types) > 1:  # 只有一种存储容量，分多种版本类型。
                for i in types:
                    try:
                        # 尝试点击当前种类，获得更新后的价格
                        i.find_element_by_xpath('.//a').click()
                    except Exception as err:
                        print(err)
                    else:
                        phone_info = {}
                        time.sleep(1)
                        phone_info['type'] = str(i.find_element_by_xpath('./a/span').text)
                        try:  # 尝试在促销价栏里找价格，如果没找到就再去J_StrPriceModBox里找
                            phone_info['price'] = str(driver.find_element_by_xpath(
                                '//div[contains(@class, "tm-promo-price")]/span').text)
                        except Exception as err:
                            print(err)
                            phone_info['price'] = str(driver.find_element_by_id('J_StrPriceModBox').find_element_by_xpath(
                                './/span[@class="tm-price"]').text)
                        phone_info['sales'] = str(driver.find_element_by_id('J_ItemRates').find_element_by_class_name(
                            'tm-count').text)
                        phone_info['shop'] = str(driver.find_element_by_class_name('slogo-shopname').text)
                        title = driver.find_element_by_class_name('tb-detail-hd')
                        phone_info['title'] = str(title.find_element_by_xpath('.//a').text)
                        item_list.append(phone_info)
                        json_str = '\t\t' + json.dumps(phone_info, ensure_ascii=False) + ',\n'
                        file.write(json_str)
            else:
                for i in storage:
                    try:
                        # 尝试点击当前种类，获得更新后的价格
                        i.find_element_by_xpath('.//a').click()
                    except Exception as err:
                        print(err)
                    else:
                        phone_info = {}
                        time.sleep(1)
                        phone_info['type'] = str(i.find_element_by_xpath('./a/span').text)
                        try:
                            phone_info['price'] = str(driver.find_element_by_xpath('//div[contains(@class, "tm-promo-price")]/span').text)
                        except Exception as err:
                            print(err)
                            phone_info['price'] = str(driver.find_element_by_id('J_StrPriceModBox').find_element_by_xpath('.//span[@class="tm-price"]').text)
                        phone_info['sales'] = str(driver.find_element_by_id('J_ItemRates').find_element_by_class_name('tm-count').text)
                        phone_info['shop'] = str(driver.find_element_by_class_name('slogo-shopname').text)
                        title = driver.find_element_by_class_name('tb-detail-hd')
                        phone_info['title'] = str(title.find_element_by_xpath('.//a').text)
                        item_list.append(phone_info)
                        json_str = '\t\t' + json.dumps(phone_info, ensure_ascii=False) + ',\n'
                        file.write(json_str)
        driver.close()
        driver.switch_to.window(windows[0])
    # 翻页
    next_page = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/ul/li[3]/a')
    next_page.click()
    print("next_page.click()")
    time.sleep(2)

# 关闭文件和浏览器
file.write('\t]')
file.close()
driver.close()


