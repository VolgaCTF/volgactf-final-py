# themis-finals-py
[Themis Finals](https://github.com/aspyatkin/themis-finals) CLI & public API library.

## Installation
```
$ pip install themis.finals
```

## Usage
### CLI mode
```
$ THEMIS_FINALS_API_ENDPOINT=10.0.0.2 themis-finals flag getinfo 18adda0e7637fe8a3270808222b3a514= 023897b20007996a0563ab92381f38cc=

18adda0e7637fe8a3270808222b3a514=  SUCCESS
  Team: Lorem
  Service: Ipsum
  Round: 1
  Not before: 5/30 16:19:37
  Expires: 5/30 16:24:37
023897b20007996a0563ab92381f38cc=  SUCCESS
  Team: Dolor
  Service: Sit
  Round: 1
  Not before: 5/30 16:19:37
  Expires: 5/30 16:24:37

$ THEMIS_FINALS_API_ENDPOINT=10.0.0.2 themis-finals flag submit 18adda0e7637fe8a3270808222b3a514= 023897b20007996a0563ab92381f38cc=

18adda0e7637fe8a3270808222b3a514=  SUCCESS
023897b20007996a0563ab92381f38cc=  SUCCESS
```

**Note:** 10.0.0.2 stands for an IP address of contest checking system. You may specify FQDN as well.

You can submit several flags at once. Please take flag API rate limits into consideration.

### Library mode
```python
from themis.finals.flag_api import FlagAPIHelper

h = FlagAPIHelper('10.0.0.2')
flags = [
    '18adda0e7637fe8a3270808222b3a514=',
    '023897b20007996a0563ab92381f38cc='
]

r1 = h.getinfo(*flags)
# [{'flag': '18adda0e7637fe8a3270808222b3a514=', 'code': <GetinfoResult.SUCCESS: 0>, 'exp': datetime.datetime(2018, 5, 30, 16, 24, 37, tzinfo=tzlocal()), 'service': u'Ipsum', 'team': u'Lorem', 'round': 1, 'nbf': datetime.datetime(2018, 5, 30, 16, 19, 37, tzinfo=tzlocal())}, {'flag': '023897b20007996a0563ab92381f38cc=', 'code': <GetinfoResult.SUCCESS: 0>, 'exp': datetime.datetime(2018, 5, 30, 16, 24, 37, tzinfo=tzlocal()), 'service': u'Sit', 'team': u'Dolor', 'round': 1, 'nbf': datetime.datetime(2018, 5, 30, 16, 19, 37, tzinfo=tzlocal())}]

r2 = h.submit(*flags)
# [{'flag': u'18adda0e7637fe8a3270808222b3a514=', 'code': <SubmitResult.SUCCESS: 0>}, {'flag': u'023897b20007996a0563ab92381f38cc=', 'code': <SubmitResult.SUCCESS: 0>}]
```

Result codes are specified in:
- `themis.finals.flag_api.GetinfoResult` enum
- `themis.finals.flag_api.SubmitResult` enum

## License
MIT @ [Alexander Pyatkin](https://github.com/aspyatkin)
