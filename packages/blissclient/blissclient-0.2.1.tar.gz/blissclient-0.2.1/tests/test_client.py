from blissclient import BlissClient


def test_client_config(blissclient: BlissClient):
    assert "test_session" in blissclient.sessions
