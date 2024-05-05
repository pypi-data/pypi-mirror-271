# wordc

> Small utility to analyze the word frequency in a text file

# 🚀 Quickstart

---

## 💾 Installation

Using pipx (undoubtedly the best way):

```sh
pipx install wordc
```

OS X & Linux:

```sh
pip3 install wordc
```

Windows:

```sh
pip install wordc
```

# 🔧 Development setup

---

```sh
pip install --editable wordc
```

# 📝 Usage

---

Display the help menu with the `-h` argument

```bash
~ $ wordc -h
```

```bash
usage: wordc [-h] [-e ENCODING] [-c] [-s SIZE] [-t TOP_WORDS] [--version] FILENAME

Utility to list the top word frequency in a document

positional arguments:
  FILENAME              file to analyze for word frequency

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        Encoding to use when reading file
  -c, --chunk           Force file chunking irrespective of file size
  -s SIZE, --size SIZE  Chunk size to use when reading file
  -t TOP_WORDS, --top_words TOP_WORDS
                        Number of top words to list
  --version             display version number
```

specify the file

```bash
~ $ wordc text_file.txt
4284 the
2192 and
2185 of
1861 a
1685 to
```

File chunking will happen automatically in certain situations:

1. When the (file size / availanle memory) ratio is over 25%
2. When the file size is over 100Mb

File chunking can be forced however by using the `-c` argument.

# <ℹ️> Meta

---

[![](assets/linkedin.png)](https://www.linkedin.com/in/sr-king)
[![](assets/github.png)](https://github.com/Stephen-RA-King)
[![](assets/pypi.png)](https://pypi.org/project/wordc)
[![Docker](assets/docker.png)](https://hub.docker.com/r/sraking/wordc)
[![](assets/www.png)](https://stephen-ra-king.github.io/justpython/)
[![](assets/email2.png)](mailto:sking.github@gmail.com)
[![](assets/github.png)](https://github.com/Stephen-RA-King/wordc)

Author: Stephen R A King ([sking.github@gmail.com](mailto:sking.github@gmail.com))

Created with Cookiecutter template: [![pydough][pydough-image]][pydough-url] version 1.3.4

<!-- Markdown link & img dfn's -->

[bandit-image]: https://img.shields.io/badge/security-bandit-yellow.svg
[bandit-url]: https://github.com/PyCQA/bandit
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[codeclimate-image]: https://api.codeclimate.com/v1/badges/7fc352185512a1dab75d/maintainability
[codeclimate-url]: https://codeclimate.com/github/Stephen-RA-King/wordc/maintainability
[codecov-image]: https://codecov.io/gh/Stephen-RA-King/wordc/branch/main/graph/badge.svg
[codecov-url]: https://app.codecov.io/gh/Stephen-RA-King/wordc
[codefactor-image]: https://www.codefactor.io/repository/github/Stephen-RA-King/wordc/badge
[codefactor-url]: https://www.codefactor.io/repository/github/Stephen-RA-King/wordc
[codeql-image]: https://github.com/Stephen-RA-King/wordc/actions/workflows/github-code-scanning/codeql/badge.svg
[codeql-url]: https://github.com/Stephen-RA-King/wordc/actions/workflows/github-code-scanning/codeql
[commitizen-image]: https://img.shields.io/badge/commitizen-friendly-brightgreen.svg
[commitizen-url]: http://commitizen.github.io/cz-cli/
[conventional-commits-image]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square
[conventional-commits-url]: https://conventionalcommits.org
[deepsource-image]: https://app.deepsource.com/gh/Stephen-RA-King/wordc.svg/?label=active+issues&show_trend=true
[deepsource-url]: https://app.deepsource.com/gh/Stephen-RA-King/wordc/?ref=repository-badge
[docker-image]: https://github.com/Stephen-RA-King/wordc/actions/workflows/docker-image.yml/badge.svg
[docker-url]: https://github.com/Stephen-RA-King/wordc/actions/workflows/docker-image.yml
[downloads-image]: https://static.pepy.tech/personalized-badge/wordc?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads
[downloads-url]: https://pepy.tech/project/wordc
[format-image]: https://img.shields.io/pypi/format/wordc
[isort-image]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
[isort-url]: https://github.com/pycqa/isort/
[lgtm-alerts-image]: https://img.shields.io/lgtm/alerts/g/Stephen-RA-King/wordc.svg?logo=lgtm&logoWidth=18
[lgtm-alerts-url]: https://lgtm.com/projects/g/Stephen-RA-King/wordc/alerts/
[lgtm-quality-image]: https://img.shields.io/lgtm/grade/python/g/Stephen-RA-King/wordc.svg?logo=lgtm&logoWidth=18
[lgtm-quality-url]: https://lgtm.com/projects/g/Stephen-RA-King/wordc/context:python
[license-image]: https://img.shields.io/pypi/l/wordc
[license-url]: https://github.com/Stephen-RA-King/wordc/blob/main/LICENSE
[mypy-image]: http://www.mypy-lang.org/static/mypy_badge.svg
[mypy-url]: http://mypy-lang.org/
[openssf-image]: https://api.securityscorecards.dev/projects/github.com/Stephen-RA-King/wordc/badge
[openssf-url]: https://api.securityscorecards.dev/projects/github.com/Stephen-RA-King/wordc
[pre-commit-image]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[pre-commit.ci-image]: https://results.pre-commit.ci/badge/github/Stephen-RA-King/wordc/main.svg
[pre-commit.ci-url]: https://results.pre-commit.ci/latest/github/Stephen-RA-King/wordc/main
[pydough-image]: https://img.shields.io/badge/pydough-2023-orange?logo=cookiecutter
[pydough-url]: https://github.com/Stephen-RA-King/pydough
[pypi-url]: https://pypi.org/project/wordc/
[pypi-image]: https://img.shields.io/pypi/v/wordc.svg
[python-version-image]: https://img.shields.io/pypi/pyversions/wordc
[readthedocs-image]: https://readthedocs.org/projects/wordc/badge/?version=latest
[readthedocs-url]: https://wordc.readthedocs.io/en/latest/?badge=latest
[status-image]: https://img.shields.io/pypi/status/wordc.svg
[tests-image]: https://github.com/Stephen-RA-King/wordc/actions/workflows/tests.yml/badge.svg
[tests-url]: https://github.com/Stephen-RA-King/wordc/actions/workflows/tests.yml
[versioning-image]: https://img.shields.io/badge/versioning-semver_2-blue
[versioning-url]: https://semver.org/
[wiki]: https://github.com/Stephen-RA-King/wordc/wiki
