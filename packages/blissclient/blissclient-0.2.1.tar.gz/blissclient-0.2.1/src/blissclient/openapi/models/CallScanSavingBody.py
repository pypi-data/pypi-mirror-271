from typing import *

from pydantic import BaseModel, Field


class CallScanSavingBody(BaseModel):
    """
    CallScanSavingBody model

    """

    function: Any = Field(alias="function")
