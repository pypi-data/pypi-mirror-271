import base64
from enum import Enum
from typing import List, Optional, Any
from fastapi.responses import Response

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

    def image_response(self):
        """Return a response containing images if output is image data."""
        if self.output and self.output.data_type == ResponseDataType.IMAGE:
            image_data_list = self.output.data
            if len(image_data_list) == 1:
                # If only one image, return a single image response
                image_data = image_data_list[0]
                return Response(content=image_data, media_type="image/png")
            else:
                # If multiple images, construct a multipart response
                boundary = "boundary_separator"
                content_type = f"multipart/mixed; boundary={boundary}"
                body_parts = []
                for image_data in image_data_list:
                    image_part = (
                        f"\r\n--{boundary}\r\n"
                        f"Content-Type: image/png\r\n"
                        f"Content-Length: {len(image_data)}\r\n\r\n"
                        f"{image_data}\r\n"
                    )
                    body_parts.append(image_part)
                body = "".join(body_parts)
                return Response(content=body, media_type=content_type)
        else:
            return self
