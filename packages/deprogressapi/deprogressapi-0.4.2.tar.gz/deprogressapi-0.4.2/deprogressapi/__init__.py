# SPDX-FileCopyrightText: 2020-2024 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences
# SPDX-FileCopyrightText: 2021-2024 Helmholtz-Zentrum hereon GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Progress API for the Data Analytics Software Framework (DASF)

basic back-end progress api for the data analytics software framework dasf
"""

from __future__ import annotations

from . import _version
from .base import BaseReport  # noqa: F401
from .print import PrintReport  # noqa: F401
from .tree import ProgressReport  # noqa: F401

__version__ = _version.get_versions()["version"]

__author__ = "Daniel Eggert, Adam Sasin, Philipp S. Sommer"
__copyright__ = "2020-2024 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences"
__credits__ = [
    "Daniel Eggert",
    "Adam Sasin",
    "Philipp S. Sommer",
]
__license__ = "Apache-2.0"

__maintainer__ = "Philipp S. Sommer"
__email__ = "daniel.eggert@gfz-potsdam.de, sasin@hu-potsdam.de, philipp.sommer@hereon.de"

__status__ = "Pre-Alpha"

__all__ = ["BaseReport", "PrintReport", "ProgressReport"]
