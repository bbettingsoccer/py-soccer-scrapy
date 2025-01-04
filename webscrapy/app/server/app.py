from fastapi import FastAPI, Response
from .common.http_request_response import HttpRequestResponse
from .model.scrapy_response_model import ScrapyResponseModel
from .service.scrapy_error_service import ScrapyErrorService
from .service.soccer_scrapy_service import SoccerScrapyService
from .common.match_constants import MatchConstants

app = FastAPI()


@app.get("/")
def read_root(response: Response):
    return {"message": "Welcome to this SheduleMatch domain !"}


@app.get("/scrapy/runtime/{crawl}/championship/{championship}/job/{job_instance}/date_match/{date_match}")
async def runtime_scrapy(crawl: str, championship: str, job_instance: str, date_match: str, response: Response):
    service = SoccerScrapyService()
    http_util = HttpRequestResponse()
    try:
        # CALL METHOD TEST CONNECTION - SCRAPY
        response_code = service.check_connection_spider()
        # CHECK STATUS TEST CONNECTION FOR INVOKE - SCRAPY/SPIDER
        match response_code.status:
            case MatchConstants.HTTP_SUCCESS:
                service.scrapy_runtime(crawl, championship, job_instance, date_match)
                return ScrapyResponseModel.ResponseModel(response_code.response_code, "Data retrieved successfully")

        if response_code.status is not MatchConstants.HTTP_SUCCESS:
            return ScrapyResponseModel.ErrorResponseModel("Server Error", response_code.response_code, response_code.message)
    except Exception as e:
        response_http = http_util.http_fail_response()
        print("Exception Exception Exception Exception Exception Exception ", response_http.response_code)
        return ScrapyResponseModel.ErrorResponseModel("Server Error", response_http.response_code, response_http.message)


@app.get("/error/championship/{championship}/job/{job_instance}", response_description="Match retrieved")
async def getErrorByChampionshipAndJob(championship: str, job_instance: str):
    try:
        collection_name_error = championship + MatchConstants.DOMAIN_SCRAPY_ERROR + job_instance
        service = ScrapyErrorService(collection_name_error)
        collections = await service.getErrorByCollection()
        if collections:
            return ScrapyResponseModel.ResponseModel(collections, "Data retrieved successfully")
        return ScrapyResponseModel.ErrorResponseModel("Error", 400, "Collection Not Found")
    except Exception as e:
        return ScrapyResponseModel.ErrorResponseModel("An error occurred.", 500, "Internal Server Error")


@app.get("/error/collection/{collection}", response_description="Match retrieved")
async def getErrorByCollection(collection: str):
    try:
        service = ScrapyErrorService(collection)
        collections = await service.getErrorByCollection()
        if collections:
            return ScrapyResponseModel.ResponseModel(collections, "Data retrieved successfully")
        return ScrapyResponseModel.ErrorResponseModel("Error", 400, "Collection Not Found")
    except Exception as e:
        return ScrapyResponseModel.ErrorResponseModel("An error occurred.", 500, "Internal Server Error")


@app.get("/error/all", response_description="Match retrieved")
async def getAllCollection():
    try:
        service = ScrapyErrorService(None)
        collections = await service.getCollectionName()
        if collections:
            return ScrapyResponseModel.ResponseModel(collections, "Data retrieved successfully")
        return ScrapyResponseModel.ErrorResponseModel("Error", 400, "Collection Not Found")
    except Exception as e:
        return ScrapyResponseModel.ErrorResponseModel("An error occurred.", 500, "Internal Server Error")


@app.delete("/error/drop/{collection}", response_description="Drop Collection")
async def drop_collection(collection: str):
    try:
        service = ScrapyErrorService(collection)
        result_req = await service.dropCollection()
        if result_req:
            return ScrapyResponseModel.ResponseModel("Drop Collection Success".format(id), "Success")
        return ScrapyResponseModel.ErrorResponseModel("Error", 400, "Collection Not Found")
    except Exception as e:
        print("Error ", e)
        return ScrapyResponseModel.ErrorResponseModel("Error", 500, " Internal Server Error")
