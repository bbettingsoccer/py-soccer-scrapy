from pydantic import BaseModel, Field, constr, conint, create_model

from typing import List

class RequestApi(BaseModel):
    crawl: constr(strict=True) = Field(...)
    championship: constr(strict=True) = Field(...)
    job_instance: constr(strict=True) = Field(...)

    def ResponseModel(data, message):
        return {
            "data": [data],
            "code": 200,
            "message": message,
        }

    def ErrorResponseModel(error, code, message):
        return {"error": error, "code": code, "message": message}