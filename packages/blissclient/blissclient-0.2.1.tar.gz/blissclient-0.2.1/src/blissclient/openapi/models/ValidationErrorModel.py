from typing import *

from pydantic import BaseModel, Field


class ValidationErrorModel(BaseModel):
    """
    ValidationErrorModel model

    """

    ctx: Optional[Union[Dict[str, Any], None]] = Field(alias="ctx", default=None)

    loc: Optional[Union[List[str], None]] = Field(alias="loc", default=None)

    msg: Optional[Union[str, None]] = Field(alias="msg", default=None)

    type_: Optional[Union[str, None]] = Field(alias="type_", default=None)
