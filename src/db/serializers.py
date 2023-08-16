from typing import List, Tuple
import re


def serialize_filter(filter) -> Tuple[str, List]:
    """We try to replace values of the filter with %s
    and extract those values into a separate list.

    Supported Formats
    - 'columA=valueA, AND columB=valueB,...'

    Args:
        filter (str): The filter to include in the where clause

    Returns:
        Tuple[str, List]: serialized data and extracted derivables
    """

    regex = r"=(\w*),"
    replacer = "=%s "
    derivables = re.findall(regex, filter)
    s_filter = re.sub(regex, replacer, filter)
    return s_filter, derivables
