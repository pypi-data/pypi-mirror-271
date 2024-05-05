"""Module for conveniently parsing options resolved from command-line arguments."""

from __future__ import annotations

import sys
from dataclasses import InitVar, dataclass, fields
from typing import Any

from awsglue.utils import getResolvedOptions
from typing_extensions import Self


@dataclass
class BaseOptions:
    """Dataclass for storing resolved options."""

    job_arguments: InitVar[dict[str, Any]]

    @classmethod
    def from_resolved_options(cls) -> Self:
        """Create an instance of the class from Glue's resolved options."""
        params = []
        if "--JOB_NAME" in sys.argv:
            params.append("JOB_NAME")

        field_names = {field.name for field in fields(cls)}

        params.extend(field_names)

        resolved_options = getResolvedOptions(sys.argv, params)

        return cls(
            job_arguments=resolved_options,
            **{
                key: value
                for key, value in resolved_options.items()
                if key in field_names
            },
        )

    def __post_init__(self, job_arguments: dict[str, Any] | None) -> None:
        """Ensure that the job_arguments attribute is set."""
        self.job_arguments = job_arguments or {}
