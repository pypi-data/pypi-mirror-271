import json
import base64
from typing import List, Any


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode()

        return super().default(obj)


def is_base64(s):
    try:
        if base64.b64encode(base64.b64decode(s)) == s.encode():
            return True
    except Exception:
        return False


def bytes_object_hook(self, keys: List[str], obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and is_base64(value):
                try:
                    obj[key] = base64.b64decode(value)
                except Exception:
                    pass
    return obj


def bytes_to_base64(obj: Any):
    if not isinstance(obj, dict):
        return obj

    for key, value in obj.items():
        if isinstance(value, bytes):
            obj[key] = base64.b64encode(value).decode()
        elif isinstance(value, dict):
            obj[key] = bytes_to_base64(value)
        elif isinstance(value, list):
            obj[key] = [bytes_to_base64(v) for v in value]

    return obj


def base64_to_bytes(obj: Any):
    if not isinstance(obj, dict):
        return obj

    for key, value in obj.items():
        if isinstance(value, str) and is_base64(value):
            try:
                obj[key] = base64.b64decode(value)
            except Exception:
                pass
        elif isinstance(value, dict):
            obj[key] = base64_to_bytes(value)
        elif isinstance(value, list):
            obj[key] = [base64_to_bytes(v) for v in value]

    return obj
