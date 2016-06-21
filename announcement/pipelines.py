# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class AnnouncementPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        #return item
        db = self.dbpool.runInteraction(self._do_replace, item, spider)
        db.addErrback(self._handle_error, item, spider)
        db.addBoth(lambda _: item)
        return db

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
            )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def _do_replace(self, conn, item, spider):
         if item['id'] != "":
            try:
                #print item['content']
                #conn.execute("REPLACE INTO announcement(id, code, name, title, content, time) values(%s, %s, %s, %s, %s, %s)", (item['id'], item['code'], item['name'], item['title'], item['content'], item['time']))
                conn.execute("REPLACE INTO announcement(id, code, name, title, content, time) values(%s, %s, %s, %s, %s, %s)", (item['id'], item['code'], item['name'], item['title'], item['content'].replace("\r\n", ""), item['time']))
                #conn.execute("select * from announcement")
            except Exception as e:
                print "*******************88889", e
                pass

    def _handle_error(self, failure, item, spider):
        print failure 
        log.err(failure)
