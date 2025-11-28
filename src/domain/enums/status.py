"""
Status - enum generico de status
"""

from enum import Enum


class Status(str, Enum):
    """status generico para entidades"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"

