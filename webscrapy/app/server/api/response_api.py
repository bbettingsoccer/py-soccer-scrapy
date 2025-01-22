from pydantic import BaseModel, Field, constr, conint, create_model


class ResponseApi(BaseModel):
    response_code: conint(strict=True) = Field(...)
    status: constr(strict=True) = Field(...)
    message: constr(strict=True) = Field(...)
    data: [] = Field(...)

    def ResponseModel(data, message):
        return {
            "data": [data],
            "code": 200,
            "message": message,
        }

    def ErrorResponseModel(error, code, message):
        return {"error": error, "code": code, "message": message}