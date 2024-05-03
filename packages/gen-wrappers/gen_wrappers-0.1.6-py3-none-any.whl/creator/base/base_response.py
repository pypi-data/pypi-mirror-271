from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel

from creator.base.job_status import JobStatus


class ResponseDataType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"
    AUDIO = "audio"


class ResponseData(BaseModel):
    data: List[Any]
    data_type: ResponseDataType
    total_count: int


class BaseResponse(BaseModel):
    status: JobStatus = JobStatus.PENDING
    output: Optional[ResponseData] = None
    error_msg: Optional[str] = None
    job_id: Optional[str] = None

    # Override Pydantic's dict method to exclude methods
    def dict(self, **kwargs):
        return super().dict(
            **kwargs,
            exclude={
                "parse_response",
                "success",
                "error"
            }
        )

    @classmethod
    def parse_response(cls, response: dict):
        """Parse the response from the API."""
        return cls(**response)

    @classmethod
    def success(cls, data: ResponseData):
        """Return a successful response."""
        return cls(status=JobStatus.FINISHED, output=data)

    @classmethod
    def active(cls):
        return cls(status=JobStatus.READY)

    @classmethod
    def running(cls, job_id: str):
        """Return a pending response."""
        return cls(status=JobStatus.RUNNING, job_id=job_id)

    @classmethod
    def error(cls, error: str):
        """Return an error response."""
        return cls(status=JobStatus.FAILED, error_msg=error)
