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
