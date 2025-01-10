from fastapi import Response
import requests
from .match_constants import MatchConstants
from ..dto.http_response_dto import HttpResponseDTO

class HttpRequestResponse:

    def handle_request(self, request_type: str, request_url: str, data: dict):
        http_response = None
        try:
            match request_type:
                case MatchConstants.GET_REQ_TYPE:
                    http_response = requests.get(request_url)
                case MatchConstants.POST_REQ_TYPE:
                    http_response = requests.post(request_url, data=data)
            return self.check_http_status_code(response=http_response)
        except Exception as e:
            return self.http_fail_response()

    @staticmethod
    def check_http_status_code(response: Response) -> HttpResponseDTO:
        httpResponse = HttpResponseDTO()
        httpResponse.response_code = response.status_code
        print("RESULTADO TEST CONECTIVIADAD ++++++++++++ ", response.status_code)
        if 200 <= response.status_code < 299:
            httpResponse.status = MatchConstants.HTTP_SUCCESS
            httpResponse.message = MatchConstants.HTTP_CLIENT_SUCCESS_200
            httpResponse.data = response.__dict__
        elif 400 <= response.status_code < 500:
            httpResponse.status = MatchConstants.HTTP_ERROR
            if response.status_code == 404:
                httpResponse.message = MatchConstants.HTTP_CLIENT_ERROR_404
            elif response.status_code == 401:
                httpResponse.message = MatchConstants.HTTP_CLIENT_ERROR_401
        elif response.status_code >= 500:
            httpResponse.status = MatchConstants.HTTP_FAIL
            httpResponse.message = MatchConstants.HTTP_CLIENT_ERROR_500
        return httpResponse

    @staticmethod
    def http_fail_response() -> HttpResponseDTO:
        httpResponse = HttpResponseDTO()
        httpResponse.message = MatchConstants.HTTP_CLIENT_ERROR_500
        httpResponse.response_code = MatchConstants.HTTP_ERROR_INTERNAL_CODE
        httpResponse.status = MatchConstants.HTTP_FAIL
        httpResponse.data = None
        return httpResponse

    @staticmethod
    def http_error_func_response() -> HttpResponseDTO:
        httpResponse = HttpResponseDTO()
        httpResponse.message = MatchConstants.HTTP_CLIENT_ERROR_422
        httpResponse.response_code = MatchConstants.HTTP_ERROR_UNPROCESSABLE_ENTITY
        httpResponse.status = MatchConstants.HTTP_ERROR
        httpResponse.data = None
        return httpResponse