# coding=utf-8
import datetime
import scrapy
import MySQLdb
db=MySQLdb.connect("localhost","spider","xyz","csuspider")
cursor = db.cursor()
db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

class CSUNewsSpider(scrapy.Spider):
    name="CSUNews"
    allowed_domains=["news.csu.edu.cn"]
    start_urls=["http://news.csu.edu.cn/xxyw.htm"]

    def parse(self,response):
        for sel in response.xpath('//ul/li'):
            news_urls='http://news.csu.edu.cn/'+sel.xpath('a/@href').extract()[0]
            yield scrapy.Request(news_urls,callback=self.parse_links_content)


    def parse_links_content(self,response):
        try:
            contents=''
            for content in response.css('.subCont p::text').extract():
                contents+=content
            title=response.css('.subTitle2 span::text').extract()[0]
            date='-'.join(response.css('.otherTme::text').re(r'(\d+)'))
            url=response.url

            yield{
                'title':title,
                'date' :date,
                'contents':contents,
                'url':url,
            }
            sql = """insert into news(title,content, date,url) values ('%s', '%s','%s','%s')"""\
                  %(title.encode('utf-8'),contents.encode('utf-8'),date.encode('utf-8'),url.encode('utf-8'))
            try:
                cursor.execute(sql)
                db.commit()
            except Exception,e:
                print e
                db.rollback()
                db.close()
        except Exception,e:
            print e
            pass
