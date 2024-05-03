import time
import pytest

from blissclient import BlissClient, Session
from blissclient.exceptions import (
    BlissRESTError,
    BlissRESTException,
    BlissRESTNotFound,
)


def test_client_session(test_session: Session):
    print(test_session.scan_saving)
    print(test_session.scan_saving.base_path)


def test_client_session_function_non_existant(test_session: Session):
    with pytest.raises(BlissRESTNotFound):
        test_session.call("test")


def test_client_session_scan(test_session: Session):
    resp = test_session.call("ascan", "$omega", 0, 5, 5, 0.2, "$diode")
    assert resp["name"] == "ascan"


def test_client_session_async(test_session: Session):
    call_id = test_session.call(
        "ascan", "$omega", 0, 5, 5, 0.2, "$diode", call_async=True
    )
    while True:
        response = test_session.state(call_id=call_id)
        if response.state == "terminated":
            assert response.return_value["name"] == "ascan"
            break
        time.sleep(1)


def test_client_session_async_kill(test_session: Session):
    call_id = test_session.call(
        "ascan", "$omega", 0, 10, 10, 0.1, "$diode", call_async=True
    )
    time.sleep(2)
    response = test_session.kill(call_id=call_id)
    assert response is True

    # The scan was killed so its return value is an exception
    with pytest.raises(BlissRESTException):
        response = test_session.state(call_id=call_id)
        print("return", response.return_value)


def test_client_session_non_existant(blissclient: BlissClient):
    with pytest.raises(BlissRESTError):
        session = blissclient.session("moo")
        session.scan_saving
