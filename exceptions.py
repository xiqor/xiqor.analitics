class ValidationError:
    """Base class for validation errors."""
    pass

class SchemaValidationError(ValidationError):
    """Raised when dataframe schema doesn't match requiered schema."""