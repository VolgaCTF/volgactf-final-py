# -*- coding: utf-8 -*-
import base64
import binascii
from enum import Enum
import json

import requests


class OpenDataResult(Enum):
    """Result codes for fetching jury open data."""

    SUCCESS = 0
    ERROR = 1


class OpenDataAPIHelper(object):
    """Fetch and filter open-data rows published by the VolgaCTF Final jury."""

    def __init__(self, endpoint, proxy=None, verify=True):
        """Configure the ACS base URL, optional proxy, and TLS verification.

        ``verify`` accepts a boolean or a CA bundle path, as in requests.
        Use ``verify=False`` to access a local ACS with a self-signed certificate.
        """
        self._endpoint = endpoint
        self._url_path = 'api/open_data/v1'
        self._proxies = dict()
        if proxy is not None:
            self._proxies[endpoint] = proxy
        self._verify = verify

    @property
    def open_data_url(self):
        """Return the jury open-data endpoint URL."""
        return '{0}/{1}'.format(
            self._endpoint,
            self._url_path
        )

    def open_data(self, team_id=None, service_id=None, decode=True):
        """Fetch rows, optionally matching integer team and service IDs.

        Both filters must match when supplied. None disables a filter; zero
        remains a valid ID. Filtering precedes decoding and ordering is preserved.
        By default, each selected row's ``open_data`` string is base64-decoded
        if valid base64, then JSON-decoded into a dictionary. Non-base64 strings are
        parsed to JSON decoding directly. Set ``decode=False`` to retain raw strings.

        Return a dictionary with ``code=OpenDataResult.SUCCESS`` and a
        ``list``, which may be empty. HTTP, request, JSON decoding, or filtering
        failures return only ``code=OpenDataResult.ERROR``. A payload decoding
        failure or non-dictionary payload fails the entire call immediately.
        """
        try:
            r = requests.get(self.open_data_url, proxies=self._proxies, verify=self._verify)
            if r is not None and r.status_code == requests.codes.ok:
                data = r.json()
                if not isinstance(data, list):
                    return dict(code=OpenDataResult.ERROR)
                if team_id is not None:
                    data = [row for row in data if row['team_id'] == team_id]
                if service_id is not None:
                    data = [row for row in data if row['service_id'] == service_id]
                if decode:
                    decoded_data = list()
                    for row in data:
                        payload = row['open_data']
                        if not isinstance(payload, str):
                            return dict(code=OpenDataResult.ERROR)
                        try:
                            payload = base64.b64decode(payload, validate=True)
                        except (binascii.Error, ValueError):
                            pass
                        payload = json.loads(payload)
                        if not isinstance(payload, dict):
                            return dict(code=OpenDataResult.ERROR)
                        decoded_data.append(dict(row, open_data=payload))
                    data = decoded_data
                return dict(
                    code=OpenDataResult.SUCCESS,
                    list=data
                )
            else:
                return dict(code=OpenDataResult.ERROR)
        except Exception:
            return dict(code=OpenDataResult.ERROR)
