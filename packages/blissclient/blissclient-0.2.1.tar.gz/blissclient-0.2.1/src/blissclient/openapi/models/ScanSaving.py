from typing import *

from pydantic import BaseModel, Field


class ScanSaving(BaseModel):
    """
    ScanSaving model

    """

    base_path: str = Field(alias="base_path")

    beamline: Optional[Union[str, None]] = Field(alias="beamline", default=None)

    collection_name: Optional[Union[str, None]] = Field(
        alias="collection_name", default=None
    )

    data_filename: Optional[Union[str, None]] = Field(
        alias="data_filename", default=None
    )

    data_path: str = Field(alias="data_path")

    dataset_name: Optional[Union[str, None]] = Field(alias="dataset_name", default=None)

    filename: str = Field(alias="filename")

    proposal_name: Optional[Union[str, None]] = Field(
        alias="proposal_name", default=None
    )

    root_path: str = Field(alias="root_path")

    template: Optional[Union[str, None]] = Field(alias="template", default=None)
