"""Module providing the GlueETLJob class for handling Glue ETL jobs."""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Generic, cast

from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark import SparkContext
from typing_extensions import TypeVar

from glue_utils import BaseOptions

if TYPE_CHECKING:
    from collections.abc import Generator

    from pyspark.sql import SparkSession

T = TypeVar("T", bound=BaseOptions, default=BaseOptions)


class GlueETLJob(Generic[T]):
    """Class that handles the boilerplate setup for Glue ETL jobs."""

    options: T
    sc: SparkContext
    spark: SparkSession
    glue_context: GlueContext

    def __init__(
        self,
        options_cls: type[T | BaseOptions] = BaseOptions,
    ) -> None:
        """Initialize the GlueETLJob.

        Parameters
        ----------
        options_cls, optional
            Has to be a subclass of BaseOptions, by default BaseOptions

        """
        if not issubclass(options_cls, BaseOptions):
            msg = "options_cls must be a subclass of BaseOptions."
            raise TypeError(msg)

        self.options = cast(T, options_cls.from_resolved_options())

        job_name = self.options.job_arguments.get("JOB_NAME", "glueetl-job")

        self.sc = SparkContext.getOrCreate()
        self.glue_context = GlueContext(self.sc)
        self.spark = self.glue_context.spark_session

        self._job = Job(self.glue_context)
        self._job.init(job_name, self.options.job_arguments)

    @contextmanager
    def managed_glue_context(
        self,
        *,
        commit: bool = True,
    ) -> Generator[GlueContext, None, None]:
        """Context manager for managing the GlueContext.

        Parameters
        ----------
        commit, optional
            Whether to commit the job, by default True

        """
        yield self.glue_context
        if commit:
            self.commit()

    def commit(self) -> None:
        """Commit the Glue ETL job."""
        self._job.commit()
