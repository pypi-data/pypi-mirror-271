from jsonschema.exceptions import ValidationError

from .registry import FilterValidatorRegistry


@FilterValidatorRegistry.register
def iequals(validator, value, instance, schema):
    """
    Check if the passed value equals to the expected value
    This check is case insensitive
    """
    if "type" in schema and schema["type"] != "string":
        yield ValidationError("iequals only works for type string")
    if not isinstance(value, str) or not isinstance(instance, str):
        yield ValidationError("iequals only works for type string")
    if not isinstance(value, type(instance)):
        yield ValidationError("Type mismatch")
    if str(value).lower() != str(instance).lower():
        yield ValidationError(f"Values not equal. Expected: {value}, Found: {instance}")
