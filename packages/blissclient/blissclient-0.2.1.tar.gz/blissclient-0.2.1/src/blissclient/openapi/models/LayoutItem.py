from typing import *

from pydantic import BaseModel, Field

# from .LayoutItem import LayoutItem


class LayoutItem(BaseModel):
    """
    LayoutItem model

    """

    # children: Optional[Union[List[LayoutItem], None]] = Field(alias="children", default=None)

    type: Optional[Union[str, None]] = Field(alias="type", default=None)
