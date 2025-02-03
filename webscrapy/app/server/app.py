import os

from fastapi import FastAPI, Response, Body

from .api.request_api import RequestApi
from .common.enviroment_conf import env_check
from .common.http_request_response import HttpRequestResponse
from .model.scrapy_response_model import ScrapyResponseModel
from .service.scrapy_error_service import ScrapyErrorService
from .service.scrapy_service import ScrapyService
from .common.match_constants import MatchConstants

app = FastAPI()
env_check()

@app.get("/")
def read_root(response: Response):
    return {"message": "Welcome to this SheduleMatch domain !"}


@app.post(path="/scrapy/runtime")
async def runtime_scrapy(data: RequestApi = Body(...)):
    http_util = HttpRequestResponse()
    try:
        print("[A]-[SoccerScrapyService][runtime_scrapy] :: ")
        service = ScrapyService(championship=data.championship, job_instance=data.job_instance)
        print("[B]-[SoccerScrapyService][runtime_scrapy] :: ")
        http_response = await service.scrapy_process(crawl=data.crawl)
        print("[C]-[SoccerScrapyService][runtime_scrapy] :: ")
        return http_response
    except Exception as e:
        response_error = http_util.http_fail_response()
        print("Exception Exception Exception Exception Exception Exception ", response_error.response_code)
        return ScrapyResponseModel.ErrorResponseModel("Server Error", response_error.response_code, response_error.message)


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
