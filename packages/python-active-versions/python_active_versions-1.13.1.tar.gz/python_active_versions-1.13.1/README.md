# python active versions


[![pypi](https://img.shields.io/pypi/v/python-active-versions.svg)](https://pypi.org/project/python-active-versions/)
[![python](https://img.shields.io/pypi/pyversions/python-active-versions.svg)](https://pypi.org/project/python-active-versions/)
[![Build Status](https://github.com/gpongelli/python-active-versions/actions/workflows/dev.yml/badge.svg)](https://github.com/gpongelli/python-active-versions/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/gpongelli/python-active-versions/branch/main/graphs/badge.svg)](https://codecov.io/github/gpongelli/python-active-versions)



Gather active python versions and, optionally, also docker images.


* Documentation: <https://gpongelli.github.io/python-active-versions>
* GitHub: <https://github.com/gpongelli/python-active-versions>
* PyPI: <https://pypi.org/project/python-active-versions/>
* Free software: MIT

## Usage

For its usage, as CLI/docker container/library please refer to usega page into [documentation](https://gpongelli.github.io/python-active-versions).

An interesting usage is in combination with nox, where this library can provide python versions as following snippet:

```python
import nox

from python_active_versions.python_active_versions import get_active_python_versions
from typing import List

def _get_active_version(_active_versions: List[dict]) -> List[str]:
    return [_av['version'] for _av in _active_versions]

_python_versions = _get_active_version(get_active_python_versions())

@nox.session(python=_python_versions)
def test_something(session):
    ...

@nox.session(python=_python_versions)
def test_another(session):
    ...
```


## Features

* Scrape official python website to get active versions
* Scrape dockerhub website to add optional python's available images

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [gpongelli/cookiecutter-pypackage](https://github.com/gpongelli/cookiecutter-pypackage) project template.
