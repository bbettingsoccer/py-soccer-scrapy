import os

import asyncio
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.signalmanager import SignalManager
from scrapy.utils.project import get_project_settings
#from scrapy.utils.reactor import install_reactor

from .scrapy_error_service import ScrapyErrorService
from ..common.http_request_response import HttpRequestResponse
from ..dto.http_response_dto import HttpResponseDTO
from ....spiders.matchsoccer_spider import MatchsoccerSpider
from ..common.match_constants import MatchConstants
from scrapy.utils.log import configure_logging
from scrapy import signals
from twisted.internet import reactor, defer
from scrapy import cmdline
import threading
class SoccerScrapyService_teste:

    """
    runner = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings_file_path = 'webscrapy.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        crawler_settings = get_project_settings()
        self.runner = CrawlerProcess(crawler_settings)
    """


    def scrapy_runtime(self, crawl: str, championship: str, job_instance: str, date_match: str) -> HttpResponseDTO:
        os.environ['COLLECTION_NAME'] = championship + MatchConstants.DOMAIN_SCRAPY_CHAMPIONSHIP
        collection_error = championship + MatchConstants.DOMAIN_SCRAPY_ERROR + job_instance
        os.environ['COLLECTION_NAME_ERROR'] = collection_error
        http_dto = HttpResponseDTO()
        try:
            print("[INVOKE]-[SoccerScrapyService][scrapy_runtime] :: ")

            http_dto.response_code = 200

            # DROP COLLECTION TYPE _ERROR
            self.instance_spider_pr("matchsoccer")
            print("[RETURN ]-[instance_spider_pr][scrapy_runtime] :: ")

            return http_dto
        except Exception as e:
            print("[ERROR]-[SoccerScrapyService][scrapy_runtime] :: ", e)
            http_dto.response_code = 500
            return http_dto

    def instance_spider_pr(self,spider_name):
        print("[INVOKE]-[SoccerScrapyService][instance_spider_pr] :: ")

        """
        runner = CrawlerRunner(get_project_settings())
        deferred = runner.crawl(spider_name)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        """



        #command = f"scrapy crawl {spider_name} -a job_instance={job_instance}"
        #command = f"scrapy crawl {spider_name}"
        #cmdline.execute(command.split())

        signal_manager = SignalManager()
        signal_manager.connect(self.spider_closed, signal=signals.spider_closed)
        settings_file_path = 'webscrapy.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        crawler_settings = get_project_settings()

        print("[INVOKE]-[SoccerScrapyService][process.start = END] :: ")

    def spider_closed(spider, reason):
        # Your code here to handle the spider closure
        print(f'Spider caralho +++++++: {reason}')
        reactor.stop()  # This will stop the reactor and unblock your program

