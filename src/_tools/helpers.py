import re
import uuid


def create_uuid_str():
    return f"{uuid.uuid4()}"


class TranscriptionDataError(Exception):
    """A base class for all business rule validation exceptions"""


class ValueObject:
    """A base class for all value objects"""


def split_list_values(field_value: str) -> list[str]:
    """Utility method to split a field value by commas and strip whitespace, and remove surrounding quotes."""
    return [re.sub(r'"', "", item).strip() for item in re.split(r"; *", field_value) if item != "*"]

