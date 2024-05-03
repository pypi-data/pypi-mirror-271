from .base import Base
from ..openapi.services.Config_service import ConfigResource_get_get


class Config(Base):
    @property
    def config(self):
        """Get the current blissterm configuration"""
        return ConfigResource_get_get(api_config_override=self._api_config)
