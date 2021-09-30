from re import L
from time import sleep
import scrapy
import json

class OlhardigitalSpider(scrapy.Spider):
    name = 'olhardigital'
    start_urls = ['https://olhardigital.com.br/']
    globalData = []

    def parse(self, response, **kwargs):
        documentLink = response.xpath("//ul[@id='menu-menu-principal']/li/a/@href")[2].get()
        
        yield scrapy.Request(documentLink, callback=self.parse_getMatter)

    async def parse_getMatter(self, response):
        loopIndex = 0

        for link in response.xpath("//a[@class='card-post type8 img-effect1']/@href").getall():
            if loopIndex == 5: break
            yield scrapy.Request(link, callback=self.parse_getData)
            loopIndex += 1
    
    def parse_getData(self, response):
        self.globalData.append(dict([
            ('title',  response.xpath("//h1/text()").get())
            ,('subtitle',  response.xpath("//meta[@property='og:description']/@content").get())
            ,('date',  response.xpath("//span[@class='data icon-clock']/text()").get().split(' ')[0].strip())
            ,('time',  response.xpath("//span[@class='data icon-clock']/text()").get().split(' ')[1].replace('h', ':').replace(',', '').strip())
        ]))

        if len(self.globalData) == 5:
            out_file = open('response.json', 'w')
            json.dump(self.globalData, out_file, indent=6)
            out_file.close()
