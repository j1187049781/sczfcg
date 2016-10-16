# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request

from sczfcg.items import SczfcgItem


class SczfcgSpider(scrapy.Spider):
    name = "sczfcg"
    allowed_domains = ["sczfcg.com"]
    page = 1
    cg_url_pre = 'http://www.sczfcg.com/CmsNewsController.do?method=recommendBulletinList&rp=25&moreType=provincebuyBulletinMore&channelCode=cggg&page='
    jg_url_pre = 'http://www.sczfcg.com/CmsNewsController.do?method=recommendBulletinList&rp=25&moreType=provincebuyBulletinMore&channelCode=jggg&page='
    start_urls = (
        jg_url_pre + str(page),
        cg_url_pre + str(page),
    )

    def parse(self, response):
        #  抓取公告链接
        url = 'http://www.sczfcg.com'
        selectli = response.selector.xpath('//div[@class="colsList"]/ul/li/a/@href').extract()
        for href in selectli:
            href = url + href
            yield Request(href, callback=self.parseItem)
        # 判断是否最后一页
        lastPage = response.selector.xpath('//a[@id="QuotaList_last"]')
        if lastPage:
            self.page += 1
            url_next = re.sub(r"page=([0-9]*)", "page=" + str(self.page), response._url)
            yield Request(url_next, callback=self.parse)

    def parseItem(self, response):
        selectTable = response.selector.xpath('//table')
        item = SczfcgItem()
        item['projectName'] = (selectTable.xpath('//tr[1]/td[2]/text()')).extract()[0].encode('utf-8').strip()
        item['procurementMethod'] = (selectTable.xpath('//tr[3]/td[2]/text()')).extract()[0].encode('utf-8').strip()
        yield item
