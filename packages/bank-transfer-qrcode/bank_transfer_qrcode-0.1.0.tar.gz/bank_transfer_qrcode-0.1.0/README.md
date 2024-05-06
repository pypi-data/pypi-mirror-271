# Bank-Transfer-QRCode
> Generate QR codes for bank transfers.

[![PyPi version](https://img.shields.io/badge/pypi-0.1.0-green)](https://pypi.org/project/bank-transfer-qrcode/)
[![Supported Python versions](https://img.shields.io/badge/Python-3.11-blue)](https://pypi.org/project/bank-transfer-qrcode/)


This package generates QR codes to be used with banking application. 
Provide information about the receiver, generate a QR code and scan it with a 
banking application.

Implementation is based on [this recommendation](https://zbp.pl/getmedia/1d7fef90-d193-4a2d-a1c3-ffdf1b0e0649/2013-12-03_-_Rekomendacja_-_Standard_2D)
and may not follow strict laws or other binding regulations.

![QR Code Example](https://github.com/Karolsoon/Bank-Transfer-QR/blob/main/examples/example_bank_transfer_qrcode.png?raw=true)

## Installation

OS X & Linux, Windows:

```sh
python -m pip install bank-transfer-qrcode
```

## Usage example

Import the QR module from the package
```py
from bank_transfer_qrcode import QR
```


Provide information about the recipient and create an instance of QR
```py
qr = QR(
    country_code='PL',
    iban='PL01234567890123456789012345',
    amount='000123',
    recipient_name='Bob Smith',
    transfer_title='Payment title'
)
```

Save the QR
```py
# Save as svg
qr.save('svg_filename', 'svg')
# Save as png
qr.save('png_filename', 'png')
```

...or get an io.BytesIO object and do something with it
```py
qr.get()
```

For mor information check the QR class or method docstrings or use
```py 
QR.info()
```

## Release History

* 0.1.0
    * The first release


## Meta

Karol Podgórski, karolsoon.dev@gmail.com

Distributed under the BSD license. See ``LICENSE`` for more information.

[https://github.com/Karolsoon/Bank-Transfer-QR/blob/main/LICENSE](https://github.com/Karolsoon/Bank-Transfer-QR/blob/main/LICENSE)
