# Claude Code Quickstart

## Create directory

```shell 
mkdir claude-quickstart-py
cd claude-quickstart-py
```

---
## Create and start virtual env

```shell
python3 -m venv .venv 
source .venv/bin/activate  
```

---
## Create project

### Project Structure
```shell
.
├── src/
│   ├── __init__.py
│   └── app.py
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── .venv
└── .python-version
```

___
## Create `src/app.py`

```python
import json
from typing import Dict


def greet(name: str) -> Dict[str, str]:
    """Return a small JSON-serializable greeting payload."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    return {"ok": "True", "message": f"Hello, {name.strip()}!"}


if __name__ == "__main__":
    import sys

    arg = sys.argv[1] if len(sys.argv) > 1 else "Developer"
    print(json.dumps(greet(arg)))
```

---
## Create `tests/test_app.py`

```python
import unittest
from src.app import greet


class TestApp(unittest.TestCase):

    def test_greet_happy_path(self):
        result = greet("Alice")
        self.assertTrue(result["ok"])

    def test_greet_strips_whitespace(self):
        result = greet("Bob")
        self.assertEqual(result["message"], "Hello, Bob!")

    def test_greet_rejects_empty(self):
        with self.assertRaises(ValueError):
            greet(" ")


if __name__ == "__main__":
    unittest.main()
```

---
## Run app

```shell
python src/app Alice
```

---
## Run tests

```shell
python -m unittest
```


