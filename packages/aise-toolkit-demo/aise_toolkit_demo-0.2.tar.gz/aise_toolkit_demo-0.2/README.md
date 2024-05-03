# aise-toolkit-demo

[![PyPI](https://img.shields.io/pypi/v/aise-toolkit-demo.svg)](https://pypi.org/project/aise-toolkit-demo/)
[![Changelog](https://img.shields.io/github/v/release/ups216/aise-toolkit-demo?include_prereleases&label=changelog)](https://github.com/ups216/aise-toolkit-demo/releases)
[![Tests](https://github.com/ups216/aise-toolkit-demo/actions/workflows/test.yml/badge.svg)](https://github.com/ups216/aise-toolkit-demo/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ups216/aise-toolkit-demo/blob/master/LICENSE)

A set of tools to assist developer to use AI

## Installation

Install this tool using `pip`:
```bash
pip install aise-toolkit-demo
```
## Usage

For help, run:
```bash
aise-toolkit-demo --help
```
You can also use:
```bash
python -m aise_toolkit_demo --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd aise-toolkit-demo
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```

```shell
# create a one-folder bundle
pyinstaller --name aise --noconfirm --log-level=WARN --onedir --nowindow ./aise_toolkit_demo/cli.py
# create a single-file bundle
pyinstaller --name aise --noconfirm --log-level=WARN --onefile --nowindow ./aise_toolkit_demo/cli.py
```
