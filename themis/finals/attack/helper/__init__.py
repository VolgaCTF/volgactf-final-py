# -*- coding: utf-8 -*-
from enum import Enum
import os

import click
import grequests
import requests
import dateutil.parser


class SubmitResult(Enum):
    SUCCESS_FLAG_ACCEPTED = 0  # submitted flag has been accepted
    ERR_GENERIC = 1  # generic error
    ERR_INVALID_IDENTITY = 2  # the attacker does not appear to be a team
    ERR_CONTEST_NOT_STARTED = 3  # contest has not been started yet
    ERR_CONTEST_PAUSED = 4  # contest has been paused
    ERR_CONTEST_COMPLETED = 5  # contest has been completed
    ERR_INVALID_FORMAT = 6  # submitted data has invalid format
    ERR_ATTEMPTS_LIMIT = 7  # attack attempts limit exceeded
    ERR_FLAG_EXPIRED = 8  # submitted flag has expired
    ERR_FLAG_YOURS = 9  # submitted flag belongs to the attacking team
    ERR_FLAG_SUBMITTED = 10  # submitted flag has been accepted already
    ERR_FLAG_NOT_FOUND = 11  # submitted flag has not been found
    ERR_SERVICE_NOT_UP = 12  # the attacking team service is not up


class GetinfoResult(Enum):
    SUCCESS = 0  # submitted flag has been accepted
    ERROR_UNKNOWN = 1  # generic error
    ERROR_ACCESS_DENIED = 2  # getinfo calls are allowed from a team's subnet
    ERROR_NOT_FOUND = 3  # flag is invalid
    ERROR_RATELIMIT = 4  # rate limit exceeded


default_endpoint_port = 80
default_endpoint_url_path = 'api/flag/v1'


class Helper(object):
    def __init__(self, host, port=default_endpoint_port,
                 url_path=default_endpoint_url_path):
        self._host = host
        self._port = port
        self._url_path = url_path

    @property
    def submit_url(self):
        return 'http://{0}:{1}/{2}/submit'.format(
            self._host,
            self._port,
            self._url_path
        )

    def _safe_create_result(self, text):
        try:
            r = SubmitResult[text]
        except KeyError:
            r = SubmitResult.ERR_GENERIC

        return r

    def submit(self, *flags):
        u = self.submit_url
        h = {'Content-Type': 'text/plain'}
        pending = (grequests.post(u, data=f, headers=h) for f in flags)
        responses = grequests.map(pending)
        results = list()
        for r in responses:
            flag = r.request.body
            if r.status_code == requests.codes.ok:
                results.append(dict(
                    flag=flag,
                    code=self._safe_create_result(r.text)
                ))
            elif r.status_code == requests.codes.bad_request:
                results.append(dict(
                    flag=flag,
                    code=self._safe_create_result(r.text)
                ))
            elif r.status_code == requests.codes.forbidden:
                results.append(dict(
                    flag=flag,
                    code=SubmitResult.ERR_INVALID_IDENTITY
                ))
            elif r.status_code == requests.codes.too_many_requests:
                results.append(dict(
                    flag=flag,
                    code=SubmitResult.ERR_ATTEMPTS_LIMIT
                ))
            else:
                results.append(dict(
                    flag=flag,
                    code=SubmitResult.ERR_GENERIC
                ))

        return results

    @property
    def getinfo_url_base(self):
        return 'http://{0}:{1}/{2}/info/'.format(
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


def create_helper():
    host = os.getenv('THEMIS_FINALS_ENDPOINT_HOST')
    port = int(os.getenv('THEMIS_FINALS_ENDPOINT_PORT',
                         '{0:d}'.format(default_endpoint_port)))
    url_path = os.getenv('THEMIS_FINALS_ENDPOINT_URL_PATH',
                         default_endpoint_url_path)
    return Helper(host, port, url_path)


@click.group()
def cli():
    pass


def print_submit_results(results):
    for r in results:
        flag_part = click.style(r['flag'], bold=True)
        status_part = None
        if r['code'] == SubmitResult.SUCCESS_FLAG_ACCEPTED:
            status_part = click.style(r['code'].name, fg='green')
        else:
            status_part = click.style(r['code'].name, fg='red')
        click.echo(flag_part + '  ' + status_part)


@cli.command()
@click.argument('flags', nargs=-1)
def submit(flags):
    helper = create_helper()
    results = helper.submit(*flags)
    print_submit_results(results)


def print_getinfo_results(results):
    for r in results:
        flag_part = click.style(r['flag'], bold=True)
        status_part = None
        extra_part = ''
        if r['code'] == GetinfoResult.SUCCESS:
            status_part = click.style(r['code'].name, fg='green')
            extra_part += click.style('\n  Team: ', bold=True, fg='yellow')
            extra_part += click.style(r['team'])
            extra_part += click.style('\n  Service: ', bold=True, fg='yellow')
            extra_part += click.style(r['service'])
            extra_part += click.style('\n  Round: ', bold=True, fg='yellow')
            extra_part += click.style('{0:d}'.format(r['round']))
            extra_part += click.style(
                '\n  Not before: ', bold=True, fg='yellow')
            extra_part += click.style(
                '{0:%-m}/{0:%-d} {0:%H}:{0:%M}:{0:%S}'.format(r['nbf']))
            extra_part += click.style('\n  Expires: ', bold=True, fg='yellow')
            extra_part += click.style(
                '{0:%-m}/{0:%-d} {0:%H}:{0:%M}:{0:%S}'.format(r['exp']))
        else:
            status_part = click.style(r['code'].name, fg='red')

        click.echo(flag_part + '  ' + status_part + extra_part)


@cli.command()
@click.argument('flags', nargs=-1)
def getinfo(flags):
    helper = create_helper()
    results = helper.getinfo(*flags)
    print_getinfo_results(results)
