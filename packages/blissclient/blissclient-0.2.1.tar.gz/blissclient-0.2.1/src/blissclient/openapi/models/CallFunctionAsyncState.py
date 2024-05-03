from typing import *

from pydantic import BaseModel, Field


class CallFunctionAsyncState(BaseModel):
    """
    CallFunctionAsyncState model

    """

    call_id: Optional[Union[str, None]] = Field(alias="call_id", default=None)

    return_value: Optional[Union[Any, None]] = Field(alias="return_value", default=None)

    state: Union[Any, Any] = Field(alias="state")
