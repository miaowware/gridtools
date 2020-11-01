# {{pkg_name}}

{{pkg_description}}

[![PyPI](https://img.shields.io/pypi/v/{{pkg_name}})](https://pypi.org/project/{{pkg_name}}/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{pkg_name}}) ![PyPI - License](https://img.shields.io/pypi/l/{{pkg_name}}) [![Documentation Status](https://readthedocs.org/projects/{{pkg_name}}/badge/?version=latest)](https://{{pkg_name}}.readthedocs.io/en/latest/?badge=latest)

## Using This Template

1. Replace instances of ... with ...:
    * `{{pkg_name}}` with the package name
    * `{{pkg_description}}` with the package description
    * `{{pkg_repo}}` with the package repository URL
    * `{{pkg_site}}` with the package website
    * `{{version}}` with the package version (probably something to do later)
    * `{{authors}}` with the package authors (comma separated)
    * `{{author_emails}}` with the package authors' emails (comma separated)
    * `{{license}}` with the package license name
    * `{{YYYY}}` with the package year of copyright
2. See comments with `NOTE` in them for more details.
3. If you want to use the Github action to publish releases, add the `PYPI_TOKEN` secret.
    * More info: https://pypi.org/help/#apitoken

## Installation

`{{pkg_name}}` requires Python 3.8 at minimum.

```none
$ pip install {{pkg_name}}
```

## Documentation

Documentation is available on [ReadTheDocs](https://{{pkg_name}}.readthedocs.io/).

## Copyright

Copyright {{YYYY}} {{authors}}  
Released under the {{license}} License.  
See [`LICENSE`](LICENSE) for the full license text.
