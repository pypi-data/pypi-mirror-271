from typing import *

from pydantic import BaseModel, Field


class RegisterHardwareSchema(BaseModel):
    """
    RegisterHardwareSchema model

    """

    ids: List[str] = Field(alias="ids")
