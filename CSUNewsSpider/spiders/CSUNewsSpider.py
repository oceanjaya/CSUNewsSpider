# coding=utf-8
import scrapy
import MySQLdb
import re
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
    cursor.execute('DELETE FROM news;')
    def parse(self,response):
        for sel in response.xpath('//ul/li'):
            news_urls='http://news.csu.edu.cn/'+sel.xpath('a/@href').extract()[0]
            yield scrapy.Request(news_urls,callback=self.parse_links_content)

    def parse_links_content(self,response):
        try:
            contents=response.xpath('string(//div[@class="subCont"])').extract()[0]
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


class CSUAcademicSpider(scrapy.Spider):
    name="CSUAcademic"
    allowed_domains=["sise.csu.edu.cn"]
    start_urls=["http://sise.csu.edu.cn/index/xsbg.htm"]
    cursor.execute('DELETE FROM academic;')
    def parse(self,response):
        for sel in response.xpath('//ul[contains(@class,"eduList")]/li'):
            url_re_words = re.compile(u"info(.+)")
            _urls=sel.xpath('a/@href').extract()[0]
            sub_url=url_re_words.search(_urls,0).group(1)
            news_urls='http://sise.csu.edu.cn/info'+sub_url
            yield scrapy.Request(news_urls,callback=self.parse_links_content)

    def parse_links_content(self,response):
        try:
            url=response.url
            contents=response.xpath('string(//div[@class="topCont"])').extract()[0]
            title=response.xpath('//h3[contains(@class,"newsTitle")]/text()').extract()[0]
            date_re_words = re.compile(u"\u95f4\uff1a(.+)")
            date=date_re_words.search(contents, 0).group(1)
            location_re_words = re.compile(u"\u70b9\uff1a(.+)")
            location=location_re_words.search(contents, 0).group(1)
            yield{
                'title':title,
                'date' :date,
                'location':location,
                'contents':contents,
                'url':url,
            }
            sql = """insert into academic(title,content, date,url,location ) values ('%s', '%s','%s','%s','%s')"""\
                  %(title.encode('utf-8'),contents.encode('utf-8'),date.encode('utf-8'),url.encode('utf-8'),location.encode('utf-8'))
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

#
# class CSUNewsSpider(scrapy.Spider):
#     name="CSUNews"
#     allowed_domains=["news.csu.edu.cn"]
#     start_urls=["http://news.csu.edu.cn/xxyw.htm"]
#
#     def parse(self,response):
#         for sel in response.xpath('//ul/li'):
#             news_urls='http://news.csu.edu.cn/'+sel.xpath('a/@href').extract()[0]
#             yield scrapy.Request(news_urls,callback=self.parse_links_content)
#
#
#     def parse_links_content(self,response):
#         try:
#             contents=''
#             for content in response.css('.subCont p::text').extract():
#                 contents+=content
#             title=response.css('.subTitle2 span::text').extract()[0]
#             date='-'.join(response.css('.otherTme::text').re(r'(\d+)'))
#             url=response.url
#
#             yield{
#                 'title':title,
#                 'date' :date,
#                 'contents':contents,
#                 'url':url,
#             }
#             sql = """insert into news(title,content, date,url) values ('%s', '%s','%s','%s')"""\
#                   %(title.encode('utf-8'),contents.encode('utf-8'),date.encode('utf-8'),url.encode('utf-8'))
#             try:
#                 cursor.execute(sql)
#                 db.commit()
#             except Exception,e:
#                 print e
#                 db.rollback()
#                 db.close()
#         except Exception,e:
#             print e
#             pass
