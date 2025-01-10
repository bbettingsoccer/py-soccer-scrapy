import os
from datetime import datetime

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, ConnectionLost
import asyncio
from ..app.server.common import match_constants
from ..app.server.model.scrapy_response_model import ScrapyResponseModel
from ..app.server.service.scrapy_error_service import ScrapyErrorService
from twisted.internet import reactor
from webscrapy.items import WebscrapyItem


class MatchsoccerSpider(scrapy.Spider):
    name = "matchsoccer"
    allowed_domains = ["placardefutebol.com.br"]
    start_urls = ["https://www.placardefutebol.com.br"]


    def __init__(self, *args, **kwargs):
        super(MatchsoccerSpider, self).__init__(*args, **kwargs)
        self.job_instance = "test" #job_instance


    def error_scrapy(self, failure):
        dateTime_now = datetime.now()
        type_error = None
        error_desc = None
        code_error = match_constants.MatchConstants.HTTP_ERROR_INTERNAL_CODE

        if failure.check(HttpError):
            response = failure.value.response
            http_error = failure.check(HttpError)
            self.logger.error('HttpError on %s', response.url)
            type_error = match_constants.MatchConstants.HTTP_ERROR
            error_desc = 'HttpError on ' + response.url

        elif failure.check(DNSLookupError):
            request = failure.request
            http_error = failure.check(DNSLookupError)
            self.logger.error('DNSLookupError on %s', request.url)
            type_error = match_constants.MatchConstants.DNSLOOKUP_ERROR
            error_desc = 'DNSLookupError on  ' + request.url

        elif failure.check(TimeoutError):
            request = failure.request
            http_error = failure.check(TimeoutError)
            self.logger.error('TimeoutError on %s', request.url)
            type_error = match_constants.MatchConstants.TIMEOUT_ERROR
            error_desc = 'TimeoutError on ' + request.url

        elif failure.check(ConnectionLost):
            request = failure.request
            http_error = failure.check(ConnectionLost)
            self.logger.error('ConnectionLost on %s', request.url)
            type_error = match_constants.MatchConstants.CONNECTION_LOST
            error_desc = 'ConnectionLost on ' + request.url

        else:
            request = failure.request
            http_error = ConnectionLost
            self.logger.error('ConnectionLost on %s', request.url)
            type_error = match_constants.MatchConstants.CONNECTION_LOST
            error_desc = 'ConnectionLost on ' + request.url


        try:
            print(" ERROROR ...............", os.getenv('COLLECTION_NAME_ERROR'))
            collections = os.getenv('COLLECTION_NAME_ERROR')

            scrapyErrorService = ScrapyErrorService(collections)
            scrapyErrorModel = ScrapyResponseModel(code_error=code_error,
                                                   type_error=type_error,
                                                   error_desc=error_desc,
                                                   datetime_scrapy=dateTime_now)

            asyncio.run(scrapyErrorService.save(scrapyErrorModel))
            #loop = asyncio.get_running_loop()
            #if loop and loop.is_running():
            #    tsk = loop.create_task(scrapyErrorService.save(scrapyErrorModel))

        except Exception as e:
            print("[ERROR][error_scrapy] :: ", e)

    def start_requests(self):
        print("[scrapy]-[start_requests] ")
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.error_scrapy,
                                 dont_filter=True)

    def parse(self, response):
        print("[scrapy]-[parse] ")
        match_data = WebscrapyItem()
        for article in response.xpath('//div[@class="row align-items-center content"]'):
            match_data[WebscrapyItem.config.team_a] = article.xpath(
                './/h5[@class="text-right team_link"]//text()').extract_first()
            match_data[WebscrapyItem.config.team_b] = article.xpath(
                './/h5[@class="text-left team_link"]//text()').extract_first()
            match_data[WebscrapyItem.config.score_a] = article.xpath(
                './/div[@class="w-25 p-1 match-score d-flex justify-content-end"]//h4//span//text()').extract_first()
            match_data[WebscrapyItem.config.score_b] = article.xpath(
                './/div[@class="w-25 p-1 match-score d-flex justify-content-start"]//h4//span//text()').extract_first()
            match_data['status'] = article.xpath(
                './/div [@class="w-25 p-1 status text-center"]//span//text()').extract_first()
            yield match_data

    def closed(self, reason):
        print ('Closed Spider Now: ', reason)
        #reactor.stop()
