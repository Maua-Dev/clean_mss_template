from typing import Any

from src.shared.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse


class HttpRequest(IRequest):
    body: dict
    headers: dict
    query_params: dict

    data: dict

    def __init__(self, body: dict = {}, headers: dict = {}, query_params: dict = {}):
        self.body = body
        self.headers = headers
        self.query_params = query_params

        data_dict = {}
        data_dict.update(body)
        data_dict.update(headers)
        data_dict.update(query_params)
        self.data = data_dict

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, value: dict):
        self._data = value

    def __repr__(self):
        return (
            f"HttpRequest (body={self.body}, headers={self.headers}, query_params={self.query_params})"
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
        data_dict.update(body)
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
        return self._data

    @status_code.setter
    def status_code(self, value: dict):
        self._status_code = value

    def __repr__(self):
        return (
            f"HttpResponse (status_code={self.status_code}, body={self.body}, headers={self.headers})"
        )


if __name__ == '__main__':
    ht = HttpRequest(body={'a': 1}, query_params={'c': 3})
