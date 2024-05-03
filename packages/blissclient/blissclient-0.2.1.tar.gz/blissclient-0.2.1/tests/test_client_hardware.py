import pytest
from blissclient import HardwareObject, BlissClient
from blissclient.exceptions import BlissRESTError, BlissRESTValidationError
from pydantic import ValidationError


def test_client_hardware(omega: HardwareObject):
    omega.move(5)
    omega.wait()
    omega.move(10)
    omega.wait()
    assert omega.position == 10

    omega.velocity = 5
    omega.velocity = 5000
    assert omega.velocity == 5000


def test_client_hardware_422(omega: HardwareObject):
    with pytest.raises(BlissRESTValidationError):
        omega.move("string")


def test_client_hardware_404(omega: HardwareObject):
    with pytest.raises(ValidationError):
        omega._call(123, 123)


def test_client_hardware_missing(blissclient: BlissClient):
    with pytest.raises(KeyError):
        blissclient.hardware.get("missing")
