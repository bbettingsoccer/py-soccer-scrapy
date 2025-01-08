import os
from crochet import setup
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from ..common.http_request_response import HttpRequestResponse
from ..dto.http_response_dto import HttpResponseDTO
from ....spiders.matchsoccer_spider import MatchsoccerSpider
from ..common.match_constants import MatchConstants
from scrapy.utils.log import configure_logging
import time

class ScrapyService:

    def __init__(self, championship, job_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setup()
        os.environ['COLLECTION_NAME'] = championship + MatchConstants.DOMAIN_SCRAPY_CHAMPIONSHIP
        os.environ['COLLECTION_NAME_ERROR'] = championship + MatchConstants.DOMAIN_SCRAPY_ERROR + job_instance

    def scrapy_process(self, crawl: str) -> HttpResponseDTO:
       httpRequest = HttpRequestResponse()
       response = self.check_connection_spider()
       match response.status:
            case MatchConstants.HTTP_SUCCESS:
                scrapy_status = self.scrapy_runtime(crawl)
                time.sleep(7)
                if scrapy_status == MatchConstants.SCRAPY_SUCCESS:
                    print(">>>>>>>>>>>>>>>>>>< RETUN SUCCESS >>>>>>>>>>>>>>>")
                    return response
                else:
                    print(">>>>>>>>>>>>>>>>>>< RETUN ERROR >>>>>>>>>>>>>>>")
                    return httpRequest.http_fail_response()
            case MatchConstants.HTTP_ERROR | MatchConstants.HTTP_FAIL:
               return httpRequest.http_fail_response()

    @staticmethod
    def check_connection_spider():
        httpRequest = HttpRequestResponse()
        url_test = os.getenv("SCRAPY_TEST_URL")
        return httpRequest.handle_request(request_type=MatchConstants.GET_REQ_TYPE, request_url=url_test,
                                      data=None)


    def scrapy_runtime(self, crawl: str) -> str:
        configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
        try:
            self.crawl_spider(crawl)
        except RuntimeError as e:
            if reactor.running:
                print("Reactor is already running")
                return MatchConstants.SCRAPY_SUCCESS
            else:
                print("[ERROR]-[SoccerScrapyService][scrapy_runtime] :: ", e)
                return MatchConstants.SCRAPY_FAIL

    def crawl_spider(self,spider_name):
        print("[INVOKE]-[SoccerScrapyService][instance_spider_pr] :: ")
        runner = CrawlerRunner(get_project_settings())
        deferred = runner.crawl(spider_name)
        #deferred.addBoth(lambda _: reactor.stop())
        reactor.run()