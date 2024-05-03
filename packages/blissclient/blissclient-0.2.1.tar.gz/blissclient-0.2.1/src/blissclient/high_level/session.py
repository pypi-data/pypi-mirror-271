from collections import deque
import os
from typing import Any

from .base import Base
from .scan import Scan
from ..openapi.models.CallFunction import CallFunction
from ..openapi.models.UpdateScanSavingBody import UpdateScanSavingBody
from ..openapi.models.ScanSaving import ScanSaving
from ..openapi.models.CallScanSavingBody import CallScanSavingBody
from ..openapi.services.Session_service import (
    CallFunctionResource_post__session_name__call_post,
    CallFunctionStateResource_get__session_name__call__call_id__get,
    CallFunctionStateResource_delete__session_name__call__call_id__delete,
    ScanSavingResource_get__session_name__scan_saving_get,
    ScanSavingResource_patch__session_name__scan_saving_patch,
    ScanSavingResource_post__session_name__scan_saving_post,
)


class Session(Base):
    def __init__(self, session_name: str):
        self._data_store = None
        self._scans = deque([], 10)
        self._session_name = session_name
        super().__init__()

    def load_scan(self, key: str, wrapped: bool = True):
        """Load a bliss scan from its blissdata redis key

        Args:
            wrapped: whether the scan is wrapped in a helper class"""
        try:
            if self._data_store is None:
                from blissdata.redis_engine.store import DataStore

                self._data_store = DataStore(
                    os.environ.get(
                        "BLISSDATA_URL",
                        os.environ["BLISSTERM_URL"]
                        .replace("http://", "redis://")
                        .replace(":5000", ":6380"),
                    )
                )

            for scan in self._scans:
                if scan.key == key:
                    return scan

            scan = self._data_store.load_scan(key)
            if wrapped:
                scan = Scan(scan)
                self._scans.append(scan)
            return scan
        except Exception as e:
            print("Could not autoload bliss scan")
            print(e)

    def _potentially_load_scan_from_return(self, return_value: Any):
        if isinstance(return_value, dict):
            if "type" in return_value:
                if (
                    return_value["type"] == "bliss.scanning.scan.Scan"
                    and "key" in return_value
                ):
                    self.load_scan(return_value["key"])

    def __str__(self):
        return f"Session: {self.session_name}"

    @property
    def session_name(self):
        """The current session name"""
        return self._session_name

    def call(
        self,
        function: str,
        *args,
        call_async: bool = False,
        object_name: str = None,
        **kwargs,
    ):
        """Call a function in the session

        Kwargs:
            call_async: Allows the function to be called asynchronously
            object_name: Call a function on an object

        Returns:
            If `call_async` is `false`, returns the function return value
            If `call_async` is `true`, returns the `call_id` uuid
        """
        response = CallFunctionResource_post__session_name__call_post(
            self._session_name,
            CallFunction(
                call_async=call_async,
                function=function,
                args=args,
                kwargs=kwargs,
                object=object_name,
            ),
            api_config_override=self._api_config,
        )

        if call_async:
            return response.call_id
        else:
            self._potentially_load_scan_from_return(response.return_value)
            return response.return_value

    def state(self, call_id: str):
        """Get the state of a function call from its `call_id`"""
        state = CallFunctionStateResource_get__session_name__call__call_id__get(
            self._session_name,
            call_id=call_id,
            api_config_override=self._api_config,
        )

        self._potentially_load_scan_from_return(state.return_value)
        return state

    def kill(self, call_id: str):
        """Kill a currently asynchronously running function from its `call_id`"""
        CallFunctionStateResource_delete__session_name__call__call_id__delete(
            self._session_name, call_id=call_id, api_config_override=self._api_config
        )
        return True

    @property
    def scans(self):
        """Get the current list of scans retrieved from the session"""
        return self._scans

    @property
    def scan_saving(self):
        """Get the current `SCAN_SAVING` configuration"""

        class ScanSavingRepr(ScanSaving):
            def __str__(self):
                return "Scan Saving:\n" + "\n".join(
                    [f"  {field}:\t{value}" for field, value in self]
                )

        scan_saving = ScanSavingResource_get__session_name__scan_saving_get(
            self._session_name, api_config_override=self._api_config
        )
        return ScanSavingRepr(**scan_saving.dict())

    def update_scan_saving(self, **kwargs):
        """Update a `SCAN_SAVING property"""
        return ScanSavingResource_patch__session_name__scan_saving_patch(
            self._session_name,
            data=UpdateScanSavingBody(**kwargs),
            api_config_override=self._api_config,
        )

    def call_scan_saving(self, function: str):
        """Call a `SCAN_SAVING` function"""
        return ScanSavingResource_post__session_name__scan_saving_post(
            self._session_name,
            data=CallScanSavingBody(function=function),
            api_config_override=self._api_config,
        )
