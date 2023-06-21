from typing import Any
from warnings import warn

from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse


class HttpRequest(IRequest):
    body: dict
    headers: dict
    query_params: dict

    data: dict

    def __init__(self, body: dict = {}, headers: dict = {}, query_params: dict = {}):
        self.body = body or {}
        self.headers = headers or {}
        self.query_params = query_params or {}
        data_dict = {}

        # check overlapping keys
        if type(body) is dict:
            data_dict.update(body)
            if [key for key in self.body.keys() if key in self.query_params.keys()] or [key for key in self.body.keys()
                                                                                        if key in self.headers.keys()]:
                warn(
                    f"body, query_params and/or headers have overlapping keys → {[key for key in self.body.keys() if key in self.query_params.keys()] or [key for key in self.body.keys() if key in self.headers.keys()]}")
        else:
            if [key for key in self.query_params.keys() if key in self.headers.keys()]:
                warn(
                    f"query_params and headers have overlapping keys → {[key for key in self.query_params.keys() if key in self.headers.keys()]}")

        if type(body) is str:
            data_dict.update({"body": body})

        data_dict.update(self.headers)
        data_dict.update(self.query_params)
        self.data = data_dict

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, value: dict):
        self._data = value

    def __repr__(self):
        return (
            f"HttpRequest (body={self.body}, headers={self.headers}, query_params={self.query_params}, data={self.data})"
        )


class HttpResponse(IResponse):
    status_code: int
    body: dict
    headers: dict

    data: dict

    def __init__(self, status_code: int, body: dict = {}, headers: dict = {}, data: dict = {}):
        self.status_code = status_code
        self.body = body or data
        self.headers = headers

        data_dict = {}
        if type(body) is dict:
            data_dict.update(body)
        if type(body) is str:
            data_dict.update({"body": body})

        data_dict.update(headers)
        self.data = data_dict

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, value: dict):
        self._data = value

    @property
    def status_code(self) -> dict:
        return self._status_code

    @status_code.setter
    def status_code(self, value: dict):
        self._status_code = value

    def __repr__(self):
        return (
            f"HttpResponse (status_code={self.status_code}, body={self.body}, headers={self.headers})"
        )


if __name__ == '__main__':
    # test
    body = {"body": "body"}
    headers = {"headers": "headers", "body": "body"}
    query_params = {"query_params": "query_params"}
    data = {"data": "data"}
    request = HttpRequest(body, headers, query_params)
    response = HttpResponse(200, body, headers)
    print(request)
    print(response)