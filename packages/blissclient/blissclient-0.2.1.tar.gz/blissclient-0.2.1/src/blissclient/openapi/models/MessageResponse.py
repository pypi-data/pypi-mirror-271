from typing import *

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """
    MessageResponse model

    """

    message: str = Field(alias="message")
