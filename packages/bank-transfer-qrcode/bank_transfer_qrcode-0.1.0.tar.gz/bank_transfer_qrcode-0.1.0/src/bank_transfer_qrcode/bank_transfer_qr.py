import io
from copy import deepcopy

import segno

from .exceptions import QRTextValidationError
from .field_definitions import (
    QR_TEXT_FORMAT,
    RECIPIENT_IDENTIFIER,
    COUNTRY_CODE,
    IBAN_PL,
    AMOUNT_IN_POLSKIE_GROSZE,
    RECIPIENT_NAME,
    TRANSFER_TITLE,
    SEPARATOR,
    RESERVE_1,
    RESERVE_2,
    RESERVE_3,
    MAX_QR_TEXT_LENGTH
)


class QR:

    # QR code requirements
    __encoding = 'UTF-8'
    __error_correction = 'L'
    __qr_version = 4
    __min_size_px = {
        'width': 250,
        'height': 250
    }
    __min_size_cm = {
        'width': 1.8,
        'height': 1.8
    }
    __qr_text_format = QR_TEXT_FORMAT
    __separator = SEPARATOR
    __max_qr_text_length = MAX_QR_TEXT_LENGTH

    # Formating requirements and definitions
    definitions = {
        'recipient_identifier': deepcopy(RECIPIENT_IDENTIFIER['type_2']),
        'country_code': deepcopy(COUNTRY_CODE),
        'iban': deepcopy(IBAN_PL),
        'amount': deepcopy(AMOUNT_IN_POLSKIE_GROSZE),
        'recipient_name': deepcopy(RECIPIENT_NAME),
        'transfer_title': deepcopy(TRANSFER_TITLE),
        'reserve_1': deepcopy(RESERVE_1),
        'reserve_2': deepcopy(RESERVE_2),
        'reserve_3': deepcopy(RESERVE_3)
    }

    def __init__(
            self,
            iban: str,
            recipient_name: str,
            transfer_title: str,
            amount: int|str=definitions['amount']['default'],
            country_code: str=definitions['country_code']['default'],
            recipient_identifier: str|int=definitions['recipient_identifier'
                                                  ]['default']
            ):
        """
        # Bank-Transfer-QR
        Creates an instance of a Bank Transfer QR code accepted
        by banking applications in Poland.

        #### For detailed descriptions check out the below dosctring or use `QR.info()`

        ### iban (required)

        `iban` - the IBAN account number of the recipient. Can be optionally
        prefixed with 'PL'. Format: '(PL)01234567890123456789012345', no spaces.

        ### recipient_name (required)
        `recipient_name` - max. 20 characters. Accepts letters, numbers,
        hypthens, underscores, dots and spaces.

        ### transfer_title (required)
        `transfer_title` - max. 32 characters long. Accepts letters, numbers,
        hyphens, underscores, dots and spaces.

        ### amount (optional)

        Default: `'000000'`

        `amount` - the amount to be transferred, represented as a 6-digit str.
        The last 2 digits (on the right) is the amount of Polski Grosz
        while the first 4 digits represent the amount of Polski Złoty.
        Example:
        #### `'010999'` equals `109,99 zł`
        If instead an `int` is provided, the value will be translated into
        a 6-digit str.
        Example:
        #### `int(123)` equals `'000123'` equals `1,23 zł`
        #### `float(123.0)` equals `'001230'` equals `12,30zł`

        If not provided, the default value of `'000000'` will be used, which
        informs the banking application, that the amount is to be specified
        manually within the application itself.

        The 6-digit notation is highly engouraged to reduce ambiguity!

        ### country_code (optional)

        Default: `'PL'`

        `country_code` - The country code of the recipients Bank Account. 
        Defaults to `'PL'`. Providing other values may not work due to local
        law enforcements or other regulations applicable.

        ### recipient_identifier (optional)

        Default: `''`

        `recipient_identifier` - The NIP (Tax identification number). Applicable
        only for institutional recipients, that is: not individuals.

        """
        self._segno_qr_object: segno.QRCode = None
        self._png = io.BytesIO()
        self._svg = io.BytesIO()

        self._qr_text = QR_TEXT_FORMAT
        self.data = {
            'iban': None,
            'recipient_name': None,
            'transfer_title': None,
            'amount': None,
            'country_code': None,
            'recipient_identifier': None,
            'reserve_1': '',
            'reserve_2': '',
            'reserve_3': ''
        }

        self._process(
            iban=iban,
            recipient_name=recipient_name,
            transfer_title=transfer_title,
            amount=amount,
            country_code=country_code,
            recipient_identifier=recipient_identifier
        )

    def show(self) -> None:
        """
        Displays the QR code.
        """
        self._segno_qr_object.show(
            scale=6,
            border=1
        )

    def get(self, file_type: str='png') -> io.BytesIO:
        """
        Returns an io.BytesIO object representation of a QR code.
        Output file type can be "png" or "svg". Defaults to "png".
        """
        if file_type.lower() == 'png':
            return self._png
        elif file_type.lower() == 'svg':
            return self._svg
        else:
            raise ValueError('Only "png" and "svg" are supported.')

    def save(self, path: str, file_type: str='png') -> None:
        """
        Saves the QR code in the desired format
        under the specified filename/path.
        """
        with open(path + '.' + file_type.lower(), mode='bw') as f:
            f.write(self.get(file_type).getvalue())

    @classmethod
    def info(cls) -> None:
        """
        Prints out the descriptions about the input fields to.
        """
        for field, definition in cls.definitions.items():
            if not field.startswith('reserve'):
                print(f'* {field} *')
                print(definition['description'])
                print('\n')


    def _process(self, **kwargs) -> None:
        data = self._transform(**kwargs)
        self._set_data(data)
        self._validate()
        self._set_qr_text()
        self._make()

    def _make(self) -> None:
        version = self.__qr_version
        while not self._segno_qr_object:
            try:
                self._segno_qr_object = segno.make(
                    content=self._qr_text,
                    error=self.__error_correction,
                    version=version,
                    encoding=self.__encoding
                )
            except segno.encoder.DataOverflowError as exc:
                version += 1
                if version > 6:
                    raise exc

        self._segno_qr_object.save(
            self._png,
            kind='png',
            scale=6,
            border=1
        )

        self._segno_qr_object.save(
            self._svg,
            kind='svg',
            scale=6,
            border=1,
            draw_transparent=True
        )

    def _set_qr_text(self) -> None:
        self._qr_text = self.__qr_text_format.format(
            separator=self.__separator,
            **self.data)
        self.__validate_qr_text_length()

    def _validate(self) -> None:
        for field_name, value in self.data.items():
            self._validate_one(
                value=value,
                definition=self.__get_definition(field_name),
                field_name=field_name
            )

    def _validate_one(
            self,
            value: str,
            definition: dict,
            field_name: str) -> None:
        validation_exception = definition['validation_exception']
        validator = definition['validator']
        if value and validator:
            if not validator.search(value):
                raise validation_exception(f'Incorrect {field_name} format')

    def _transform(self, **kwargs) -> str:
        """
        Applies transformations defined in the field definitions.
        Returns the transformed value as an str.
        """
        data = {}
        for field_name, value in kwargs.items():
            transformed = self._transform_one(
                field_name=field_name,
                value=value
            )
            data[field_name] = transformed
        return data

    def _transform_one(
            self,
            field_name: str,
            value: str|int|float
            ) -> str:
        definition = self.__get_definition(field_name)
        transformations = self.__get_transformations(definition)
        self.__validate_transformations_are_callable(
            transformations,
            field_name
        )
        self.__validate_input_type(value, definition, field_name)
        item = value
        for t in transformations:
            func, args = t
            item = func(item, *args)
        return item

    def _set_data(self, data: dict) -> None:
        self.data.update(data)

    def __validate_transformations_are_callable(
            self,
            transformations: list[tuple[callable, tuple[str|int|None]]],
            field_name: str) -> None:
        for t in transformations:
            if not callable(t[0]):
                raise TypeError(
                    'Transformation must be callable. '
                    f'Please review transformations for "{field_name}"'
                )

    def __validate_input_type(
            self,
            input_value,
            definition: dict,
            field_name: str) -> None:
        in_typ = definition['input_types']
        if not isinstance(input_value, in_typ):
            msg = (
                f'"{field_name}" value must be one of {in_typ}, '
                f'not {input_value.__class__.__name__}'
            )
            raise TypeError(msg)

    def __get_definition(self, field_name: str) -> None:
        if definition := self.definitions.get(field_name):
            return definition
        raise AttributeError(
            f'Unknown parameter passed into constructor: {field_name}')

    def __get_transformations(self, definition: dict) -> None:
        return definition.get('transformations')

    def __validate_qr_text_length(self) -> None:
        if len(self._qr_text) > self.__max_qr_text_length:
            raise QRTextValidationError(
                'The length of the underlying QR text exceeds '
                'the allowed max length: '
                f'{self.__max_qr_text_length} (is {len(self._qr_text)})')
