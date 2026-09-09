# volgactf.final
[![PyPI](https://img.shields.io/pypi/v/volgactf.final.svg?style=flat-square)](volgactf.final)
[![PyPI - License](https://img.shields.io/pypi/l/volgactf.final.svg?style=flat-square)](volgactf.final)

[VolgaCTF Final](https://github.com/VolgaCTF/volgactf-final) is an automatic checking system (ACS) for A/D CTF contests.

This repository contains a CLI & public API library for Python 3.

## Installation
```
$ pip install volgactf.final
```

## Flag API
### CLI mode
```bash
$ VOLGACTF_FINAL_API_ENDPOINT=https://final.volgactf.ru volgactf-final flag info 18adda0e7637fe8a3270808222b3a514= 023897b20007996a0563ab92381f38cc=
18adda0e7637fe8a3270808222b3a514= SUCCESS
  Team: Lorem
  Service: Ipsum
  Round: 1
  Not before: 5/30 16:19:37
  Expires: 5/30 16:24:37
023897b20007996a0563ab92381f38cc= SUCCESS
  Team: Dolor
  Service: Sit
  Round: 1
  Not before: 5/30 16:19:37
  Expires: 5/30 16:24:37

$ VOLGACTF_FINAL_API_ENDPOINT=https://final.volgactf.ru volgactf-final flag submit 18adda0e7637fe8a3270808222b3a514= 023897b20007996a0563ab92381f38cc=
18adda0e7637fe8a3270808222b3a514= SUCCESS
023897b20007996a0563ab92381f38cc= SUCCESS
```

**Note 1.** https://final.volgactf.ru stands for an ACS endpoint.

You can submit several flags at once. Please take flag API rate limits into consideration.

### Library mode
```python
from volgactf.final.flag_api import FlagAPIHelper

h = FlagAPIHelper('https://final.volgactf.ru')

flags = [
    '18adda0e7637fe8a3270808222b3a514=',
    '023897b20007996a0563ab92381f38cc='
]

r1 = h.get_info(*flags)
# [{'flag': '18adda0e7637fe8a3270808222b3a514=', 'code': <GetInfoResult.SUCCESS: 0>, 'exp': datetime.datetime(2018, 5, 30, 16, 24, 37, tzinfo=tzlocal()), 'service': u'Ipsum', 'team': u'Lorem', 'round': 1, 'nbf': datetime.datetime(2018, 5, 30, 16, 19, 37, tzinfo=tzlocal())}, {'flag': '023897b20007996a0563ab92381f38cc=', 'code': <GetInfoResult.SUCCESS: 0>, 'exp': datetime.datetime(2018, 5, 30, 16, 24, 37, tzinfo=tzlocal()), 'service': u'Sit', 'team': u'Dolor', 'round': 1, 'nbf': datetime.datetime(2018, 5, 30, 16, 19, 37, tzinfo=tzlocal())}]

r2 = h.submit(*flags)
# [{'flag': u'18adda0e7637fe8a3270808222b3a514=', 'code': <SubmitResult.SUCCESS: 0>}, {'flag': u'023897b20007996a0563ab92381f38cc=', 'code': <SubmitResult.SUCCESS: 0>}]
```

Result codes are specified in `volgactf.final.flag_api.GetInfoResult` and `volgactf.final.flag_api.SubmitResult` enums.

## Capsule API
### CLI mode
```bash
$ VOLGACTF_FINAL_API_ENDPOINT=https://final.volgactf.ru volgactf-final capsule public_key
SUCCESS
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE6O4HeeDG/p7CYoHrDh54SBV2RoYW
oOvajNCsb0tBWPC6VZK2jTFhwzShgAnkwkUvzZMMdDiSmHCZOm5x6KZ25Q==
-----END PUBLIC KEY-----

$ VOLGACTF_FINAL_API_ENDPOINT=https://final.volgactf.ru volgactf-final capsule decode eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJmbGFnIjoiZTI0MWNhZDgwZmE1YzFlZGVlYTE1ZjllNjc4YWU4OTA9In0.5lRNzKi_EPcT_wm6i8X0uhwSrV8y8JW0HAATC0dURV8WIEkHsYWoDACd4laaqWdzkS8No-2QREvEF4f5eg4HFw
SUCCESS
Flag: e241cad80fa5c1edeea15f9e678ae890=
```

### Library mode
```python
from volgactf.final.capsule_api import CapsuleAPIHelper

h = CapsuleAPIHelper('https://final.volgactf.ru')

r1 = h.get_public_key()
# {'public_key': u'-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE6O4HeeDG/p7CYoHrDh54SBV2RoYW\noOvajNCsb0tBWPC6VZK2jTFhwzShgAnkwkUvzZMMdDiSmHCZOm5x6KZ25Q==\n-----END PUBLIC KEY-----\n', 'code': <GetPublicKeyResult.SUCCESS: 0>}

r2 = h.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJmbGFnIjoiZTI0MWNhZDgwZmE1YzFlZGVlYTE1ZjllNjc4YWU4OTA9In0.5lRNzKi_EPcT_wm6i8X0uhwSrV8y8JW0HAATC0dURV8WIEkHsYWoDACd4laaqWdzkS8No-2QREvEF4f5eg4HFw')
# {'decoded': {u'flag': u'e241cad80fa5c1edeea15f9e678ae890='}, 'code': <DecodeResult.SUCCESS: 0>}
```

Result codes are specified in `volgactf.final.capsule_api.GetPublicKeyResult` and `volgactf.final.capsule_api.DecodeResult` enums.

## Service API
### CLI mode
```bash
$ VOLGACTF_FINAL_API_ENDPOINT=https://final.volgactf.ru volgactf-final service list
SUCCESS
#1 Lorem
#2 Ipsum

$ VOLGACTF_FINAL_API_ENDPOINT=https://final.volgactf.ru volgactf-final service status 1 2
#1 UP
#2 NOT_UP
```

### Library mode
```python
from volgactf.final.service_api import ServiceAPIHelper

h = ServiceAPIHelper('https://final.volgactf.ru')

r1 = h.list()
# {'code': <ListResult.SUCCESS: 0>, 'list': [{'id': 1, 'name': 'Lorem'},{'id': 2, 'name': 'Ipsum'}]}

r2 = h.get_status(1, 2)
# [{'service_id': 1, 'code': <GetServiceStatusResult.UP: 0>}, {'service_id': 2, 'code': <GetServiceStatusResult.NOT_UP: 2>}]

r3 = h.is_up(1)
# True
```

Result codes are specified in `volgactf.final.service_api.ListResult` and `volgactf.final.service_api.GetServiceStatusResult` enums.

## Open Data API
### CLI mode
```bash
$ VOLGACTF_FINAL_API_ENDPOINT=https://final.volgactf.ru volgactf-final open_data --team-id 2 --service-id 1
SUCCESS
[
  {
    "round_id": 34,
    "team_id": 2,
    "service_id": 1,
    "open_data": {
      "username": "chk_c59edf8b4cf94c099037994ccf607858"
    },
    "expires": "2026-09-09T13:50:05+00:00"
  },
  {
    "round_id": 35,
    "team_id": 2,
    "service_id": 1,
    "open_data": {
      "username": "chk_c99065f44fdd4f5ea76cfaeb16aae93a"
    },
    "expires": "2026-09-09T13:52:06+00:00"
  },
  {
    "round_id": 36,
    "team_id": 2,
    "service_id": 1,
    "open_data": {
      "username": "chk_31a358df429e4b9faa440dbcdeda3a66"
    },
    "expires": "2026-09-09T13:54:06+00:00"
  }
]

$ volgactf-final open_data --team-id 2 --service-id 1 --no-decode
SUCCESS
[
  {
    "round_id": 34,
    "team_id": 2,
    "service_id": 1,
    "open_data": "{\"username\": \"chk_c59edf8b4cf94c099037994ccf607858\"}",
    "expires": "2026-09-09T13:50:05+00:00"
  },
  {
    "round_id": 35,
    "team_id": 2,
    "service_id": 1,
    "open_data": "{\"username\": \"chk_c99065f44fdd4f5ea76cfaeb16aae93a\"}",
    "expires": "2026-09-09T13:52:06+00:00"
  },
  {
    "round_id": 36,
    "team_id": 2,
    "service_id": 1,
    "open_data": "{\"username\": \"chk_31a358df429e4b9faa440dbcdeda3a66\"}",
    "expires": "2026-09-09T13:54:06+00:00"
  }
]
```

Both `--team-id` and `--service-id` filters are optional. The command prints `SUCCESS` followed by the JSON
list, or `ERROR` on failure.
Use `--no-decode` to preserve the original payload strings. TLS verification is enabled by default.

### Library mode
```python
from volgactf.final.open_data_api import OpenDataAPIHelper, OpenDataResult

h = OpenDataAPIHelper('https://final.volgactf.test')
r1 = h.open_data(team_id=2, service_id=1)
# {'code': <OpenDataResult.SUCCESS: 0>, 'list': [{'round_id': 34, 'team_id': 2, 'service_id': 1, 'open_data': {'username': 'chk_c59edf8b4cf94c099037994ccf607858'}, 'expires': '2026-09-09T13:50:05+00:00'}, {'round_id': 35, 'team_id': 2, 'service_id': 1, 'open_data': {'username': 'chk_c99065f44fdd4f5ea76cfaeb16aae93a'}, 'expires': '2026-09-09T13:52:06+00:00'}, {'round_id': 36, 'team_id': 2, 'service_id': 1, 'open_data': {'username': 'chk_31a358df429e4b9faa440dbcdeda3a66'}, 'expires': '2026-09-09T13:54:06+00:00'}]}

r2 = h.open_data(team_id=2, service_id=1, decode=False)
# {'code': <OpenDataResult.SUCCESS: 0>, 'list': [{'round_id': 34, 'team_id': 2, 'service_id': 1, 'open_data': '{"username": "chk_c59edf8b4cf94c099037994ccf607858"}', 'expires': '2026-09-09T13:50:05+00:00'}, {'round_id': 35, 'team_id': 2, 'service_id': 1, 'open_data': '{"username": "chk_c99065f44fdd4f5ea76cfaeb16aae93a"}', 'expires': '2026-09-09T13:52:06+00:00'}, {'round_id': 36, 'team_id': 2, 'service_id': 1, 'open_data': '{"username": "chk_31a358df429e4b9faa440dbcdeda3a66"}', 'expires': '2026-09-09T13:54:06+00:00'}]}
```

`team_id` and `service_id` accept integers or `None` (no filter). When both are
supplied, both must match. Filtering happens before decoding. By default, each
selected row's `open_data` string is first decoded as strict base64 if valid;
otherwise the original string is used. The resulting payload is then parsed
as JSON and must be a dictionary, which replaces the row's `open_data` string.
Other fields and row order are preserved. Set `decode=False` to skip payload
decoding entirely.

Successful calls return `{'code': OpenDataResult.SUCCESS, 'list': [...]}`.
Any request, filtering, or decoding failure returns only
`{'code': OpenDataResult.ERROR}`. Decoding stops at the first failed row;
no partial list is returned.

## License
MIT @ [VolgaCTF](https://github.com/VolgaCTF)
