from typing import *

from pydantic import BaseModel, Field


class SetObjectProperty(BaseModel):
    """
    SetObjectProperty model

    """

    property: str = Field(alias="property")

    value: Any = Field(alias="value")
