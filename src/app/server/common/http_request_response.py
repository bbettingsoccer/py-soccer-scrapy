from fastapi import Response

from .match_constants import MatchConstants


class HttpRequestResponse:

    @staticmethod
    def handle_response(status_code: int, body: str):
        response = Response()
        try:
            response.status_code = status_code
            response.headers["Content-Type"] = "application/json"
            # response.body = body
            return response
        except Exception as e:
            print("[ERROR][handle_response] -- ", e)

    def check_http_status_code(self, status_code: int):
        http_msg = None
        request_status = False
        if 200 <= status_code < 299:
            http_msg = MatchConstants.HTTP_CLIENT_SUCCESS_200
        elif 400 <= status_code < 500:
            if status_code == 404:
                http_msg = MatchConstants.HTTP_CLIENT_ERROR_404
            elif status_code == 401:
                http_msg = MatchConstants.HTTP_CLIENT_ERROR_401
        elif status_code >= 500:
            http_msg = MatchConstants.HTTP_CLIENT_ERROR_500

        response_http = self.handle_response(status_code, http_msg)
        return response_http
