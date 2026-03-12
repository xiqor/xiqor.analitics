class ValidationError:
    """Base class for validation errors."""

class SchemaValidationError(ValidationError):
    """Raised when dataframe schema doesn't match requiered schema."""

class PriceLogicValidationError(ValidationError):
    """Raised when candle prices (ohlcv) isn't logical (ex. low > high)"""