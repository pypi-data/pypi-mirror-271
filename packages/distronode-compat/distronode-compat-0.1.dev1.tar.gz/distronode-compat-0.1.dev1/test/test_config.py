"""Tests for distronode_compat.config submodule."""
import copy
import subprocess

import pytest
from _pytest.monkeypatch import MonkeyPatch
from packaging.version import Version

from distronode_compat.config import DistronodeConfig, distronode_version, parse_distronode_version
from distronode_compat.errors import InvalidPrerequisiteError, MissingDistronodeError


def test_config() -> None:
    """Checks that config vars are loaded with their expected type."""
    config = DistronodeConfig()
    assert isinstance(config.ACTION_WARNINGS, bool)
    assert isinstance(config.CACHE_PLUGIN_PREFIX, str)
    assert isinstance(config.CONNECTION_FACTS_MODULES, dict)
    assert config.DISTRONODE_COW_PATH is None
    assert isinstance(config.NETWORK_GROUP_MODULES, list)
    assert isinstance(config.DEFAULT_GATHER_TIMEOUT, (int, type(None)))

    # check lowercase and older name aliasing
    assert isinstance(config.collections_paths, list)
    assert isinstance(config.collections_path, list)
    assert config.collections_paths == config.collections_path

    # check if we can access the special data member
    assert config.data["ACTION_WARNINGS"] == config.ACTION_WARNINGS

    with pytest.raises(AttributeError):
        _ = config.THIS_DOES_NOT_EXIST


def test_config_with_dump() -> None:
    """Tests that config can parse given dumps."""
    config = DistronodeConfig(config_dump="ACTION_WARNINGS(default) = True")
    assert config.ACTION_WARNINGS is True


def test_config_copy() -> None:
    """Checks ability to use copy/deepcopy."""
    config = DistronodeConfig()
    new_config = copy.copy(config)
    assert isinstance(new_config, DistronodeConfig)
    assert new_config is not config
    # deepcopy testing
    new_config = copy.deepcopy(config)
    assert isinstance(new_config, DistronodeConfig)
    assert new_config is not config


def test_parse_distronode_version_fail() -> None:
    """Checks that parse_distronode_version raises an error on invalid input."""
    with pytest.raises(
        InvalidPrerequisiteError,
        match="Unable to parse distronode cli version",
    ):
        parse_distronode_version("foo")


def test_distronode_version_missing(monkeypatch: MonkeyPatch) -> None:
    """Validate distronode_version behavior when distronode is missing."""
    monkeypatch.setattr(
        "subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(  # noqa: ARG005
            args=[],
            returncode=1,
        ),
    )
    with pytest.raises(
        MissingDistronodeError,
        match="Unable to find a working copy of distronode executable.",
    ):
        # bypassing lru cache
        distronode_version.__wrapped__()


def test_distronode_version() -> None:
    """Validate distronode_version behavior."""
    assert distronode_version() >= Version("1.0")


def test_distronode_version_arg() -> None:
    """Validate distronode_version behavior."""
    assert distronode_version("2.0") >= Version("1.0")
