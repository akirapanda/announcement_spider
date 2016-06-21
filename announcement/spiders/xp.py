#coding = utf-8
import scrapy
import json
import time
from announcement.items import AnnouncementItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.log import configure_logging
import logging
from scrapy.crawler import CrawlerProcess


configure_logging(install_root_handler=False)
logging.basicConfig(filename="log.txt", level=logging.DEBUG)
#logging.basicConfig(filename="log.txt")

class XPSpider(scrapy.Spider):
    name = "xp"
    allowed_domains = ["eastmoney.com"]
    start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        #"http://36kr.com/newsflashes.json",
        #"http://www.cyzone.cn/category/8/",
    ]
    #log.start("log.txt", INFO)
    
    #for page in range(1,15000):
    #for page in range(1,15000):
    #for page in range(1,15000):
    #    start_urls.append("http://data.eastmoney.com/Notice/Noticelist.aspx?type=0&market=all&date=&page=" + str(page))

    def start_requests(self):
        #for page in range(4114,15000):
        for page in range(4790,15000):
        #for page in range(1,15):
            if page != 1:
                request = Request("http://data.eastmoney.com/Notice/Noticelist.aspx?type=0&market=all&date=&page=" + str(page), callback = self.parse_start, headers={'referer':'http://data.eastmoney.com/Notice/Noticelist.aspx?type=0&market=all&date=&page=' + str(page - 1)})
            else: 
                request = Request("http://data.eastmoney.com/Notice/Noticelist.aspx?type=0&market=all&date=&page=" + str(page), callback = self.parse_start, headers={'referer':'http://www.eastmoney.com/'})
            yield request

    def parse_start(self, response):
        #filename = response.url.split("/")[-2]
        #json_res = json.loads(response.body)
        ##print json_res
        logging.log(logging.WARNING, "current" + response.url[-7:]) 
        for k, v in response.request.headers.items():
            logging.log(logging.WARNING, "============" + k)
            for val in v:
                logging.log(logging.WARNING, "============" + val)
        #print response, "==========================="
        download_delay = 4

        sel = Selector(response)
        item_list = sel.xpath("//table[@id='dt']//tr")
        #print item_list
        count = 0
        for elem in item_list:
            items = AnnouncementItem()
            content_link =  elem.xpath(".//td[4]/a/@href").extract()
            if len(content_link) > 0:
                try:
                    items['code'] = elem.xpath(".//td[1]/a/text()").extract()[0] 
                    if items['code'].startswith("8") or items['code'].startswith("4"):
                        continue
                    items['name'] = elem.xpath(".//td[2]/a/text()").extract()[0]
                    items['title'] = elem.xpath(".//td[4]/a/text()").extract()[0]
                    items['time'] = elem.xpath(".//td[6]/text()").extract()[0]
                    items["content"] = "" 
                    print content_link[0] + "=============="
                    items["id"] =  content_link[0][content_link[0].rfind("/") + 1:-5]
                except Exception:
                    continue
                yield items
                #print items, content_link[0]
            #print content_link[0] + "====="
                #self.DEBUG_PRINT("count", count)
                #request = Request("http://data.eastmoney.com" + content_link[0], callback = self.parse_content, headers={'referer':response.url})
                #request = Request("http://data.eastmoney.com" + content_link[0], callback = self.parse_content, headers = {"USER_AGENT:":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1  (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"})
                #self.DEBUG_PRINT("url", 'http://data.eastmoney.com' + content_link[0])
                #request.meta["items"] = items 
                #yield request
                #break

    def parse_content(self, response):
        items = response.meta["items"]
        sel = Selector(response)
        #print response.url
        if len(sel.xpath("//pre/text()").extract()) > 0:
            items["content"] = sel.xpath("//pre/text()").extract()[0] 
        items["id"] =  response.url[response.url.rfind("/") + 1:-5]
        self.DEBUG_PRINT("items", items)
        yield items
        
    def DEBUG_PRINT(self, debug_name, debug_meta):
        pass
        #print debug_name + "'s value is :" +  "=========", debug_meta

        #    items['id'] = int(url[url.rfind("/")+1:url.rfind(".")])
        #    yield items
        #    items = CrawlCompanyWebsiteItem()
        #    items['id'] = newsflashs['id']
        #    yield items
        #for newsflashs in json_res['data']['newsflashes']:
        #    items = CrawlCompanyWebsiteItem()
        #    items['id'] = newsflashs['id']
        #    items['hash_title'] = newsflashs['hash_title']
        #    items['description_text'] = newsflashs['description_text']
        #    items['news_url'] = newsflashs['news_url']
        #    items['created_at'] = newsflashs['created_at']
        #    items['is_top'] = newsflashs['is_top']
        #    items['column_id'] = newsflashs['column_id']
        #    items['news_url_type'] = newsflashs['news_url_type']
        #    #print items['created_at']
        #    #print items['hash_title']
        #    yield items
	
	
        #with open(filename, 'wb') as f:
        #    f.write(response.body)

#process = CrawlerProcess({
#    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
#    })
#
#process.crawl(XPSpider)
#process.start() 
