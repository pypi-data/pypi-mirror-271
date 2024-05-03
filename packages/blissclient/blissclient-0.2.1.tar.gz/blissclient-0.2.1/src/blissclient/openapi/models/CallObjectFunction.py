from typing import *

from pydantic import BaseModel, Field


class CallObjectFunction(BaseModel):
    """
    CallObjectFunction model

    """

    function: str = Field(alias="function")

    value: Optional[Union[Any, None]] = Field(alias="value", default=None)
