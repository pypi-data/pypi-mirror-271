# SPDX-FileCopyrightText: 2020-2024 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences
#
# SPDX-License-Identifier: CC0-1.0

"""Setup script for the dasf-progress-api package."""
import versioneer
from setuptools import setup

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
