# blissclient

A python client for `blissterm`, the high-level client is fully typed ready for auto-completion in any modern IDE.


## Getting Started

Set the `BLISSTERM_URL`

```bash
export BLISSTERM_URL=http://localhost:5000
```

Then:

```python
from blissclient import BlissClient

client = BlissClient()

omega = client.hardware.get("omega")
print(omega.position)

omega.move(100)
omega.wait()

```

Execute calls in the session:

```python
from blissclient import BlissClient


client = BlissClient()
test_session = client.session("test_session")

# Blocking until the call terminates
return_value =test_session.call("ascan", "$omega", 0, 10, 10, 0.1, "$diode")
```

Strings prefixed with `$` are translated to the relevant beacon objects

Or execute asynchronously:

```python
import time
from blissclient import BlissClient

client = BlissClient()

test_session = client.session("test_session")
call_id = test_session.call("ascan", "$omega", 0, 10, 10, 0.1, "$diode", call_async=True)

while True:
    response = test_session.state(call_id=call_id)
    if response.state == "terminated":
        break
    else:
        time.sleep(1)

    print(response.return_value)

    # The redis scan key, can be used with `blissdata``
    response.return_value["key"]
```

See the test suite for more examples.
