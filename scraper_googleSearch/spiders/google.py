import scrapy
from scrapy.http.request import Request
import re


class GoogleSpider(scrapy.Spider):
    name = 'google'

    HEADERS = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        'referer': None
    }

    def start_requests(self):
        urls = [ "https://www.google.com/search?q=aspria+berlin+ku%27damm&oq=aspria+berlin+ku%27damm&aqs=chrome.0.0i355i512j46i175i199i512j69i59j0i30i625l6.3380j0j7&sourceid=chrome&ie=UTF-8#lrd=0x47a850c4b634ef93:0x2faf0f02eacd864e,1,,,,"
        ]

        for url in urls:
            async_id = url.split("lrd=")[1].split(",")[0]
            ajax_url = "https://www.google.com/async/reviewDialog?async=feature_id:" + str(
                async_id) + ",start_index:0,_fmt:pc,sort_by:newestFirst"
            yield Request(url=ajax_url, cookies= {'googletrans': '/en'},headers=self.HEADERS, callback=self.get_total_iteration)

    def get_total_iteration(self, response):
        total_reviews_text = response.css('.z5jxId::text').extract_first()
        total_reviews = int(re.sub(r'[^0-9]', '', total_reviews_text))

        temp = total_reviews / 10  # since
        new_num = int(temp)
        if temp > new_num:
            new_num += 1
        iteration_number = new_num

        j = 0
        if total_reviews > 10:
            for _ in range(0, iteration_number + 1):
                yield Request(url=response.request.url.replace('start_index:0', f'start_index:{j}'),
                              headers=self.HEADERS, callback=self.parse_reviews, dont_filter=True)
                j += 10
        else:
            yield Request(url=response.request.url, headers=self.HEADERS, callback=self.parse_reviews, dont_filter=True)

    def parse_reviews(self, response):
        all_reviews = response.xpath('//*[@id="reviewSort"]/div/div[2]/div')

        for review in all_reviews:
            reviewer = review.css('div.TSUbDb.w6Pmwe a::text').extract_first()
            review_content = review.css('div.review-full-text span::text').extract_first()
            link = review.css('div.TSUbDb a::attr(href)').extract_first()
            owner_response= str(review.css('div.lororc span::text').extract_first())
            owner_answer_date = review.css('div.LfKETd span::text').extract_first()
            owner_responded = False
            if len(owner_response) > 0 :
                owner_responded = True
                  
            if review_content is None:
                review_content = review.css('.Jtu6Td span::text').extract_first()
                if review_content is None:
                    review_content = ''
            review_rating  = int(str(review.xpath('.//span[@class="pjemBf"]/text()').extract_first()).replace("/5",""))
            #review_rating = review.xpath('.//span[@class="Fam1ne EBe2gf"]/@aria-label').extract_first().split(" ")[1]
            review_date = review.xpath('.//span[@class="Qhbkge"]/text()').extract_first()
            yield {

                "Reviewer Name" : reviewer,
                "Review content" : review_content,
                "Full review link":link,
                "Rating" : review_rating,
                "Review Time Information":review_date,
                "shop owner reply": owner_responded,
                "shop owner text": owner_response,
                "shop owner answer time": owner_answer_date
   
            }
