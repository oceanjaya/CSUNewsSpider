import scrapy

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
            title=''
            time=''
            for content in response.css('.subCont p::text').extract():
                contents+=content
            title+=response.css('.subTitle2 span::text').extract()[0]
            time+=response.css('.otherTme::text').extract()[1]
            yield{
                'title':title,
                'time' :time,
                'contents':contents,
            }
        except:
            pass