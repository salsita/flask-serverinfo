# [Flask-ServerInfo](https://github.com/salsita/flask-serverinfo) <a href='https://github.com/salsita'><img align='right' title='Salsita' src='https://www.google.com/a/cpanel/salsitasoft.com/images/logo.gif?alpha=1' /></a>

Flask server info view for inspecting server app and user requests.

[![Version](https://badge.fury.io/gh/salsita%2Fflask-serverinfo.svg)]
(https://github.com/salsita/flask-serverinfo/tags)
[![PyPI package](https://badge.fury.io/py/Flask-ServerInfo.svg)]
(https://pypi.python.org/pypi/Flask-ServerInfo/)
[![Downloads](https://img.shields.io/pypi/dm/Flask-ServerInfo.svg)]
(https://pypi.python.org/pypi/Flask-ServerInfo/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/Flask-ServerInfo.svg)]
(https://pypi.python.org/pypi/Flask-ServerInfo/)
[![License](https://img.shields.io/pypi/l/Flask-ServerInfo.svg)]
(https://pypi.python.org/pypi/Flask-ServerInfo/)


## Supported Platforms

* [Python](http://www.python.org/) >= 2.6, 3.3
* [Flask](http://flask.pocoo.org/) >= 0.5


## Get Started

Install using [pip](https://pip.pypa.io/) or [easy_install](http://pythonhosted.org/setuptools/easy_install.html):
```bash
pip install Flask-ServerInfo
easy_install Flask-ServerInfo
```

## Features

- Provide a view that dumps the server app object and user request object in JSON.


## Changelog

### 0.1.2

#### Fixes

- Fix inspecting dictionaries with non-string keys.
- Fix package setup on Python 3.

### 0.1.1

#### Fixes

- Fix package setup to not require dependencies preinstalled.

### 0.1.0

#### Features

- Initial release.
