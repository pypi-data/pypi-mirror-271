from typing import List, Dict, Union


class ExtractionError(Exception):
    """ An exception that occurs when an anomaly occurs during the extraction process. """


class AccessError(ExtractionError):
    """ """
    def __init__(self, *, data: Union[List, Dict], prefix: str = "") -> None:
        if isinstance(data, dict):
            msg = (
                f"No registered structure key found in the specified dictionary. "
                f"Keys found: {data.keys()}."
            )
        elif isinstance(data, list):
            msg = (
                f"No value at the specified index. List length: {len(data)}"
            )
        else:
            raise TypeError(
                f"Invalid input type: {type(data)}. "
                "Expected input type: Union[Dict, List]."
            )
        super().__init__(f"{prefix}{msg}")


class ErrorWrapper(Exception):
    """ """
    def __init__(self, exception: Exception) -> None:
        super().__init__(
            f"{exception.__class__.__name__}" 
            f": {exception.args[0]}" if exception.args[0] else ""
        )
