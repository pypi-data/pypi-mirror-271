from typing import *

from pydantic import BaseModel, Field


class CallFunctionResponse(BaseModel):
    """
    CallFunctionResponse model

    """

    call_id: Optional[Union[str, None]] = Field(alias="call_id", default=None)

    return_value: Any = Field(alias="return_value")
