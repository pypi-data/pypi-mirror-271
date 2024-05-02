# json-schema-filter
[![PyPI version](https://badge.fury.io/py/json-schema-filter.svg)](https://badge.fury.io/py/json-schema-filter)
![Publish](https://github.com/bharat23/json-schema-filter/actions/workflows/python-publish.yml/badge.svg)

A library that uses `jsonschema` to filter the objects

### Usage
```python
from json_schema_filter import JsonSchemaFilter

schema = {
    "properties": {
        "name": {
            "type": "string",
            "equals": "Shakespeare"
        }
    },
    "required": ["name"]
}

input_data = [
    {"name": "what is in the name"},
    {"name": "Shakespeare"},
    {"name": "hamlet"},
]

print(JsonSchemaFilter(schema).filter(input_data))

# output
"""
Total Selected: 1
Filtered Item: [0]
        1. name: Values not equal. Expected: Shakespeare, Found: what is in the name
Filtered Item: [2]
        1. name: Values not equal. Expected: Shakespeare, Found: hamlet
"""
```

### Supported additional properties
|Property|Supported type|Description|
|--------|--------------|-----------|
|equals|*|Check if value matches
|iequals|string|Check if value matches (case insensitive)
|nequals|*|Check if value does not match
