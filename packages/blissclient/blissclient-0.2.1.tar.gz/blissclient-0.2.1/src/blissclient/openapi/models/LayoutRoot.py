from typing import *

from pydantic import BaseModel, Field

from .LayoutItem import LayoutItem


class LayoutRoot(BaseModel):
    """
    LayoutRoot model

    """

    acronym: str = Field(alias="acronym")

    children: List[LayoutItem] = Field(alias="children")

    icon: Optional[Union[str, None]] = Field(alias="icon", default=None)

    name: str = Field(alias="name")
