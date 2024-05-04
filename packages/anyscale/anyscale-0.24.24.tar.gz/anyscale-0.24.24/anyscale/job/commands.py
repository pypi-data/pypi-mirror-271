from typing import Optional

from anyscale._private.sdk import sdk_command
from anyscale.job._private.job_sdk import JobSDK
from anyscale.job.models import JobConfig


_JOB_SDK_SINGLETON_KEY = "job_sdk"

_SUBMIT_EXAMPLE = """\
import anyscale
from anyscale.job.models import JobConfig

anyscale.job.submit(
    JobConfig(
        name="my-job",
        entrypoint="python main.py",
        working_dir=".",
    ),
)
"""


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    JobSDK,
    doc_py_example=_SUBMIT_EXAMPLE,
    arg_docstrings={"config": "The config options defining the job.",},
)
def submit(config: JobConfig, *, _sdk: JobSDK) -> str:
    """Submit a job."""
    return _sdk.submit(config)


_STATUS_EXAMPLE = """\
import anyscale
from anyscale.job.models import JobStatus

status: JobStatus = anyscale.job.status(name="my-job")"""


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    JobSDK,
    doc_py_example=_STATUS_EXAMPLE,
    arg_docstrings={"name": "Name of the job.", "job_id": "Unique ID of the job"},
)
def status(
    name: Optional[str] = None, job_id: Optional[str] = None, *, _sdk: JobSDK
) -> str:
    """Get the status of a job."""
    return _sdk.status(name=name, job_id=job_id)


_TERMINATE_EXAMPLE = """\
import anyscale

anyscale.job.terminate(name="my-job")"""


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    JobSDK,
    doc_py_example=_TERMINATE_EXAMPLE,
    arg_docstrings={"name": "Name of the job.", "job_id": "Unique ID of the job"},
)
def terminate(
    name: Optional[str] = None, job_id: Optional[str] = None, *, _sdk: JobSDK
) -> str:
    """Get the status of a job."""
    return _sdk.terminate(name=name, job_id=job_id)


_ARCHIVE_EXAMPLE = """\
import anyscale

anyscale.job.archive(name="my-job")"""


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    JobSDK,
    doc_py_example=_ARCHIVE_EXAMPLE,
    arg_docstrings={"name": "Name of the job.", "job_id": "Unique ID of the job"},
)
def archive(
    name: Optional[str] = None, job_id: Optional[str] = None, *, _sdk: JobSDK
) -> str:
    """Get the status of a job."""
    return _sdk.archive(name=name, job_id=job_id)
