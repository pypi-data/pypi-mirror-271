# type: ignore[attr-defined]
"""Ortogonal Polynomials in the unit sphere."""

import sys
from importlib import metadata as importlib_metadata

from .associated_legendre_functions import associated_legendre
from .legendre_polynomials import legendre


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
