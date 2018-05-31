# -*- coding: utf-8 -*-
from enum import Enum
import grequests
import requests
import dateutil.parser


class SubmitResult(Enum):
    SUCCESS = 0  # submitted flag has been accepted
    ERROR_UNKNOWN = 1  # generic error
    ERROR_ACCESS_DENIED = 2  # the attacker does not appear to be a team
    ERROR_COMPETITION_NOT_STARTED = 3  # contest has not been started yet
    ERROR_COMPETITION_PAUSED = 4  # contest has been paused
    ERROR_COMPETITION_FINISHED = 5  # contest has been completed
    ERROR_FLAG_INVALID = 6  # submitted data has invalid format
    ERROR_RATELIMIT = 7  # attack attempts limit exceeded
    ERROR_FLAG_EXPIRED = 8  # submitted flag has expired
    ERROR_FLAG_YOUR_OWN = 9  # submitted flag belongs to the attacking team
    ERROR_FLAG_SUBMITTED = 10  # submitted flag has been accepted already
    ERROR_FLAG_NOT_FOUND = 11  # submitted flag has not been found
    ERROR_SERVICE_STATE_INVALID = 12  # the attacking team service is not up


class GetinfoResult(Enum):
    SUCCESS = 0  # submitted flag has been accepted
    ERROR_UNKNOWN = 1  # generic error
    ERROR_ACCESS_DENIED = 2  # getinfo calls are allowed from a team's subnet
    ERROR_NOT_FOUND = 3  # flag is invalid
    ERROR_RATELIMIT = 4  # rate limit exceeded


class FlagAPIHelper(object):
    def __init__(self, host):
        self._host = host
        self._port = 80
        self._url_path = 'api/flag/v1'

    @property
    def submit_url(self):
        return 'http://{0}:{1:d}/{2}/submit'.format(
            self._host,
            self._port,
            self._url_path
        )

    def _safe_create_result(self, text):
        try:
            r = SubmitResult[text]
        except KeyError:
            r = SubmitResult.ERROR_UNKNOWN

        return r

    def submit(self, *flags):
        u = self.submit_url
        h = {'Content-Type': 'text/plain'}
        pending = (grequests.post(u, data=f, headers=h) for f in flags)
        responses = grequests.map(pending)
        results = list()
        for r in responses:
            flag = r.request.body
            possible_codes = [
                requests.codes.ok,
                requests.codes.bad_request,
                requests.codes.forbidden
            ]
            print(r.text)
            if r.status_code in possible_codes:
                results.append(dict(
                    flag=flag,
                    code=self._safe_create_result(r.text)
                ))
            elif r.status_code == requests.codes.too_many_requests:
                results.append(dict(
                    flag=flag,
                    code=SubmitResult.ERROR_RATELIMIT
                ))
            else:
                results.append(dict(
                    flag=flag,
                    code=SubmitResult.ERROR_UNKNOWN
                ))

        return results

    @property
    def getinfo_url_base(self):
        return 'http://{0}:{1:d}/{2}/info/'.format(
            self._host,
            self._port,
            self._url_path
        )

    def construct_getinfo_url(self, flag):
        return self.getinfo_url_base + flag

    def getinfo(self, *flags):
        pending = (grequests.get(self.construct_getinfo_url(f)) for f in flags)
        responses = grequests.map(pending)
        results = list()
        for r in responses:
            flag = r.request.url[len(self.getinfo_url_base):]
            if r.status_code == requests.codes.ok:
                data = r.json()
                results.append(dict(
                    flag=flag,
                    code=GetinfoResult.SUCCESS,
                    team=data['team'],
                    service=data['service'],
                    round=data['round'],
                    nbf=dateutil.parser.parse(data['nbf']),
                    exp=dateutil.parser.parse(data['exp'])
                ))
            elif r.status_code == requests.codes.forbidden:
                results.append(dict(
                    flag=flag,
                    code=GetinfoResult.ERROR_ACCESS_DENIED
                ))
            elif r.status_code == requests.codes.not_found:
                results.append(dict(
                    flag=flag,
                    code=GetinfoResult.ERROR_NOT_FOUND
                ))
            elif r.status_code == requests.codes.too_many_requests:
                results.append(dict(
                    flag=flag,
                    code=GetinfoResult.ERROR_RATELIMIT
                ))
            else:
                results.append(dict(
                    flag=flag,
                    code=GetinfoResult.ERROR_UNKNOWN
                ))

        return results
