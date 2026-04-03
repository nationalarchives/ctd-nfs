import uuid


def create_uuid_str():
    return f"{uuid.uuid4()}"


class BusinessRuleValidationException(Exception):
    """A base class for all business rule validation exceptions"""


class ValueObject:
    """A base class for all value objects"""

