import json
import os
import requests

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.webscrapy.spiders.matchsoccer_spider import MatchsoccerSpider
from ..common.enviroment_conf import get_path_file
from ..common.match_constants import MatchConstants
from ..service.scrapy_error_service import ScrapyErrorService


class SoccerScrapyService:

    async def scrapy_runtime(self, crawl: str, championship: str, job_instance: str, date_match: str):
        os.environ['COLLECTION_NAME'] = championship+MatchConstants.DOMAIN_SCRAPY_CHAMPIONSHIP
        collection_error = championship+MatchConstants.DOMAIN_SCRAPY_ERROR+job_instance
        os.environ['COLLECTION_NAME_ERROR'] = collection_error
        scrap_error_service = ScrapyErrorService(collection_error)
        response_http = None
        try:
            # DROP COLLECTION TYPE _ERROR
            await scrap_error_service.dropCollection()

            # CALL METHOD TO INSTANCE SPIDER
            self.instance_spider(crawl, job_instance)

            collections_error = await scrap_error_service.getErrorByCollection()

            if collections_error is None:
                response_http = MatchConstants.HTTP_SUCCESS_STATUS
                # CALL PROCESS_BATCH_ETL - SPARK - instance_batch_etl
                self.instance_batch_etl(date_match, championship)
            elif collections_error is not None:
                error = collections_error[0]
                response_http = error["code_error"]
            return response_http
        except Exception as e:
            print("[ERROR]-[SoccerScrapyService][scrapy_runtime] :: ", e)

    @staticmethod
    def instance_spider(crawl: str, job_instance: str):
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

    @staticmethod
    def instance_batch_etl(date_match: str, championship: str):
        path_file = get_path_file(folder1="env", folder2="ApiSpark_Invoke", file="post_body_matchresult_etl.json")
        try:
            spark_url = os.getenv('API_SOCCER_ETL')
            with open(path_file, 'r') as f:
                body = json.load(f)
                appArgs = body['appArgs']
                appArgs[3] = date_match
                appArgs[4] = championship
                body['appArgs'] = appArgs
                print("body body_matchresult ", body)
            response = requests.post(spark_url, json=body)
            print("REQUEST",response.text)
        except Exception as e:
            print("[ERROR]-[SoccerScrapyService][instance_batch_etl] :: ", e)
