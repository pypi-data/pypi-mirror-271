# nmk-vscode
VSCode plugin for nmk build system

<!-- NMK-BADGES-BEGIN -->
[![License: MPL](https://img.shields.io/github/license/dynod/nmk-vscode?color=green)](https://github.com/dynod/nmk-vscode/blob/main/LICENSE)
[![Checks](https://img.shields.io/github/actions/workflow/status/dynod/nmk-vscode/build.yml?branch=main&label=build%20%26%20u.t.)](https://github.com/dynod/nmk-vscode/actions?query=branch%3Amain)
[![Issues](https://img.shields.io/github/issues-search/dynod/nmk?label=issues&query=is%3Aopen+is%3Aissue+label%3Aplugin%3Avscode)](https://github.com/dynod/nmk/issues?q=is%3Aopen+is%3Aissue+label%3Aplugin%3Avscode)
[![Supported python versions](https://img.shields.io/badge/python-3.8%20--%203.11-blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/nmk-vscode)](https://pypi.org/project/nmk-vscode/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Flake8 analysis result](https://img.shields.io/badge/flake8-0-green)](https://flake8.pycqa.org/)
[![Code coverage](https://img.shields.io/codecov/c/github/dynod/nmk-vscode)](https://app.codecov.io/gh/dynod/nmk-vscode)
[![Documentation Status](https://readthedocs.org/projects/nmk-vscode/badge/?version=stable)](https://nmk-vscode.readthedocs.io/)
<!-- NMK-BADGES-END -->

This plugin helps to generate various [VS Code](https://code.visualstudio.com/) files for an easier integration:
- settings
- launch configrations
- automated tasks
- recommended extensions

## Usage

To use this plugin in your **`nmk`** project, insert this reference:
```yaml
refs:
    - pip://nmk-vscode!plugin.yml
```

## Documentation

This plugin documentation is available [here](https://nmk-vscode.readthedocs.io/)

## Issues

Issues for this plugin shall be reported on the [main  **`nmk`** project](https://github.com/dynod/nmk/issues), using the **plugin:vscode** label.
