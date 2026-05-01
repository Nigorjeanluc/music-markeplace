import uuid
from typing import Optional, Any

def is_valid_uuid(val: Any) -> bool:
    """Check if a value is a valid UUID (string or UUID object)."""
    try:
        if isinstance(val, uuid.UUID):
            return True
        uuid.UUID(str(val))
        return True
    except (ValueError, AttributeError):
        return False

def validate_uuid_or_return_none(val: str) -> Optional[str]:
    """Return the value if valid UUID, else None."""
    return val if is_valid_uuid(val) else None
