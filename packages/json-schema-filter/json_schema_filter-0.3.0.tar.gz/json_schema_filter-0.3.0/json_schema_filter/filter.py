from typing import Dict, List, Union

from jsonschema import validators
from jsonschema.validators import Draft202012Validator

from .filter_validator import FilterValidatorRegistry
from .struct import FilterResult, Rejected, Selected


class JsonSchemaFilter:
    """
    JSON Schema Entry Class

    :param schema: input schema for the filter
    :param schema_version: Draft version to use for validations.
                           Default: Draft202012Validator

    :returns: CustomValidator class with filter
    """

    def __init__(
        self, schema: Dict, schema_version=Draft202012Validator
    ) -> "JsonSchemaFilter":
        all_validators = dict(schema_version.VALIDATORS)
        all_validators.update(FilterValidatorRegistry.registered_validators)
        CustomValidator = validators.create(
            meta_schema=schema_version.META_SCHEMA, validators=all_validators
        )
        self._validator: schema_version = CustomValidator(schema=schema)

    def filter(self, input_data: Union[List, Dict]) -> FilterResult:
        """
        Filter the input based on the schema provided

        :param input_data: Dict or List of Dict to process

        :returns: FilterResult class obj
        """
        if not isinstance(input_data, list):
            input_data = [input_data]
        filter_result_obj = FilterResult(selected=[], rejected=[])
        for idx, data in enumerate(input_data):
            errors = self._validator.iter_errors(data)
            is_match = True
            messages = []
            for inner_idx, err in enumerate(errors):
                path = "->".join(err.json_path.split(".")[1:])
                messages.append(f"{inner_idx+1}. {path}: {err.message}")
                is_match = False
            if not is_match:
                filter_result_obj.rejected.append(
                    Rejected(idx=idx, item=data, reasons=messages)
                )
            else:
                filter_result_obj.selected.append(Selected(idx=idx, item=data))
        return filter_result_obj
