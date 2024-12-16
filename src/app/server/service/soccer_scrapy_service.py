import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.webscrapy.spiders.matchsoccer_spider import MatchsoccerSpider
from ..common.match_constants import MatchConstants
from ..service.scrapy_error_service import ScrapyErrorService


class SoccerScrapyService:

    async def scrapy_runtime(self, crawl: str, championship: str, job_instance: str):
        os.environ['COLLECTION_NAME'] = championship+MatchConstants.DOMAIN_SCRAPY_CHAMPIONSHIP
        collection_error = championship+MatchConstants.DOMAIN_SCRAPY_ERROR+job_instance
        os.environ['COLLECTION_NAME_ERROR'] = collection_error
        scrap_error_service = ScrapyErrorService(collection_error)
        response_http = None
        try:
            # DROP COLLECTION TYPE _ERROR
            await scrap_error_service.dropCollection()

            # CALL METHOD TO INSTANCE SPIDER
            self.instance_Spider(crawl, job_instance)

            collections = await scrap_error_service.getErrorByCollection()

            if collections is None:
                response_http = MatchConstants.HTTP_SUCCESS_STATUS
            elif collections is not None:
                collection = collections[0]
                response_http = collection["code_error"]
            return response_http
        except Exception as e:
            print("[ERROR]-[SoccerScrapyService][scrapy_runtime] :: ", e)

    @staticmethod
    def instance_Spider(crawl: str, job_instance: str):
        try:
            settings_file_path = 'src.webscrapy.settings'  # The path seen from root, ie. from main.py
            os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
            crawler_settings = get_project_settings()
            process = CrawlerProcess(settings=crawler_settings)
            match crawl:
                case MatchConstants.MATCH_SOCCER_SPIDER:
                    process.crawl(MatchsoccerSpider, job_instance=job_instance)
            process.start(stop_after_crawl=False)
        except Exception as e:
            print("[ERROR]-[SoccerScrapyService][instance_Spider] :: ", e)
