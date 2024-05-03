from typing import *

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    ErrorResponse model

    """

    error: str = Field(alias="error")
