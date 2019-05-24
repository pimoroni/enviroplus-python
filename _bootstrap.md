* Python Library - library/name/__init__.py
* At least *one*  test - library/tests/test_setup.py
* Examples

# In Detail

To get started, copy the contents of this repository (excluding the .git directory) and run `_bootstrap.sh` to highlight substitutions you need to make.

Be careful to copy *all* files, including those starting with a . such as `.travis.yml`.

A Makefile is provided to automate some tests, checks and package building. You should use it!

## Library

### Structure

Libraries should be singleton if they pertain to a HAT or pHAT and class-based if they are for breakouts with selectable addresses.

A singleton library would work like this:

```
import library

library.do_something()
```

Whereas a class-based library requires an instance of its class:

```
import library

device = library.Library()

device.do_something()
```

### Linting

You should ensure you either run `flake8` while writing the library, or use an IDE/Editor with linting.

All libraries (and example code) should stick to PEP8 style guides, although you can ignore long line warnings (E501) if you feel they're unwarranted.

### Testing

At least one test script should be used to prevent obvious errors and omissions from creeping into the library.

You should use `tox` to run the test scripts:

```
sudo pip install tox
cd library/
tox
```

## Examples

Examples should use hyphens and short, descriptive names, ie: `rainbow-larson.py`

Examples should include a `print()` front-matter introducing them, ie:

```
print("""rainbow-larson.py - Display a larson scanning rainbow

Press Ctrl+C to exit.

""")
```

# Deployment

Before deploying you should `make python-testdeploy` and verify that the package looks good and is installable from test PyPi.

You should also `make check` to catch common errors, including mismatched version numbers, trailing whitespace and DOS line-endings.

Subsequent to deployment you should `git tag -a "vX.X.X" -m "Version X.X.X"` and `git push origin master --follow-tags` to tag a release on GitHub that matches the deployed code.
