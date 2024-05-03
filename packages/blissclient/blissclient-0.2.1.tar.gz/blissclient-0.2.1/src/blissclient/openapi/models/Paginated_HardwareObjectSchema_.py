from typing import *

from pydantic import BaseModel, Field

from .HardwareObjectSchema import HardwareObjectSchema


class Paginated_HardwareObjectSchema_(BaseModel):
    """
    Paginated&lt;HardwareObjectSchema&gt; model

    """

    limit: Optional[Union[int, None]] = Field(alias="limit", default=None)

    results: List[HardwareObjectSchema] = Field(alias="results")

    skip: Optional[Union[int, None]] = Field(alias="skip", default=None)

    total: int = Field(alias="total")
