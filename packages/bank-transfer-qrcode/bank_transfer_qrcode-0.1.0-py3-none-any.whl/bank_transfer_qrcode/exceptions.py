# pylint: disable=R0903,C0114


class BaseValidationError(Exception):
    """
    Base Exception for validation errors that may occur.
    """


class IBANValidationError(BaseValidationError):
    """
    Raised when the IBAN validation fails. 
    Can be a type, pattern or value validation error.
    """


class RecipientNameValidationError(BaseValidationError):
    """
    Raised when the Recipient Name validation fails. 
    Can be a type, pattern or value validation error.
    """


class AmountValidationError(BaseValidationError):
    """
    Raised when the Amount validation fails. 
    Can be a type, pattern or value validation error.
    """


class CountryCodeValidationError(BaseValidationError):
    """
    Raised when the Country Code validation fails. 
    Can be a type, pattern or value validation error.
    """


class TransferTitleValidationError(BaseValidationError):
    """
    Raised when the Transfer Title validation fails. 
    Can be a type, pattern or value validation error.
    """


class RecipientIdentifierValidationError(BaseValidationError):
    """
    Raised when the Recipient Identifier validation fails. 
    Can be a type, pattern or value validation error.
    """


class QRTextValidationError(BaseValidationError):
    """
    Raised when the QR text is invalid i.e. total length exceeded.
    """