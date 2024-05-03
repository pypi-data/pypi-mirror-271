from typing import *

from pydantic import BaseModel, Field


class UpdateScanSavingBody(BaseModel):
    """
    UpdateScanSavingBody model

    """

    collection_name: Optional[Union[str, None]] = Field(
        alias="collection_name", default=None
    )

    data_filename: Optional[Union[str, None]] = Field(
        alias="data_filename", default=None
    )

    dataset_name: Optional[Union[str, None]] = Field(alias="dataset_name", default=None)

    proposal_name: Optional[Union[str, None]] = Field(
        alias="proposal_name", default=None
    )

    template: Optional[Union[str, None]] = Field(alias="template", default=None)
