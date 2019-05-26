# -*- coding: utf-8 -*-
from enum import Enum

import grequests
import requests


class GetServiceListResult(Enum):
    SUCCESS = 0
    ERROR = 1


class GetServiceStatusResult(Enum):
    UP = 0
    NOT_UP = 1
    ERROR_ACCESS_DENIED = 2
    ERROR_NOT_FOUND = 3
    ERROR_RATELIMIT = 4
    ERROR_UNKNOWN = 5


class ServiceAPIHelper(object):
    def __init__(self, host, exception_handler=None):
        self._host = host
        self._port = 80
        self._url_path = 'api/service/v1'
        self._exception_handler = exception_handler

    @property
    def service_list_url(self):
        return 'http://{0}:{1:d}/{2}/list'.format(
            self._host,
            self._port,
            self._url_path
        )

    def get_service_list(self):
        try:
            r = requests.get(self.service_list_url)
            if r is not None and r.status_code == requests.codes.ok:
                data = r.json()
                return dict(
                    code=GetServiceListResult.SUCCESS,
                    list=data
                )
            else:
                return dict(code=GetServiceListResult.ERROR)
        except Exception:
            return dict(code=GetServiceListResult.ERROR)

    @property
    def getstatus_url_base(self):
        return 'http://{0}:{1:d}/{2}/status/'.format(
            self._host,
            self._port,
            self._url_path
        )

    def construct_getstatus_url(self, service_id):
        return self.getstatus_url_base + str(service_id)

    def _safe_create_getstatus_result(self, text):
        try:
            r = GetServiceStatusResult[text]
        except KeyError:
            r = GetServiceStatusResult.ERROR_UNKNOWN

        return r

    def getstatus(self, *service_ids):
        pending = (grequests.get(self.construct_getstatus_url(s)) for s in service_ids)
        responses = grequests.map(pending,
                                  exception_handler=self._exception_handler)
        results = list()
        possible_codes = [
            requests.codes.forbidden,
            requests.codes.not_found,
            requests.codes.too_many_requests
        ]

        for r in responses:
            if r is None:
                continue
            service_id = int(r.request.url[len(self.getstatus_url_base):])
            if r.status_code in possible_codes:
                results.append(dict(
                    service_id=service_id,
                    code=self._safe_create_getstatus_result(r.text)
                ))
            else:
                results.append(dict(
                    service_id=service_id,
                    code=GetServiceStatusResult.ERROR_UNKNOWN
                ))

        return results

    def is_up(self, service_id):
        r = self.getstatus(service_id)[0]['code'] == GetServiceStatusResult.UP
