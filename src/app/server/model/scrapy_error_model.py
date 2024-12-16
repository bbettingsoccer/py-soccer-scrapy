from pydantic import BaseModel, Field, constr, conint, create_model
from _datetime import datetime


class ScrapyErrorModel(BaseModel):
    code_error: conint(strict=True) = Field(...)
    type_error: constr(strict=True) = Field(...)
    error_desc: constr(strict=True) = Field(...)
    datetime_scrapy: datetime = None


    class config:
        code_error = "code_error"
        type_error = "type_error"
        error_desc = "error"
        datetime_scrapy = "datetime_scrapy"

    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        OptionalModel = create_model(
            f"Optional{cls.__name__}",
            __base__=ScrapyErrorModel,
            **{
                k: (v.annotation, None) for k, v in ScrapyErrorModel.model_fields.items()
            })
        return OptionalModel

    def ResponseModel(data, message):
        return {
            "data": [data],
            "code": 200,
            "message": message,
        }



    def ErrorResponseModel(error, code, message):
        return {"error": error, "code": code, "message": message}

    @staticmethod
    def data_helper(data) -> dict:
        return {
            "_id": str(data['_id']),
            "code_error": str(data["code_error"]),
            "type_error": str(data["type_error"]),
            "error_desc": str(data["error_desc"]),
            "datetime_scrapy": str(data["datetime_scrapy"])
        }
