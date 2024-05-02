from jsonschema.exceptions import ValidationError

from .registry import FilterValidatorRegistry


@FilterValidatorRegistry.register
def nequals(validator, value, instance, schema):
    """
    Check if the passed value not equals to the expected value
    """
    if not isinstance(value, type(instance)):
        yield ValidationError("Type mismatch")
    if value == instance:
        yield ValidationError(
            f"Values are equal. Input value should not match {instance}"
        )
