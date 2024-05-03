from typing import *

from pydantic import BaseModel, Field


class ActiveMG(BaseModel):
    """
    ActiveMG model

    """

    available: List[str] = Field(alias="available")

    disabled: List[str] = Field(alias="disabled")

    enabled: List[str] = Field(alias="enabled")

    session_name: str = Field(alias="session_name")
