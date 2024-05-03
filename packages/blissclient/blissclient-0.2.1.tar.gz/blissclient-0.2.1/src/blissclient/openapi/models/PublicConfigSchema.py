from typing import *

from pydantic import BaseModel, Field

from .LayoutItem import LayoutItem
from .LayoutRoot import LayoutRoot
from .MonitorConfigSchema import MonitorConfigSchema


class PublicConfigSchema(BaseModel):
    """
    PublicConfigSchema model

    """

    activeSessions: List[str] = Field(alias="activeSessions")

    beamline: Optional[Union[str, None]] = Field(alias="beamline", default=None)

    layouts: List[LayoutRoot] = Field(alias="layouts")

    monitor: List[MonitorConfigSchema] = Field(alias="monitor")

    sessions: List[str] = Field(alias="sessions")

    sideItems: List[LayoutItem] = Field(alias="sideItems")

    topItems: List[LayoutItem] = Field(alias="topItems")
