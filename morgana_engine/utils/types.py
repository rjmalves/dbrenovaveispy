from datetime import datetime, date
from typing import Callable


def casting_functions(schema_type: str) -> Callable:
    """
    Returns a function that can be used to cast a value to
    the specified schema type.

    Args:
        schema_type (str): The type of the schema.

    Returns:
        Callable: A function that can be used to cast a value
        to the specified schema type.
    """
    type_mappings: dict[str, Callable] = {
        "int": int,
        "float": float,
        "string": str,
        "bool": bool,
        "date": date.fromisoformat,
        "datetime": datetime.fromisoformat,
    }
    return type_mappings.get(schema_type, lambda x: x)
