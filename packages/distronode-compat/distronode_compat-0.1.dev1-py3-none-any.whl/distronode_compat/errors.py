"""Module to deal with errors."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from distronode_compat.constants import DISTRONODE_MISSING_RC, INVALID_PREREQUISITES_RC

if TYPE_CHECKING:
    from subprocess import CompletedProcess


class DistronodeCompatError(RuntimeError):
    """Generic error originating from distronode_compat library."""

    code = 1  # generic error

    def __init__(
        self,
        message: str | None = None,
        proc: CompletedProcess[Any] | None = None,
    ) -> None:
        """Construct generic library exception."""
        super().__init__(message)
        self.proc = proc


class DistronodeCommandError(RuntimeError):
    """Exception running an Distronode command."""

    def __init__(self, proc: CompletedProcess[Any]) -> None:
        """Construct an exception given a completed process."""
        message = (
            f"Got {proc.returncode} exit code while running: {' '.join(proc.args)}"
        )
        super().__init__(message)
        self.proc = proc


class MissingDistronodeError(DistronodeCompatError):
    """Reports a missing or broken Distronode installation."""

    code = DISTRONODE_MISSING_RC

    def __init__(
        self,
        message: str | None = "Unable to find a working copy of distronode executable.",
        proc: CompletedProcess[Any] | None = None,
    ) -> None:
        """."""
        super().__init__(message)
        self.proc = proc


class InvalidPrerequisiteError(DistronodeCompatError):
    """Reports a missing requirement."""

    code = INVALID_PREREQUISITES_RC
