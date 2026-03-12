class ValidationError(BaseException):
    """Base class for validation errors."""

class SchemaValidationError(ValidationError):
    """Raised when dataframe schema doesn't match requiered schema."""

class TypeValidationError(ValidationError):
    """Raised when Candle object's attribute has invalid type"""

class PriceLogicValidationError(ValidationError):
    """Raised when candle prices (ohlcv) isn't logical (ex. low > high)"""