from typing import *

from pydantic import BaseModel, Field


class CallFunction(BaseModel):
    """
    CallFunction model

    """

    args: Optional[Union[List[Any], None]] = Field(alias="args", default=None)

    call_async: Optional[Union[bool, None]] = Field(alias="call_async", default=None)

    function: str = Field(alias="function")

    kwargs: Optional[Union[Dict[str, Any], None]] = Field(alias="kwargs", default=None)

    object: Optional[Union[str, None]] = Field(alias="object", default=None)
