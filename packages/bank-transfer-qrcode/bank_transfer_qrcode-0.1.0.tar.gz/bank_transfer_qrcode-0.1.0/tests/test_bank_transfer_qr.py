from copy import deepcopy

import pytest

from bank_transfer_qrcode.bank_transfer_qr import QR
from bank_transfer_qrcode.exceptions import BaseValidationError, QRTextValidationError
from bank_transfer_qrcode.field_definitions import (
    RECIPIENT_IDENTIFIER,
    COUNTRY_CODE,
    IBAN_PL,
    AMOUNT_IN_POLSKIE_GROSZE,
    RECIPIENT_NAME,
    TRANSFER_TITLE,
    RESERVE_1,
    RESERVE_2,
    RESERVE_3
)


@pytest.fixture(scope='function')
def qr_instance():
    return QR(
        iban='01234567890123456789012345',
        recipient_name='John Doe',
        transfer_title='Payment title'
    )


@pytest.fixture(scope='function')
def qr_with_incorrect_transformations():
    class QR_with_bad_transformations(QR):
        pass

    QR_with_bad_transformations.definitions = {
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

    for field, definition in QR_with_bad_transformations.definitions.items():
        definition['transformations'] = [
                (dict(), tuple())
            ]
    
    return QR_with_bad_transformations


@pytest.mark.parametrize(
    argnames='iban,recipient_name,payment_title',
    argvalues=[
        ('01234567890123456789012345', 'Bob Smith', 'Payment title'),
        ('01234567890123456789012345', 'Bob ąąąśśśććććłłłóóó', 'Payment tłłóśąęć'),
        ('PL01234567890123456789012345', 'Bob Smith', 'Payment title')
    ]
)
def test_can_create_qr_instance_with_minimal_set_of_parameters(
        iban,
        recipient_name,
        payment_title):
    qr = QR(
        iban=iban,
        recipient_name=recipient_name,
        transfer_title=payment_title
    )
    assert isinstance(qr, QR)


def test_can_create_qr_instance_with_all_parameters():
    recipient_identifier = '123-123-12-12'
    country_code = 'PL'
    iban = 'PL01234567890123456789012345'
    amount = '000123'
    recipient_name = 'Bob Smith'
    transfer_title = 'Payment title'
    qr = QR(
        iban=iban,
        recipient_name=recipient_name,
        transfer_title=transfer_title,
        amount=amount,
        recipient_identifier=recipient_identifier,
        country_code=country_code
    )
    assert isinstance(qr, QR)


@pytest.mark.parametrize(
    argnames='value,definition,field_name',
    argvalues=[
        ('123-123-12-12', RECIPIENT_IDENTIFIER['type_2'], 'Recipient Identifier'),
        ('PL01234567890123456789012345', IBAN_PL, 'IBAN'),
        ('PL', COUNTRY_CODE, 'Country Code'),
        ('Bob Smith', RECIPIENT_NAME, 'Recipient Name'),
        ('000123', AMOUNT_IN_POLSKIE_GROSZE, 'Amount'),
        ('FV 2024/11/12-0006', TRANSFER_TITLE, 'Transfer Title')
    ]
)
def test_validate_one_method_correctly_uses_arguments(
        value: str,
        definition: dict,
        field_name: str,
        qr_instance: QR):
    try:
        qr_instance._validate_one(value, definition, field_name)
    except BaseValidationError:
        pytest.fail('Validation in _validate_one() failed but should pass')
    except Exception:
        pytest.fail('An exception was raised while processing _validate_one()')


@pytest.mark.parametrize(
    argnames='value,definition,field_name',
    argvalues=[
        ('123-123-12-12-12-12', RECIPIENT_IDENTIFIER['type_2'], 'Recipient Identifier'),
        ('GB01234567890123456789012345', IBAN_PL, 'IBAN'),
        ('16', COUNTRY_CODE, 'Country Code'),
        ('Bob Smith ************', RECIPIENT_NAME, 'Recipient Name'),
        ('0001234', AMOUNT_IN_POLSKIE_GROSZE, 'Amount'),
        ('FV', TRANSFER_TITLE, 'Transfer Title')
    ]
)
def test_validate_one_raises_relevant_validation_error_when_validation_failed(
        value: str,
        definition: dict,
        field_name: str,
        qr_instance: QR):
    expected_exception = definition['validation_exception']
    with pytest.raises(expected_exception=expected_exception):
        qr_instance._validate_one(value, definition, field_name)


def test_qr_text_format_of_qr_instance():
    pass


def test_can_save_code_to_file():
    pass


def test_raises_value_error_when_save_directory_not_exists():
    pass



# Transformations

@pytest.mark.parametrize(
    argnames='value,definition,field_name',
    argvalues=[
        (['123-123-12-12'], RECIPIENT_IDENTIFIER['type_2'], 'recipient_identifier'),
        (1234567890123456789012345.0, IBAN_PL, 'iban'),
        (('pl',), COUNTRY_CODE, 'country_code'),
        (['Bob', 'Smith'], RECIPIENT_NAME, 'recipient_name'),
        ({'amount': '0001234'}, AMOUNT_IN_POLSKIE_GROSZE, 'amount'),
        (20240101, TRANSFER_TITLE, 'transfer_title')
    ]
)
def test_transformation_raises_type_error_when_input_is_wrong_type(
        value,
        definition: dict,
        field_name: str,
        qr_instance: QR
        ):
    with pytest.raises(TypeError):
        qr_instance._transform_one(field_name, value)


def test_transformation_raises_type_error_when_first_item_is_not_callable(qr_with_incorrect_transformations):
    # Replace existing transformation
    with pytest.raises(TypeError) as exc_info:
        qr_with_incorrect_transformations(
            '01234567890123456789012345',
            'Bob Smith',
            'Payment title'
        )
    assert exc_info.match(
        'Transformation must be callable. '
        f'Please review transformations for "iban"')


# QR text validation

def test_with_length_above_160_characters_raises_validation_error(qr_instance):
    qr_instance.data = {k: '' for k in qr_instance.data}
    qr_instance.data['transfer_title'] = 'a' * 153 # + 8 separators gives 161 characters
    with pytest.raises(QRTextValidationError):
        qr_instance._set_qr_text()


def test_qr_text_with_length_equal_to_160_characters_does_not_raise_error(qr_instance):
    qr_instance.data = {k: '' for k in qr_instance.data}
    qr_instance.data['transfer_title'] = 'a' * 152 # + 8 separators gives 160 characters
    qr_instance._set_qr_text()

    assert len(qr_instance._qr_text) == 160
