import os

from .high_level.config import Config
from .high_level.session import Session
from .high_level.hardware import Hardware


class BlissClient:
    def __init__(self):
        self._hardware = Hardware()
        self._config = Config()

    def __str__(self):
        return f"BlissClient: {self.url}\n  Beamline: {self.beamline}\n  Sessions: {', '.join(self.sessions)}"

    @property
    def url(self):
        return os.environ["BLISSTERM_URL"]

    @property
    def config(self):
        return self._config.config

    @property
    def beamline(self):
        return self.config.beamline

    @property
    def sessions(self):
        return self.config.sessions

    @property
    def hardware(self):
        return self._hardware

    def session(self, session_name: str):
        return Session(session_name=session_name)
