from jsonschema.exceptions import ValidationError

from .registry import FilterValidatorRegistry


@FilterValidatorRegistry.register
def equals(validator, value, instance, schema):
    """
    Check if the passed value equals to the expected value
    """
    if not isinstance(value, type(instance)):
        yield ValidationError("Type mismatch")
    if value != instance:
        yield ValidationError(f"Values not equal. Expected: {value}, Found: {instance}")
