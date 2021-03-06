# coding=utf-8
import scrapy
import MySQLdb
import re
from CSUNewsSpider.items import NewsItem,AcademicItem,JobsItem
db=MySQLdb.connect("localhost","spider","xyz","csuspider")
cursor = db.cursor()
db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

class CSUNewsSpiders(scrapy.Spider):
    name="CSUNews"
    allowed_domains=["news.csu.edu.cn"]
    start_urls=["http://news.csu.edu.cn/xxyw.htm"]
    def parse(self,response):
        for sel in response.xpath('//ul/li'):
            news_urls='http://news.csu.edu.cn/'+sel.xpath('a/@href').extract()[0]
            yield scrapy.Request(news_urls,callback=self.parse_links_content)

    def parse_links_content(self,response):
        try:
            content=response.xpath('string(//div[@class="subCont"])').extract()[0]
            content=content.replace(u'&', u'&amp;')
            content=content.replace(u'<',u'&lt;')
            title=response.xpath('//*[@class="subTitle2"]/span/text()').extract()[0]
            date='-'.join(response.xpath('//*[@class="otherTme"]/text()').re(r'(\d+)'))


            url=response.url
            news=NewsItem({
                'title':title,
                'date' :date,
                'content':content,
                'url':url,
            })
            yield  news
            sql = """insert into news(title,content, date,url) values ('%s', '%s','%s','%s')"""\
                  %(title.encode('utf-8'),content.encode('utf-8'),date.encode('utf-8'),url.encode('utf-8'))
            try:
                cursor.execute(sql)
                db.commit()
            except Exception,e:
                print e
        except Exception,e:
            print e


class CSUAcademicSpider(scrapy.Spider):
    name="CSUAcademic"
    allowed_domains=["sise.csu.edu.cn"]
    start_urls=["http://sise.csu.edu.cn/index/xsbg.htm"]
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
            contents=contents.replace(u'&', u'&amp;')
            contents=contents.replace(u'<',u'&lt;')
            title=response.xpath('//h3[contains(@class,"newsTitle")]/text()').extract()[0]
            date_re_words = re.compile(u"间：(.+)\r")
            date=date_re_words.search(contents, 0).group(1)
            date_tuple=re.findall(u"(\d+)月(\d+)[日号]",date)[0]
            year=response.xpath('//p[@class="newsTO"]/text()').re(r'(\d+)')[0]
            month=date_tuple[0]
            day=date_tuple[1]
            if(len(month)==1):
                month='0'+month
            if(len(day)==1):
                day='0'+day
            date_sort=year+month+day
            location_re_words = re.compile(u"点：(.+)\r")
            location=location_re_words.search(contents, 0).group(1)
            type=u"academic"
            academic=AcademicItem({
                'title':title,
                'date' :date,
                'location':location,
                'content':contents,
                'url':url,
                'type':type,
                'date_sort':date_sort
             })
            yield academic
            sql = "insert into info(title,content, date,url,location,type,date_sort ) values ('%s', '%s','%s','%s','%s','%s','%s')"\
                  %(title.encode('utf-8'),contents.encode('utf-8'),date.encode('utf-8'),url.encode('utf-8'),
                    location.encode('utf-8'),type.encode('utf-8'),date_sort.encode('utf-8'))
            try:
                cursor.execute(sql)
                db.commit()
            except Exception,e:
                print e
        except Exception,e:
            print e



class CSUJobsSpider(scrapy.Spider):
    name="CSUJobs"
    allowed_domains=["jobsky.csu.edu.cn"]
    start_urls=["http://jobsky.csu.edu.cn:8000/Home/ListNews.aspx?typeid=1"]
    def parse(self,response):
        for suburl in response.xpath('//div[@id="listAll"]/div/div/table/tr[@class="data"]/td[@class="articletitle"]/a/@href').extract():
            job_urls='http://jobsky.csu.edu.cn:8000/Home/'+suburl
            #yield job_urls
            yield scrapy.Request(job_urls,callback=self.parse_links_content)

    def parse_links_content(self,response):
        try:
            url=response.url
            contents=response.xpath('string(//div[@id="articleContent"])').extract()[0].replace(u'\xa0', u'\r\n')
            contents=contents.replace(u'&', u'&amp;')
            contents=contents.replace(u'<',u'&lt;')
            title=response.xpath('//span[@id="ContentPlaceHolder1_lbltitle"]/text()').extract()[0]
            date_re_words = re.compile(u"招聘时间：([\s\S]+?)招聘地点：")
            date=date_re_words.search(contents, 0).group(1).replace(u"\r\n",u" ")
            date_tuple=re.findall(u"(\d+)年(\d+)月(\d+)[日号]",date)[0]
            year=date_tuple[0]
            month=date_tuple[1]
            day=date_tuple[2]
            if(len(month)==1):
                month='0'+month
            if(len(day)==1):
                day='0'+day
            date_sort=year+month+day
            location_re_words = re.compile(u"招聘地点：(.+?)\r")
            location=location_re_words.search(contents, 0).group(1).replace(u"\r\n",u" ")
            type=u"jobs"
            job=JobsItem({
                'title':title,
                'date' :date,
                'location':location,
                'content':contents,
                'url':url,
                'type':type,
                'date_sort':date_sort
             })
            yield job
            sql = "insert into info(title,content, date,url,location,type,date_sort ) values ('%s', '%s','%s','%s','%s','%s','%s')"\
                  %(title.encode('utf-8'),contents.encode('utf-8'),date.encode('utf-8'),url.encode('utf-8'),
                    location.encode('utf-8'),type.encode('utf-8'),date_sort.encode('utf-8'))
            try:
                cursor.execute(sql)
                db.commit()
            except Exception,e:
                print e
        except Exception,e:
            print e

