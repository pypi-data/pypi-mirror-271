[![Build Status](https://dev.azure.com/p4irin/c4t/_apis/build/status%2Fp4irin.c4t?branchName=master&jobName=BuildAndTest&configuration=BuildAndTest%20Python38)](https://dev.azure.com/p4irin/c4t/_build/latest?definitionId=5&branchName=master)
[![c4t publish](https://github.com/p4irin/c4t/actions/workflows/python-publish.yml/badge.svg)](https://github.com/p4irin/c4t/actions/workflows/python-publish.yml)
![PyPI - Version](https://img.shields.io/pypi/v/c4t)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/c4t)
![PyPI - Format](https://img.shields.io/pypi/format/c4t)
![PyPI - License](https://img.shields.io/pypi/l/c4t)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
# c4t: Chrome for Testing - v1.6.0

Install _Chrome for Testing_ assets. A flavor of Chrome, specifically for testing and a matching chromedriver. Currently, the version of assets installed is for _linux64_ platforms only.

## Why Chrome for Testing?

Taken from [the Chrome Developers Blog](https://developer.chrome.com/blog/chrome-for-testing/)

> ...setting up an adequate browser testing environment is notoriously difficult...
>
> You want consistent, reproducible results across repeated test runs—but this may not happen if the browser executable or binary decides to update itself in between two runs.
>
>You want to pin a specific browser version and check that version number into your source code repository, so that you can check out old commits and branches and re-run the tests against the browser binary from that point in time.
>
> Not only do you have to download a Chrome binary somehow, you also need a correspondingly-versioned ChromeDriver binary to ensure the two binaries are compatible.
>
> Chrome for Testing is a dedicated flavor of Chrome targeting the testing use case, without auto-update, integrated into the Chrome release process, made available for every Chrome release
>
> ...finding a matching Chrome and ChromeDriver binary can be completely eliminated by integrating the ChromeDriver release process into the Chrome for Testing infrastructure.

## Requirements

To use Chrome for Testing assets you'll need a version of Selenium > 4.11.0

## Installation

### From PyPI

```bash
(venv) $ pip install c4t
(venv) $
```

### From GitHub

```bash
(venv) $ pip install git+https://github.com/p4irin/c4t.git
(venv) $
```

## Verify

### In a REPL

#### Show version

```bash
(venv) $ python
Python 3.8.10 (default, Jun  2 2021, 10:49:15) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import c4t
>>> c4t.__version__
'<major>.<minor>.<patch>'
>>>
```

### Or on the command line

#### Show version

```bash
(venv) $ c4t --version
v1.1.0
(venv) $
```

#### Display package documentation

```bash
(venv) $ python -m pydoc c4t
(venv) $
```

## Usage

### In code

#### Install the default, the latest stable version and use it with Selenium

```bash
Python 3.8.10 (default, May 26 2023, 14:05:08) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import c4t
>>> assets = c4t.Assets()
>>> assets.install()
Create directory ${HOME}/.c4t-assets/124.0.6367.91
Downloading chrome-linux64.zip.
100% [......................................................................] 146689409 / 146689409

Downloading chromedriver-linux64.zip.
100% [..........................................................................] 7508443 / 7508443

Unzipping chrome-linux64.zip
Unzipping chromedriver-linux64.zip
Creating symlink to chrome version 117.0.5938.62
Creating symlink to chromedriver version 117.0.5938.62
Finished installing version 117.0.5938.62 of Chrome for Testing and Chromedriver.
-------------------------------------------
Version 117.0.5938.62 is the active version
-------------------------------------------
>>> from selenium.webdriver import ChromeOptions, ChromeService, Chrome
>>> options = ChromeOptions()
>>> options.binary_location = c4t.location.chrome
>>> service = ChromeService(executable_path=c4t.location.chromedriver)
>>> browser = Chrome(options=options, service=service)
>>> browser.get('https://pypi.org/user/p4irin/')
>>> browser.close()
>>> browser.quit()
>>>
```

### On the command line

#### Display command line help

```bash
(venv) $ c4t --help
usage: c4t [-h] [-V] {install,path,list,switch,delete} ...

Install 'Chrome for Testing' assets

options:
  -h, --help            show this help message and exit
  -V, --version         Show version and exit.

Commands:
  {install,path,list,switch,delete}
    install             Install a version of 'Chrome for Testing' assets
    path                Show the installation path of assets and exit
    list                List versions
    switch              Switch the active version
    delete              Delete an installed version

Reference: https://github.com/GoogleChromeLabs/chrome-for-testing
```

```bash
(venv) $ c4t install --help
usage: c4t install [-h] [--version VERSION] [-l]

Install a version of 'Chrome for Testing' assets.

options:
  -h, --help            show this help message and exit
  --version VERSION     The version of 'Chrome for Testing' assets to install. The default is 'latest'
  -l, --last-known-good-version
                        Install a last known good version from a list
```

#### Install the default, the latest stable version

```bash
# By default assets are installed in ${HOME}/.c4t-assets
# To use a different path, set the C4T_PATH_TO_ASSETS environment variable.
# e.g.: export C4T_PATH_TO_ASSETS=<path>
# Add this export to your .bashrc so the path is set for every bash session.
(venv) $ c4t install
```

#### Install a specific version

```bash
(venv) $ c4t install --version 116.0.5794.0
```

#### Install a last known good version from a list

```bash
# Notice the list also indicates versions you already installed
(venv) $ c4t install -l
0 - Stable version=124.0.6367.91, revision=1274542, installed
1 - Beta version=125.0.6422.26, revision=1287751
2 - Dev version=126.0.6439.0, revision=1292160, installed
3 - Canary version=126.0.6449.0, revision=1293886
Select a version by number:
```

#### Show installation path of assets

```bash
(venv) $ c4t path
Path to assets: /home/p4irin/.c4t-assets
```

#### Show the currently active version

```bash
(venv) $ c4t list --active
Active version of 'Chrome for Testing' assets installed: 124.0.6367.91
```

#### Show a list of installed versions

```bash
# Notice the active version is marked 'active'
(venv) $ c4t list --installed
0 - 116.0.5794.0
1 - 124.0.6367.91, active
2 - 125.0.6422.14
3 - 126.0.6439.0
```

#### Show a list of last known good versions

```bash
(venv) $ c4t list --last-known-good-versions
0 - Stable version=124.0.6367.91, revision=1274542, installed
1 - Beta version=125.0.6422.26, revision=1287751
2 - Dev version=126.0.6439.0, revision=1292160, installed
3 - Canary version=126.0.6449.0, revision=1293886
```

#### Switch active version

```bash
(venv) $ c4t switch
0 - 116.0.5794.0
1 - 124.0.6367.91, active
2 - 125.0.6422.14
3 - 126.0.6439.0
Select a version by number: 0
Creating symlink to chrome version 116.0.5794.0
Creating symlink to chromedriver version 116.0.5794.0
Active version is now: 116.0.5794.0
```

### Common workflow

1. Install one or more versions of Chrome for testing assets
1. Set/switch the active version
1. Run your Selenium Webdriver tests with the active version of Chrome for testing

E.g., this allows for quickly switching back to a previous version of Chrome to run your tests against in case of a regression on a recent/latest version. For example, a test failing against the latest of Chrome, did it pass consistently on the previous version or is it flaky and in need for a more robust implementation?

## Reference

- [Blog](https://developer.chrome.com/blog/chrome-for-testing/)
- [GitHub](https://github.com/GoogleChromeLabs/chrome-for-testing)
