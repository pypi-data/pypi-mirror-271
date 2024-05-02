"""Test for distronode_compat.loaders module."""
from pathlib import Path

from distronode_compat.loaders import colpath_from_path


def test_colpath_from_path() -> None:
    """Test colpath_from_path non existing path."""
    assert colpath_from_path(Path("/foo/bar/")) is None
