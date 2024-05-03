from typing import *

from pydantic import BaseModel, Field


class TerminalSizeBody(BaseModel):
    """
    TerminalSizeBody model

    """

    h: int = Field(alias="h")

    session_name: str = Field(alias="session_name")

    w: int = Field(alias="w")
