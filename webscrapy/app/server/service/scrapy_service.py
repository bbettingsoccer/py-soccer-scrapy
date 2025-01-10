import os
from crochet import setup
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from sqlalchemy.util import await_only
from twisted.internet import reactor
from ..common.http_request_response import HttpRequestResponse
from ..dao.operationimpl_dao import OperationImplDAO
from ..dto.http_response_dto import HttpResponseDTO
from ..common.match_constants import MatchConstants
from scrapy.utils.log import configure_logging
import time
import asyncio

class ScrapyService:

    def __init__(self, championship, job_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setup()
        os.environ['COLLECTION_NAME'] = championship + MatchConstants.DOMAIN_SCRAPY_CHAMPIONSHIP
        os.environ['COLLECTION_NAME_ERROR'] = championship + MatchConstants.DOMAIN_SCRAPY_ERROR + job_instance


    async def scrapy_process(self, crawl: str) -> HttpResponseDTO:
       httpRequest = HttpRequestResponse()
       response = self.check_connection_spider()
       match response.status:
            case MatchConstants.HTTP_SUCCESS:
                scrapy_status = self.scrapy_runtime(crawl)
                time.sleep(7)
                if scrapy_status == MatchConstants.SCRAPY_SUCCESS:
                    collection = OperationImplDAO(os.environ['COLLECTION_NAME'])
                    collection_count = await collection.count_document()
                    if collection_count == 0:
                        httpRequestError = httpRequest.http_fail_response()
                        httpRequestError.data = 0
                        return httpRequestError
                    elif collection_count > 0:
                        response.data = collection_count
                        return response
                else:
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