# SPDX-FileCopyrightText: 2023 - 2024 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Top-level package for python active versions."""
import logging

from python_active_versions.bundle import get_bundle_dir

try:
    from icecream import ic, install

    # installing icecream
    install()
    ic.configureOutput(outputFunction=logging.debug, includeContext=True)
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa  # pylint: disable=C3001

__author__ = "Gabriele Pongelli"
__email__ = "gabriele.pongelli@gmail.com"
__version__ = "1.14.0"

__description__ = "Gather active python versions."
__project_name__ = "python-active-versions"
