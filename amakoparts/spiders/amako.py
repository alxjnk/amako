import scrapy
import json
import re


def float_serializer(value):
    if value == 'запрос':
        return 0
    if value:
        return float(re.search(r'\d+.\d+', value).group())
    return value


def quantity_serializer(value):
    if value == '&gt;10':
        value = '10'
    return int(re.search(r'\d+', value).group())


class Product(scrapy.Item):
    DT_RowId = scrapy.Field()
    title = scrapy.Field()
    partid = scrapy.Field()
    manufacturerid = scrapy.Field()
    manufacturer = scrapy.Field()
    quantity = scrapy.Field(serializer=quantity_serializer)
    price = scrapy.Field(serializer=float_serializer)
    actionprice = scrapy.Field()
    rep = scrapy.Field()
    img = scrapy.Field()
    replacements = scrapy.Field()
    img_link = scrapy.Field()
    manufacturer_img = scrapy.Field()


class MySpider(scrapy.Spider):
    name = 'amako'
    start_urls = [
        'https://parts.amaco.ua/ru/man/',
    ]

    def parse(self, response):
        ln = 999999
        hrefs = ('response url', response.selector.xpath(
            '//*[@id="List"]/li/a/@href').getall())
        titles = ('response url', response.selector.xpath(
            '//*[@id="List"]/li/a/@title').getall())
        man_imgs = ('response url', response.selector.xpath(
            '//*[@id="List"]/li/a/img/@src').getall())

        for href, title, imgs in zip(hrefs, titles, man_imgs):
            for h, t, i in zip(href, title, imgs):
                yield scrapy.http.Request('https://parts.amaco.ua/services/search/data.html?draw=1&columns%5B0%5D%5Bdata%5D=title&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=manufacturer&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=partid&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=quantity&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=price&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length={1}&search%5Bvalue%5D=&search%5Bregex%5D=false&lang=1&manufacturer={0}&_=1577614837927'.format(h[2:-1], ln), callback=self.parse_manufacturer, meta={'manufacturer': t, 'man_img': i}, dont_filter=True)
                # break
# https://parts.amaco.ua/ru/part/4ba5315f-f513-11e3-b5c5-00155d012119

    def parse_manufacturer(self, response):
        jsonresponse = json.loads(
            response.body_as_unicode())
        manufacturer = response.meta.get('manufacturer')
        man_img = response.meta.get('man_img')

        for item in jsonresponse['data']:
            product = Product(item)
            product['manufacturer'] = manufacturer
            product['manufacturer_img'] = 'https://parts.amaco.ua/ru' + man_img
            yield scrapy.http.Request('https://parts.amaco.ua/ru/part/{0}'.format(item['DT_RowId']), callback=self.parse_parts, meta={'product': product}, dont_filter=True)
            # break

    def parse_parts(self, response):
        product = response.meta.get('product')
        img = response.selector.xpath('//*[@id="Images"]/img/@src').get()
        replacements = [];
        for row in response.selector.xpath('//*[@id="Replacements"]/table/tbody/tr'):
            row = row.xpath('td/a/text()').extract()
            if len(row) == 3:
                replacements.append(row[1] + ' ' + row[0])
            if len(row) == 4:
                replacements.append(row[2] + ' ' + row[0])
        if img == None:
            img = 'no image'
        else:
            img = 'https://parts.amaco.ua/ru' + img
        product['quantity'] = str(product['quantity'])
        product['img_link'] = img
        product['replacements'] = replacements
        product['title'] = product['partid'] + ' ' + product['title']
        yield product
