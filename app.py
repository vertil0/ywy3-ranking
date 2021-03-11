import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class Chel(Item):
    Company = Field()
    Name = Field()
    LevelAudition = Field()
    ep2 = Field()
    ep4 = Field()
    ep6 = Field()

class MySpider(scrapy.Spider):
    name = "ywy3"
    start_urls = ["https://en.wikipedia.org/wiki/Youth_With_You_(season_3)"]

    def parse(self, response):
        chuva4ki = response.xpath('//table/tbody/tr/td[1][contains(text(), "Independent Trainees")]/../../tr')
        rowspan = 0
        current_company = None
        first_row_is_company = True
        for chuvak in chuva4ki[3:]:
            if rowspan <= 1: rowspan = int(chuvak.xpath("td[1]/@rowspan").extract_first())
            item = Chel()
            if rowspan and first_row_is_company:
                rowspan = int(rowspan)
                current_company = chuvak.xpath("td[1]/text()").extract_first().strip() or chuvak.xpath("td[1]/a/text()").extract_first().strip()
            if first_row_is_company:
                item["Company"] = chuvak.xpath("td[1]/text()").extract_first().strip() or chuvak.xpath("td[1]/a/text()").extract_first().strip()
                item["Name"] = chuvak.xpath("td[2]/text()").extract_first().strip() or chuvak.xpath("td[2]/a/text()").extract_first().strip()
                item["LevelAudition"] = chuvak.xpath("td[4]/text()").extract_first().strip() 
                item["ep2"] = chuvak.xpath("td[7]/text()").extract_first().strip() 
                item["ep4"] = chuvak.xpath("td[8]/text()").extract_first().strip() 
                item["ep6"] = chuvak.xpath("td[9]/text()").extract_first().strip() 
            elif rowspan > 1:
                item["Name"] = chuvak.xpath("td[1]/text()").extract_first().strip() or chuvak.xpath("td[1]/a/text()").extract_first().strip()
                item["Company"] = current_company
                item["LevelAudition"] = chuvak.xpath("td[3]/text()").extract_first().strip()
                if "Hussein" in item["Name"]:
                    item["ep2"] = "119"
                    item["ep4"] = "119"
                    item["ep6"] = "119"
                else:
                    item["ep2"] = chuvak.xpath("td[6]/text()").extract_first().strip() 
                    item["ep4"] = chuvak.xpath("td[7]/text()").extract_first().strip() 
                    item["ep6"] = chuvak.xpath("td[8]/text()").extract_first().strip() 
                rowspan = rowspan - 1
                if rowspan <= 1:
                    first_row_is_company = True
            if rowspan > 1:
                first_row_is_company = False
            yield item
process = CrawlerProcess(settings={
    "FEEDS": {
        "main.csv": {"format": "csv"},
    },
})

process.crawl(MySpider)
process.start() 