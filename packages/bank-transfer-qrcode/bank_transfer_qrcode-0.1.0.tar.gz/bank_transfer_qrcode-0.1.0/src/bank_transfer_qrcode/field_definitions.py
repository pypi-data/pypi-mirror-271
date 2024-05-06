import re
from dataclasses import dataclass

from .exceptions import (
    RecipientIdentifierValidationError,
    IBANValidationError,
    CountryCodeValidationError,
    AmountValidationError,
    RecipientNameValidationError,
    TransferTitleValidationError
)


QR_TEXT_FORMAT = ('{recipient_identifier}'
            '{separator}'
            '{country_code}'
            '{separator}'
            '{iban}'
            '{separator}'
            '{amount}'
            '{separator}'
            '{recipient_name}'
            '{separator}'
            '{transfer_title}'
            '{separator}'
            '{reserve_1}'
            '{separator}'
            '{reserve_2}'
            '{separator}'
            '{reserve_3}'
)


MAX_QR_TEXT_LENGTH = 160


SEPARATOR = '|' # Not negiotiable?


# TODO: Maybe a definition should be a dataclass for readability?
@dataclass
class Field_Definition:
    required: bool
    input_types: tuple[type]
    validator: re.Pattern
    validation_exception: Exception
    transformations: list[tuple[callable, tuple[None|int|str]]]
    default: str|None
    description: str


RECIPIENT_IDENTIFIER = {
        'type_1': {
            'required': True,
            'input_types': (str, int),
            'validator': re.compile(
                r'''
                (
                    ^16\d{3} # Optional, some systems operate with 12 digit NIPs
                    |   
                    ^\d{3}     # 3 digits from the NIP
                )
                (-)?    # Separator, optional
                (\d{3}) # 3 digits from the NIP
                (-)?    # Separator, optional
                (\d{2}) # 2 digits from the NIP
                (-)?    # Separator, optional
                (\d{2}) # 2 digits from the NIP
                $
                ''',
                re.VERBOSE),
            'validation_exception': RecipientIdentifierValidationError,
            'transformations': [
                (str, tuple()),
                (str.strip, tuple()),
                (str.split, tuple()),
                (''.join, tuple())
            ],
            'default': None
        },
        'type_2': {
            'required': False,
            'input_types': (str, int),
            'validator': re.compile( # Only relevant if provided, can be empty
                r'''
                (
                    ^16\d{3} # Optional, some systems operate with 12 digit NIPs
                    |   
                    ^\d{3}     # 3 digits from the NIP
                )
                (-)?    # Separator, optional
                (\d{3}) # 3 digits from the NIP
                (-)?    # Separator, optional
                (\d{2}) # 2 digits from the NIP
                (-)?    # Separator, optional
                (\d{2}) # 2 digits from the NIP
                $
                ''',
                re.VERBOSE),
            'validation_exception': RecipientIdentifierValidationError,
            'transformations': [
                (str, tuple()),
                (str.strip, tuple()),
                (str.split, tuple()),
                (''.join, tuple())
            ],
            'default': '',
            'description': ('Recipient identifier.\n'
                            'Type 1: Institutional recipient,\n'
                            'Type 2: Individual recipient (Non-Institutional).\n'
                            'Value is always the NIP of the recipient.\n'
                            'Mandatory for type 1 recipients.\n'
                            'Optional for type 2 recipients and can be left empty.')
        },
        'description': ('Recipient identifier.\n'
                        'Type 1: Institutional recipient,\n'
                        'Type 2: Individual recipient (Non-Institutional).\n'
                        'Value is always the NIP of the recipient.\n'
                        'Mandatory for type 1 recipients.\n'
                        'Optional for type 2 recipients and can be left empty.')
}
RECIPIENT_IDENTIFIER['default'] = RECIPIENT_IDENTIFIER['type_2']


COUNTRY_CODE = {
    'required': False,
    'default': 'PL',
    'input_types': (str,),
    'validator': re.compile(r'^([a-zA-Z]{2})$'),
    'validation_exception': CountryCodeValidationError,
    'transformations': [
        (str.strip, tuple()),
        (str.split, tuple()),
        (' '.join, tuple()),
        (str.upper, tuple())
    ],
    'description': 'ISO 3166-2. Two uppercase letters country code'
}


IBAN_PL = {
    'required': True,
    'default': None,
    'input_types': (str, int),
    'validator': re.compile(r'^(PL)?([0-9]{26})$'),
    'validation_exception': IBANValidationError,
    'transformations': [
        (str, tuple()),
        (str.strip, tuple()),
        (str.split, tuple()),
        (' '.join, tuple())
    ],
    'description': ('Internatinal Banking Account Number. '
                    'This implementation is specific for Poland.\n'
                    'Other countries may require different validation patterns.\n'
                    'NOTE: Validates only one of the known IBAN formats and '
                    'is nowhere near to inclue the calulation of checksums'
                    ' or other applicable validation steps. ')
}

AMOUNT_IN_POLSKIE_GROSZE = {
    'required': True,
    'default': '000000',
    'input_types': (str, int, float),
    'validator': re.compile(r'^(\d{6})$'),
    'validation_exception': AmountValidationError,
    'transformations': [
        (str, tuple()),
        (str.strip, tuple()),
        (str.split, tuple()),
        (' '.join, tuple()),
        (str.replace, (',', '')),
        (str.replace, ('.', '')),
        (str.rjust, (6, '0'))
    ],
    'description': ('The amount to be transferred to the recipient.\n'
                    'Format is like 9999,00 but without the comma: 999900.\n'
                    'Deviates from the recommendation by NOT allowing higher '
                    'amounts than 9999,99 PLN.')
}


RECIPIENT_NAME = {
    'required': True,
    'default': None,
    'input_types': (str,),
    'validator': re.compile(r'^([\w -.,/\(\)"\']{3,20})$'),
    'validation_exception': RecipientNameValidationError,
    'transformations': [
        (str.strip, tuple()),
        (str.split, tuple()),
        (' '.join, tuple())
    ],
    'description': ('The name of the recipient. Max. length 20 characters.')
}


TRANSFER_TITLE = {
    'required': True,
    'default': None,
    'input_types': (str,),
    'validator': re.compile(r'^([\w -.,/\(\)"\']{3,32})$'),
    'validation_exception': TransferTitleValidationError,
    'transformations': [
        (str.strip, tuple()),
        (str.split, tuple()),
        (' '.join, tuple())
    ],
    'description': 'Transfer title. Max. length 32 characters.'
}


RESERVE_1 = {
    'required': True,
    'default': '',
    'input_types': (str,),
    'validator': None,
    'validation_exception': ValueError,
    'transformations': [
        (str, tuple())
    ],
    'description': 'Unused.'
}


RESERVE_2 = {
    'required': True,
    'default': '',
    'input_types': (str,),
    'validator': None,
    'validation_exception': ValueError,
    'transformations': [
        (str, tuple())
    ],
    'description': 'Unused.'
}


RESERVE_3 = {
    'required': True,
    'default': '',
    'input_types': (str,),
    'validator': None,
    'validation_exception': ValueError,
    'transformations': [
        (str, tuple())
    ],
    'description': 'Unused.'
}
