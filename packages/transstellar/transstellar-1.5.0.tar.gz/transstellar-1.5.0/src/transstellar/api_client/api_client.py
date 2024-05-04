import http
import json
import logging

import requests

from .errors import ClientError, ServerError, UnauthorizedError


class APIClient:
    token = ""
    headers = {"content-type": "application/json", "accept": "application/json"}
    httpclient_logger = logging.getLogger("http.client")

    def __init__(self, base_url: str, options={}):
        self.base_url = base_url

        if options.get("debug") == True:
            global httpclient_logger

            def httpclient_log(*args):
                self.httpclient_logger.log(logging.DEBUG, " ".join(args))

            # mask the print() built-in in the http.client module to use
            # logging instead
            http.client.print = httpclient_log
            # enable debugging
            http.client.HTTPConnection.debuglevel = 1

    def __get_headers(self, headers):
        return {**self.headers, **headers, "Authorization": f"Bearer {self.token}"}

    def __handle_response(
        self, response: requests.models.Response, expected_successful_status_code=200
    ):
        status_code = response.status_code
        responseJson = None

        if response.text:
            responseJson = json.loads(response.text)

        if status_code >= 200 and status_code < 300:
            if status_code != expected_successful_status_code:
                raise Exception(
                    f"Response status code ({status_code}) is not as expected: {expected_successful_status_code}"
                )
            return responseJson

        if status_code >= 400 and status_code < 500:
            error_message = responseJson.get("message", "Unknown client error")

            if status_code == 400:
                raise ClientError(f"Client error: {error_message}")

            elif status_code == 401:
                raise UnauthorizedError("Unauthorized: Check your credentials")

            else:
                error_message = responseJson.get("message", "Unknown client error")
                raise ClientError(f"Client error: HTTP {status_code}. {error_message}")

        if status_code >= 500:
            error_message = responseJson.get("message", "Internal Server Error")
            raise ServerError(f"Server error: HTTP {status_code}. {error_message}")

    def __get(self, url, params, headers={}):
        headers = self.__get_headers(headers)
        response = requests.get(url, params=params, headers=headers)

        return self.__handle_response(response)

    def __post(self, url, payload, headers={}, expected_successful_status_code=200):
        headers = self.__get_headers(headers)
        response = requests.post(url, json=payload, headers=headers)

        return self.__handle_response(response, expected_successful_status_code)

    def __delete(self, url, headers={}):
        headers = self.__get_headers(headers)
        response = requests.delete(url, headers=headers)

        return self.__handle_response(response, expected_successful_status_code=204)

    def as_token(self, token):
        self.token = token

        return self
