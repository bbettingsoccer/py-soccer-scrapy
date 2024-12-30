from fastapi import APIRouter

from ..common.http_request_response import HttpRequestResponse
from ..model.scrapy_error_model import ScrapyErrorModel
from ..service.scrapy_error_service import ScrapyErrorService
from ..service.soccer_scrapy_service import SoccerScrapyService
from ..common.match_constants import MatchConstants

router = APIRouter()


@router.get("/runtime/{crawl}/championship/{championship}/job/{job_instance}/date_match/{date_match}", response_description="Match retrieved")
async def runtime_scrapy(crawl: str, championship: str, job_instance: str, date_match: str):
    service = SoccerScrapyService()
    http_util = HttpRequestResponse()
    try:
        response_code = await service.scrapy_runtime(crawl, championship, job_instance, date_match)
        response_http = http_util.check_http_status_code(response_code)
        return response_http
    except Exception as e:
        response_http = http_util.check_http_status_code(MatchConstants.HTTP_ERROR_INTERNAL_CODE)
        return response_http


@router.get("/error/championship/{championship}/job/{job_instance}", response_description="Match retrieved")
async def getErrorByChampionshipAndJob(championship: str, job_instance: str):
    try:
        collection_name_error = championship+MatchConstants.DOMAIN_SCRAPY_ERROR+job_instance
        service = ScrapyErrorService(collection_name_error)
        collections = await service.getErrorByCollection()
        if collections:
            return ScrapyErrorModel.ResponseModel(collections, "Data retrieved successfully")
        return ScrapyErrorModel.ErrorResponseModel("Error", 400, "Collection Not Found")
    except Exception as e:
        return ScrapyErrorModel.ErrorResponseModel("An error occurred.", 500, "Internal Server Error")


@router.get("/error/collection/{collection}", response_description="Match retrieved")
async def getErrorByCollection(collection: str):
    try:
        service = ScrapyErrorService(collection)
        collections = await service.getErrorByCollection()
        if collections:
            return ScrapyErrorModel.ResponseModel(collections, "Data retrieved successfully")
        return ScrapyErrorModel.ErrorResponseModel("Error", 400, "Collection Not Found")
    except Exception as e:
        return ScrapyErrorModel.ErrorResponseModel("An error occurred.", 500, "Internal Server Error")


@router.get("/error/all", response_description="Match retrieved")
async def getAllCollection():
    try:
        service = ScrapyErrorService(None)
        collections = await service.getCollectionName()
        if collections:
            return ScrapyErrorModel.ResponseModel(collections, "Data retrieved successfully")
        return ScrapyErrorModel.ErrorResponseModel("Error", 400, "Collection Not Found")
    except Exception as e:
        return ScrapyErrorModel.ErrorResponseModel("An error occurred.", 500, "Internal Server Error")


@router.delete("/error/drop/{collection}", response_description="Drop Collection")
async def drop_collection(collection: str):
    try:
        service = ScrapyErrorService(collection)
        result_req = await service.dropCollection()
        if result_req:
            return ScrapyErrorModel.ResponseModel("Drop Collection Success".format(id), "Success")
        return ScrapyErrorModel.ErrorResponseModel("Error", 400, "Collection Not Found")
    except Exception as e:
        print("Error ", e)
        return ScrapyErrorModel.ErrorResponseModel("Error", 500, " Internal Server Error")
