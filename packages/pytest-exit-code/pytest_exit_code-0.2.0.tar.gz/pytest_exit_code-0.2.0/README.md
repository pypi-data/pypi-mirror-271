# pytest-exit-code [![PyPi version][pypi-version-badge]][pypi-project] [![Python versions][pypi-pyversions-badge]][pypi-project]

A [pytest] plugin that overrides the built-in exit codes to retain more information about the test results.

## Features

This plugin changes the exit code returned by running `pytest`.
The exit codes can range from `0` to `63` and are a combination of the following bitwise flags:

| Flag | Description                     |
| ---- | ------------------------------- |
| `0`  | All tests passed.               |
| `1`  | One or more tests passed.       |
| `2`  | One or more tests failed.       |
| `4`  | One or more tests errored.      |
| `8`  | One or more tests were skipped. |
| `16` | One or more tests xfailed.      |
| `32` | One or more tests xpassed.      |

So:

- An exit code of `2` means that all tests failed.
- An exit code of `6` means that all tests either failed or errored.
- An exit code of `7` indicates that the result contains a mix of passed, failed and errored tests.

## Installation

```sh
$ pip install python-exit-code
```

## Contributing

Contributions are very welcome.
Tests can be run with [tox], please ensure the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [Apache Software License 2.0] license, `pytest-exit-code` is free and open source software.

[Apache Software License 2.0]: https://www.apache.org/licenses/LICENSE-2.0
[pypi-project]: https://pypi.org/project/pytest-exit-code
[pypi-version-badge]: https://img.shields.io/pypi/v/pytest-exit-code.svg
[pypi-pyversions-badge]: https://img.shields.io/pypi/pyversions/pytest-exit-code.svg
[pytest]: https://github.com/pytest-dev/pytest
[tox]: https://tox.readthedocs.io/en/latest/
