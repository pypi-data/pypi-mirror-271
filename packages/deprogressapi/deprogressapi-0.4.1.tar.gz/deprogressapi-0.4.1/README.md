<!--
SPDX-FileCopyrightText: 2020-2024 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences
SPDX-FileCopyrightText: 2021-2024 Helmholtz-Zentrum hereon GmbH

SPDX-License-Identifier: CC-BY-4.0
-->

![DASF Logo](https://git.geomar.de/digital-earth/dasf/dasf-messaging-python/-/raw/master/docs/_static/dasf_logo.svg)

## Progress API for the Data Analytics Software Framework (DASF)

[![CI](https://git.geomar.de/digital-earth/dasf/dasf-progress-api/badges/master/pipeline.svg)](https://git.geomar.de/digital-earth/dasf/dasf-progress-api/-/pipelines?page=1&scope=all&ref=master)
[![Latest Release](https://git.geomar.de/digital-earth/dasf/dasf-progress-api/-/badges/release.svg)](https://git.geomar.de/digital-earth/dasf/dasf-progress-api)
[![PyPI version](https://img.shields.io/pypi/v/deprogressapi.svg)](https://pypi.python.org/pypi/deprogressapi/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![REUSE status](https://api.reuse.software/badge/git.geomar.de/digital-earth/dasf/dasf-progress-api)](https://api.reuse.software/info/git.geomar.de/digital-earth/dasf/dasf-progress-api)

`DASF: Progress API` is part of the Data Analytics Software Framework (DASF, https://git.geomar.de/digital-earth/dasf),
developed at the GFZ German Research Centre for Geosciences (https://www.gfz-potsdam.de).
It is funded by the Initiative and Networking Fund of the Helmholtz Association through the Digital Earth project
(https://www.digitalearth-hgf.de/).

`DASF: Progress API` provides a light-weight tree-based structure to be sent via the DASF RCP messaging protocol.
It's generic design supports deterministic as well as non-deterministic progress reports.
While `DASF: Messaging Python` provides the necessary implementation to distribute
the progress reports from the reporting backend modules,
`DASF: Web` includes ready to use components to visualize the reported progress.

## Installation

Install this package in a dedicated python environment via

```bash
python -m venv venv
source venv/bin/activate
pip install deprogessapi
```

To use this in a development setup, clone the [source code][source code] from
gitlab, start the development server and make your changes::

```bash
git clone https://git.geomar.de/digital-earth/dasf/dasf-progress-api
cd dasf-progress-api
python -m venv venv
source venv/bin/activate
make dev-install
```

More detailed installation instructions my be found in the [docs][docs].


[source code]: https://git.geomar.de/digital-earth/dasf/dasf-progress-api
[docs]: https://digital-earth.pages.geomar.de/dasf/dasf-messaging-python/installation.html


## Service Desk

For everyone without a Geomar Gitlab account, we setup the Service Desk feature for this repository.
It lets you communicate with the developers via a repository specific eMail address. Each request will be tracked via the Gitlab issuse tracker.

eMail: [gitlab+digital-earth-dasf-dasf-progress-api-2274-issue-@git-issues.geomar.de](mailto:gitlab+digital-earth-dasf-dasf-progress-api-2274-issue-@git-issues.geomar.de)


## Usage

A progress report is stored in a tree structure. So there will be one 'root' report instance containing multiple 'sub-reports'.

In order to report the progress simply add a reporter argument with type `ProgressReport` to the exposed method, e.g.

```python
from deprogressapi import ProgressReport

def some_exposed_method(reporter: Optional[ProgressReport] = ProgressReport(
                          step_message="some progress message")) -> str:

    # ...
```

For a report instance new subreports can be created via the `create_subreport` method.
Each created report is published (sent to the requesting client) automatically upon creation and on completion.

```python
# create a subreport
sub_report = root_report.create_subreport(step_message="Calculating something")

# execute some logic
# ...

# mark the sub-report as compelte
sub_report.complete()
```

All sub-reports are again instances of `ProgressReport`, so you can create more sub-reports for each.

### error handling
In order to report an error, you provide an error status argument to the `complete` method. The corresponding error message can be set via the reports `step_message` field.

```python
from deprogressapi.base import Status

# ...
# some code that raises an exception
# ...
except Exception as e:
    error = str(e)
    progress_report.step_message = "error '{msg}': {err}".format(msg=progress_report.step_message, err=error)
    progress_report.complete(Status.ERROR)
```

## Recommended Software Citation

`Eggert, Daniel; Dransch, Doris (2021): DASF: Progress API: A progress reporting structure for the data analytics software framework. V. v0.1.4. GFZ Data Services. https://doi.org/10.5880/GFZ.1.4.2021.007`


## Technical note

This package has been generated from the template
https://codebase.helmholtz.cloud/hcdc/software-templates/python-package-template.git.

See the template repository for instructions on how to update the skeleton for
this package.


## License information

Copyright © 2020-2024 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences



Code files in this repository are licensed under the
Apache-2.0, if not stated otherwise in the file.

Documentation files in this repository are licensed under CC-BY-4.0, if not stated otherwise in the file.

Supplementary and configuration files in this repository are licensed
under CC0-1.0, if not stated otherwise
in the file.

Please check the header of the individual files for more detailed
information.



### License management

License management is handled with [``reuse``](https://reuse.readthedocs.io/).
If you have any questions on this, please have a look into the
[contributing guide][contributing] or contact the maintainers of
`dasf-progress-api`.

[contributing]: https://digital-earth.pages.geomar.de/dasf/dasf-messaging-python/contributing.html
