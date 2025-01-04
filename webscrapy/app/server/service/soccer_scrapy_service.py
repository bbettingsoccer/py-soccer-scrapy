import os
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor
from ..common.http_request_response import HttpRequestResponse
from ..dto.http_response_dto import HttpResponseDTO
from ....spiders.matchsoccer_spider import MatchsoccerSpider
from ..common.match_constants import MatchConstants
from ..service.scrapy_error_service import ScrapyErrorService
from scrapy.utils.log import configure_logging
import nest_asyncio
import threading

install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
nest_asyncio.apply()


class SoccerScrapyService:

    def scrapy_runtime(self, crawl: str, championship: str, job_instance: str, date_match: str) -> HttpResponseDTO:
        os.environ['COLLECTION_NAME'] = championship + MatchConstants.DOMAIN_SCRAPY_CHAMPIONSHIP
        collection_error = championship + MatchConstants.DOMAIN_SCRAPY_ERROR + job_instance
        os.environ['COLLECTION_NAME_ERROR'] = collection_error
        scrap_error_service = ScrapyErrorService(collection_error)
        configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
        http_dto = HttpResponseDTO()
        try:

            http_dto.response_code = 200

            # DROP COLLECTION TYPE _ERROR
            scrap_error_service.dropCollection()
            # DROP COLLECTION TYPE _ERROR
            threading.Thread(target=self.instance_spider_pr, args=(job_instance,)).start()

            return http_dto
        except Exception as e:
            print("[ERROR]-[SoccerScrapyService][scrapy_runtime] :: ", e)
            http_dto.response_code = 200
            return http_dto


    def instance_spider_pr(self, job_instance: str):
        settings_file_path = 'webscrapy.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        crawler_settings = get_project_settings()
        process = CrawlerProcess(crawler_settings)
        process.crawl(MatchsoccerSpider, job_instance=job_instance)
        process.start(stop_after_crawl=False)

    def check_connection_spider(self):
        httpRequest = HttpRequestResponse()
        url_test = os.getenv("SCRAPY_TEST_URL")
        return httpRequest.handle_request(request_type=MatchConstants.GET_REQ_TYPE, request_url=url_test,
                                      data=None)

