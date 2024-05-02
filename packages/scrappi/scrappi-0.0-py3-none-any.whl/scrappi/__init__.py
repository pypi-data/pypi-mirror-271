"""scrappi - EO Satellite product catalogue retrieval by API or file system"""

__author__ = "Sam Hunt <sam.hunt@npl.co.uk>"
__all__ = []

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
