# -*- coding: utf8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from bdsola import items
from MySQLdb import connect
from scrapy.utils.project import get_project_settings  
from twisted.enterprise import adbapi


class BdsolaPipeline(object):
    
#     def __init__(self):
#         settings = get_project_settings();
#         dbdic = dict(host=settings['MYSQL_HOST'],
#                     user=settings['MYSQL_USER'],
#                     passwd=settings['MYSQL_PASSWD'],
#                     db=settings['MYSQL_DBNAME'],
#                     port=settings['MYSQL_PORT'],
#                     charset='utf8')
#         self.dbpool = adbapi.ConnectionPool("MySQLdb",dbdic);
#         
    
    def process_item(self, item, spider):
        settings = get_project_settings();
        conn = connect(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            db=settings['MYSQL_DBNAME'],
            port=settings['MYSQL_PORT'],
            charset='utf8');
        
        cur = conn.cursor();
        filetype = item['filetype'];
        table = '';
        
        vedio = ["m4v", "mk", "mkv", "mov", "mp4", "mpg", "msi", "pps", "rmvb", "vob", "webm", "wmv", "rm", "avi", "3gp"];
        doc = ["doc", "xls", "pdf", "ppt", "txt", "wps", "xlsx", "xdoc", "pptx", "docx", "epud"];
        music = ["mp3", "flac", "wma", "wav", "mod", "cd", "ra", "md", "asf", "aac", "mid", "ape", "amr"];
        picture = ["bmp", "exif", "tiff", "gif", "psd", "ai", "jpeg", "png", "jpg", "cdr"];
        soft = ["exe", "apk", "ipa"];
        file = ["file", "文件夹"];
        zips = ["rar", "zip", "tar", "7z"];
        other = ['torrent'];
        
        # cursor.execute('''insert into call_number VALUES （%s,%s,%s）'''%(year,time,call)
        for v in vedio:
            if filetype == v:
                table = '`ntj_videos`';
                break;
        for d in doc:
            if filetype == d:
                table = '`ntj_docs`';
                break;
        for m in music:
            if filetype == m:
                table = '`ntj_musics`';
                break;
        for p in picture:
            if filetype == p:
                table = '`ntj_pics`';
                break;
        for s in soft:
            if filetype == s:
                table = '`ntj_softs`';
                break;
        for f in file:
            if filetype == f:
                table = '`ntj_files`';
                
                break;
        for z in zips:
            if filetype == z:
                table = '`ntj_zips`'
                break;
        if filetype == other[0]:
            table = '`ntj_others`';
            
        # 无法实别类型默认为ntj_files表
        if table == '':
            table = '`ntj_files`';
    
        # 开启事物
        try:
            sql = "insert into {0}(title,filesize,filetype,stime,downurl,curview,shareusr,picname,shareip,sh,usrid) values('{1}','{2}','{3}',{4},'{5}',{6},'{7}','{8}','{9}',{10},'{11}')".format(table, item['title'],
                    item['filesize'], item['filetype'], item['stime'], item['downurl'],
                    item['curview'], item['shareusr'], item['picname'], item['shareip'], item['sh'], item['userid']);
            cur.execute(sql);
            conn.commit();
        except Exception:
            cur.close();
            conn.rollback();
        finally:
            conn.close();
            
        return item
