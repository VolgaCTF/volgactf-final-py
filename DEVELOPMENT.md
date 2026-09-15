## Developer guide

### Setup devenv

Create a new virtualenv, activate it and install dependencies:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Release a new version

1. Activate the virtualenv
2. Bump a version in `volgactf/final/__about__.py`
3. Clean up old distributions in `dist`
4. Build new distributions with `python -m build`
5. Check the built distributions with `python -m twine check dist/*`
6. Upload the distributions with `python -m twine upload dist/*`
