import base64
import datetime
import json
import re
import uuid
from functools import partial


class JSONSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S.%f")
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, bytes):
            return f'b64:{base64.b64encode(obj).decode("utf-8")}'
        if hasattr(obj, "to_json"):
            return obj.to_json()
        return super().default(obj)


def json_deserializer(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            # Base64 decoding
            if value.startswith("b64:"):
                base64_str = value[4:]  # Remove the 'b64:' prefix
                try:
                    dct[key] = base64.b64decode(base64_str)
                except (ValueError, TypeError):
                    pass

            # UUID conversion
            if re.match(
                r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
                value,
            ):
                try:
                    dct[key] = uuid.UUID(value)
                except ValueError:
                    pass

            # Datetime conversion
            datetime_patterns = [
                (
                    r"^(\d{2,4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}(\.\d+))$",
                    "%Y-%m-%d %H:%M:%S.%f",
                    lambda dt: dt,
                ),
                (
                    r"^(\d{2,4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$",
                    "%Y-%m-%d %H:%M:%S",
                    lambda dt: dt,
                ),
                (r"^(\d{2,4}-\d{2}-\d{2})$", "%Y-%m-%d", lambda dt: dt.date()),
                (
                    r"^(\d{2}:\d{2}:\d{2}(\.\d+))$",
                    "%H:%M:%S.%f",
                    lambda dt: dt.time(),
                ),
                (r"^(\d{2}:\d{2}:\d{2})$", "%H:%M:%S", lambda dt: dt.time()),
            ]

            for reg, pattern, formatter in datetime_patterns:
                if re.match(reg, value):
                    try:
                        dt = datetime.datetime.strptime(value, pattern)
                        dct[key] = formatter(dt)
                        break  # Exit loop after successful conversion
                    except ValueError:
                        continue  # Try next pattern

    return dct


dumps = partial(json.dumps, cls=JSONSerializer)
loads = partial(json.loads, object_hook=json_deserializer)
dump = partial(json.dump, cls=JSONSerializer)
load = partial(json.load, object_hook=json_deserializer)
