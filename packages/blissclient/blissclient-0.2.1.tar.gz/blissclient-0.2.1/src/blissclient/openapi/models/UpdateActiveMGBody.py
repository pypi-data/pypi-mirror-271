from typing import *

from pydantic import BaseModel, Field


class UpdateActiveMGBody(BaseModel):
    """
    UpdateActiveMGBody model

    """

    disabled: Optional[Union[List[str], None]] = Field(alias="disabled", default=None)

    enabled: Optional[Union[List[str], None]] = Field(alias="enabled", default=None)
