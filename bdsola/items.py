# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BdsolaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field();
    filesize = scrapy.Field();
    filetype = scrapy.Field();
    stime = scrapy.Field();    #文件共享时间
    downurl = scrapy.Field(); #下载链接 
    curview = scrapy.Field(); 
    shareusr = scrapy.Field();#分享者名字
    picname = scrapy.Field();#分享者头像
    userid  =   scrapy.Field();
    sh      =   scrapy.Field();
    shareip =   scrapy.Field();
    
    
    
    pass
