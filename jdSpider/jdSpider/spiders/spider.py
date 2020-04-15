import scrapy
from jdSpider.items import JdspiderItem
from scrapy import Selector
import time


class JdSpider(scrapy.Spider):
    """
    由于京东的反爬虫机制，需要设置cookie和headers，
    另外，京东的商品详情页是异步加载的，所以这个爬虫需要和selenium配合使用（中间件）
    """
    name = 'JdSpider'
    # 伪装为浏览器访问
    headers1 = {
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    # 使用cookie防止被重定向
    cookieStr = 'shshshfpa=6f029e6b-f9a9-7a84-c60f-2bef73572e36-1538057638; shshshfpb=09552f22e2672164e7d67678026754b2ab8875369e7a754715bace5a7b; __jdu=15380576375691494136499; pinId=dbTG4l12mpTNq2iXUS9enLV9-x-f3wj7; unpl=V2_ZzNtbUVUQRd2XURQLhgMAmILEFhLXhAWdFhFBykeXwEyAhEKclRCFX0URlRnG10UZAIZWEJcQhBFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsdXgxmBxRaQFFHEn0IQ1x%2bGV4CYgsabXJQcyVFAUVdcx5sBFcCIh8WC0ARfAFHUjYZWAduAhZbRVVFEXIARlFzHFwHYAYaVXJWcxY%3d; pin=jd_6e92c7c6be686; unick=jd_6e92c7c6be686; _tp=PFFEsxb5ge6L1Q6jhWV19jKyjb9adsEAvN6cPm2BlXU%3D; _pst=jd_6e92c7c6be686; user-key=7b77380c-e652-499a-8b78-b9f32df673fc; cn=1; __jdv=76161171|direct|-|none|-|1577283459353; PCSYCityID=CN_110000_110100_110108; areaId=1; ipLoc-djd=1-2800-2848-0; TrackID=1ZywLzCn9sCWzTsjA0tiUq9qJKDHQ7DUk8LCA-Lozea2D1t9cwyNtbLhFrvd57UghOm-sQTXM7Mfc8SAmLJ50VRQxf-ZExG_0ztP4vnUds3E; thor=0F177F8B0F4C19424A5E1FCE9FC1B7D05B3D3FCDED30F0AC62D071AEB4E01340DFD003E661EC897BC7D475DF767BE85EC959D6F13A77580E40B622EB444EA4BEB0381AD77BBB8429CCFE128CC2A8B5D735669C162E161637A2FCAE2EDEDA425D25E0175D3BAC0D3F9345B4E32D38E2FCDA9EE8C6864D47CA3988D8ADEEB7E685D1EC4C5123E3B0C652C87736CF2FF15BCDE07732F24C6F35384CECA5BBA8858C; ceshi3.com=103; __jda=122270672.15380576375691494136499.1538057637.1577319270.1577327150.27; __jdc=122270672; 3AB9D23F7A4B3C9B=QGITJ7IPWECCN3NTGB4VKF4YRHS2XAPPBZKCBKYQQO6W2UWYEH5DZKTGJ2ZKQN5X45REWXZJ7OLFXFJGP2ARFSRQ3A; shshshfp=5701747be5d14fbaaa0099b0930c59dd; shshshsID=7471b0f1c4ef45472edabb7406d88e55_3_1577327172615; __jdb=122270672.6.15380576375691494136499|27.1577327150'
    cookieDic = {i.split("=", 1)[0]: i.split("=", 1)[1] for i in cookieStr.split(";")}

    cookies = cookieDic
    count = 0
    shop_count = 0

    def start_requests(self):
        yield scrapy.Request(
            'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=shou%27ji&psort=3&click=0')

    def parse(self, response):

        page = Selector(response)

        # 获得每个商品详情页的链接，进行进一步分析
        for i in range(1, 60):
            url = page.xpath(f'//*[@id="J_goodsList"]/ul/li[{i}]//div[@class="p-name p-name-type-2"]//a/@href').get()
            yield scrapy.Request('https:' + url, callback=self.parse_urls, headers=self.headers1, cookies=self.cookies)

    def parse_urls(self, response):

        page = Selector(response)
        item = JdspiderItem()
        item_number = page.xpath('//div[@data-type="版本"]/div/div')
        print(item_number)
        print(item_number.get())
        # 如果只有当前版本，不能进行版本选择，直接返回item
        if len(item_number) == 0:
            try:
                with open(f'only_one{self.shop_count}.html', 'w', encoding='utf-8') as f:
                    f.write(page.text)
                    self.shop_count += 1
            except Exception as err:
                print(err)
            item["price"] = str(page.xpath('//span[@class="p-price"]/span[2]/text()').get())
            item["phone_type"] = 'Na'
            item['shop'] = str(page.xpath('//div[@class="J-hove-wrap EDropdown fr"]/div/div/a/@title').get())
            item['sales'] = str(page.xpath('//div[@id="comment-count"]//a/text()').get())
            item['title'] = str(page.xpath('//div[@class="sku-name"]/text()').get())
            yield item
        # 如果有多个版本，通过拼接获得每个版本的链接再进行进一步分析
        for i in item_number:
            url = 'https://item.jd.com/' + str(i.xpath('./@data-sku').get()) + '.html#crumb-wrap'
            print(i.xpath('./@data-sku').get())
            print(i.xpath('./@data-value').get())
            print(url)
            yield scrapy.Request(url=url, headers=self.headers1, dont_filter=True, cookies=self.cookies,
                                 callback=self.parse_detail, cb_kwargs=dict(storage=i.xpath('./@data-value').get()))

    def parse_detail(self, response, storage):
        # 获得商品信息并返回item
        print("==========================parse_detail=====================")
        page = Selector(response)

        item = JdspiderItem()

        item["price"] = page.xpath('//span[@class="p-price"]/span[2]/text()').get()
        if item["price"] is None:
            item["price"] = page.xpath('//span[@class="p-price ys-price"]/span[2]/text()').get()
            if item["price"] is None:
                item["price"] = page.xpath('//div[@class="summary-price J-summary-price"]'
                                           '//span[@class="p-price"]/span[2]/text()').get()

        item["phone_type"] = storage
        item['shop'] = page.xpath('//div[@class="J-hove-wrap EDropdown fr"]/div/div/a/@title').get()
        item['sales'] = page.xpath('//div[@id="comment-count"]//a/text()').get()
        if item['sales'] is None:
            item['sales'] = page.xpath('//li[@data-anchor="#comment"]/s/text()').get()
        item['title'] = page.xpath('//div[@class="sku-name"]/text()').get()
        if item["title"] == "\n                                        ":
            temp = page.xpath('//div[@class="sku-name"]/text()').getall()
            item["title"] = temp[1]
        print(item)
        if item["price"] is None:
            f = open(f'error{self.count}.html', 'w', encoding='utf-8')
            self.count += 1
            f.write(response.text)
            f.close()
        if item["phone_type"] and item["price"] and item["sales"] and item["title"]:
            item["price"] = str(item["price"])
            item["shop"] = str(item["shop"])
            item["sales"] = str(item["sales"])
            item["title"] = str(item["title"])
            yield item
