# Extended JSON Encoder

The `json-advanced` is Python package provides an extended JSON encoder class, `JSONSerializer`, that enables encoding of complex Python data types such as `datetime.datetime`, `datetime.date`, `datetime.time`, `bytes` and `uuid`. It also supports objects that have a `to_json` method, allowing for customizable JSON encoding.

## Features

- **Datetime Handling**: Automatically converts `datetime.datetime`, `datetime.date`, and `datetime.time` objects to their string representation.
- **UUID Encoding**: Encodes `uuid` objects as uuid strings.
- **Bytes Encoding**: Encodes `bytes` objects as base64 strings, prefixed with `b64:`.
- **Custom Object Support**: Encodes any object that has a `to_json` method by calling that method.

## Installation

You can install the package directly from source:

```bash
pip install json-advanced
```

## Usage
To use the JSONSerializer in your project, you need to import it and use it with the standard json module's dump or dumps functions:

```python
import json
import datetime
import uuid

from json_advanced.json_encoder import JSONSerializer

# Example object containing various complex data types
data = {
    "now": datetime.datetime.now(),
    "today": datetime.date.today(),
    "time": datetime.datetime.now().time(),
    "bytes_data": b"example bytes",
    "uuid": uuid.uuid4(),
}

# Serialize the object to a JSON string
json_string = json.dumps(data, cls=JSONSerializer)
print(json_string)
```

## Extending the Serializer
If you have custom types that you want to serialize, you can extend JSONSerializer by overriding the default method. Ensure you call super().default(obj) for types you do not handle:

```python
class MyCustomSerializer(JSONSerializer):
    def default(self, obj):
        if isinstance(obj, MyCustomType):
            return obj.custom_serialize()
        return super().default(obj)
```

## Contributions
Contributions are welcome! Please open an issue or pull request on GitHub if you have suggestions or improvements.

## License
This package is licensed under the MIT License - see the LICENSE file for details.