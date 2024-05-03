from typing import *

from pydantic import BaseModel, Field


class CallObjectFunctionResponse(BaseModel):
    """
    CallObjectFunctionResponse model

    """

    function: str = Field(alias="function")

    response: Any = Field(alias="response")

    value: Optional[Union[Any, None]] = Field(alias="value", default=None)
