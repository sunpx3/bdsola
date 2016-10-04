# -*- coding: UTF8 -*- 
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bdsola.items import BdsolaItem
from scrapy.selector import Selector
from scrapy.http import Request
import time
import random
import logging

class searchBookSpider(CrawlSpider):

    name = 'bdsola';
    # base_domain = ['http://quanxiaoshuo.com'];
    start_urls = ['http://www.bdsola.com/d/1.html'];
    
    i = 1;  # 共享自增量

    def parse(self, response):
        # 数据获取
        sel = Selector(response);
        items = BdsolaItem();  
        # 获取持久化状态
        searchBookSpider.i = self.state.get('items_count', 0);
        
        # 碰到异常格式默认为.
        items['title'] = sel.xpath("//div[@class='ftitle']/h1/text()").extract()[0].encode('utf-8');
        # 编码 处理
         
        # 处理异常文件类型
        try:
            items['filetype'] = sel.xpath("//div[@class='f-ext']/span[1]/text()").re('\.(\w+)')[0].encode('utf-8');
        except Exception:
            items['filetype'] = '文件夹';
        #***********************************#   
        try:
            items['userid'] = sel.xpath("//div[@class='info']/span/a/@href").re("uid=(\d+)")[0];
        except Exception:
            items['userid'] = '123456789';
        #***********************************#   
        try:
            # 将日期转为时间戳
            tempTime = sel.xpath("//div[@class='f-ext']/span[1]").re('\d+-\d+\d+-\d+\s+\d+:\d+:\d+')[0];
            timeArray = time.strptime(tempTime, "%Y-%m-%d %H:%M:%S");
            items['stime'] = int(time.mktime(timeArray));
        except Exception:
            items['stime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()));
            
        items['downurl'] = sel.xpath("//div[@class='f-ext']/span[3]/a/@href").extract_first().encode('utf-8');
        items['shareusr'] = sel.xpath("//div[@class='info']//span/b/text()").extract_first().encode('utf-8');
        items['picname'] = sel.xpath("//div[@class='info']/p/img/@src").extract_first().encode('utf-8');
        items['filesize'] = str((int)(random.random() * 10 + 30)) + " M";
        items['curview'] = 0;
        items['sh'] = 1;
        items['shareip'] = '127.0.0.1';
            
        yield items;
       
        #********获取下一页url并加入队列中***********************************************************************
        
        if searchBookSpider.i < 200:
            searchBookSpider.i += 1;
            # 持久化该状态
            self.state['items_count'] = searchBookSpider.i;
            url = "http://www.bdsola.com/d/" + str(searchBookSpider.i) + ".html";
        else:
            logging.info("抓取结束");
            return;

        yield Request(url, callback=self.parse);
            


        

       
    
