from pydantic import BaseModel, ValidationError
from typing import Any, Type, TypeVar

T = TypeVar('T')

def validate(value: Any, data_type: Type[T]) -> T:
    """
    A function to validate the type of a value using Pydantic.

    Example:
        ```python
        import zyx

        validated_int = zyx.validate(42, int)
        print(f"Validated integer: {validated_int}")
        ```

    Args:
        value (Any): The value to validate.
        data_type (Type[T]): The type to validate the value against.
    """

    if not value:
        raise ValueError("Value is required!")

    class InputModel(BaseModel):
        data: data_type
    try:
        model = InputModel(data=value)
        return model.data
    except ValidationError as e:
        raise ValueError(f"Validation failed: {str(e)}")
    
if __name__ == "__main__":
    try:
        # Validate an integer
        validated_int = validate(42, int)
        print(f"Validated integer: {validated_int}")

        # Validate a string
        validated_str = validate("Hello, Pydantic!", str)
        print(f"Validated string: {validated_str}")

        # Validate a float
        validated_float = validate(3.14, float)
        print(f"Validated float: {validated_float}")

        # Validate a boolean
        validated_bool = validate(True, bool)
        print(f"Validated boolean: {validated_bool}")

        # Validate a list of integers
        validated_list = validate([1, 2, 3], list[int])
        print(f"Validated list: {validated_list}")

        # Validate an invalid input
        validated_invalid = validate("Not an integer", int)
    except ValueError as e:
        print(f"Validation error: {str(e)}")
