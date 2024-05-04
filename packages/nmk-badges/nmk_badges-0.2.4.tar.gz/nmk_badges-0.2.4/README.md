# nmk-badges
Readme badges generation plugin for nmk build system

<!-- NMK-BADGES-BEGIN -->
[![License: MPL](https://img.shields.io/github/license/dynod/nmk-badges?color=green)](https://github.com/dynod/nmk-badges/blob/main/LICENSE)
[![Checks](https://img.shields.io/github/actions/workflow/status/dynod/nmk-badges/build.yml?branch=main&label=build%20%26%20u.t.)](https://github.com/dynod/nmk-badges/actions?query=branch%3Amain)
[![Issues](https://img.shields.io/github/issues-search/dynod/nmk?label=issues&query=is%3Aopen+is%3Aissue+label%3Aplugin%3Abadges)](https://github.com/dynod/nmk/issues?q=is%3Aopen+is%3Aissue+label%3Aplugin%3Abadges)
[![Supported python versions](https://img.shields.io/badge/python-3.8%20--%203.11-blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/nmk-badges)](https://pypi.org/project/nmk-badges/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Flake8 analysis result](https://img.shields.io/badge/flake8-0-green)](https://flake8.pycqa.org/)
[![Code coverage](https://img.shields.io/codecov/c/github/dynod/nmk-badges)](https://app.codecov.io/gh/dynod/nmk-badges)
[![Documentation Status](https://readthedocs.org/projects/nmk-badges/badge/?version=stable)](https://nmk-badges.readthedocs.io/)
<!-- NMK-BADGES-END -->

This plugin adds support for README markdown [badges/shields](https://shields.io/) generation.

## Usage

To use this plugin in your **`nmk`** project, insert this reference:
```yaml
refs:
    - pip://nmk-badges!plugin.yml
```

## Documentation

This plugin documentation is available [here](https://nmk-badges.readthedocs.io/)

## Issues

Issues for this plugin shall be reported on the [main  **`nmk`** project](https://github.com/dynod/nmk/issues), using the **plugin:badges** label.
