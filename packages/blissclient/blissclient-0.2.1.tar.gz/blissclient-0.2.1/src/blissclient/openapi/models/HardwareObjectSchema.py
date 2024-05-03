from typing import *

from pydantic import BaseModel, Field


class HardwareObjectSchema(BaseModel):
    """
    HardwareObjectSchema model

    """

    alias: Optional[Union[str, None]] = Field(alias="alias", default=None)

    callables: List[str] = Field(alias="callables")

    errors: List[Dict[str, Any]] = Field(alias="errors")

    id: str = Field(alias="id")

    name: str = Field(alias="name")

    online: bool = Field(alias="online")

    properties: Dict[str, Any] = Field(alias="properties")

    type: str = Field(alias="type")
