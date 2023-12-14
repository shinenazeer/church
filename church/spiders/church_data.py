import scrapy


class ChurchDataSpider(scrapy.Spider):
    name = "church_data"
    allowed_domains = ["churches.sbc.net"]
    start_urls = ["https://churches.sbc.net/?_paged=1"]

    def parse(self, response):
        churches = response.css("div.fwpl-result")
        for ch in churches:
            url = ch.css("div.fwpl-item a::attr(href)").get()
            yield response.follow(url,self.parse_church_profile)

        for i in range(2, 42):
            yield response.follow(f"https://churches.sbc.net/?_paged={i}", self.parse)

    def parse_church_profile(self, response):
        yield {
            "Name": response.css("h1.heading__title::text").get().strip(),
            "Address": response.css("h3.heading__address::text").get().strip(),
            "Phone": response.css("p.heading__phone::text").get()
        }