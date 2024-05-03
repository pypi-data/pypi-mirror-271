from typing import *

from pydantic import BaseModel, Field


class MonitorConfigSchema(BaseModel):
    """
    MonitorConfigSchema model

    """

    comparator: Optional[Union[str, None]] = Field(alias="comparator", default=None)

    comparison: Optional[Union[str, List[str], None]] = Field(
        alias="comparison", default=None
    )

    name: str = Field(alias="name")

    overlay: Optional[Union[str, None]] = Field(alias="overlay", default=None)

    value: str = Field(alias="value")
