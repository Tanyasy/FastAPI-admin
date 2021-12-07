@echo off

cd app
rd /s /Q  .\dist
rd /s /Q .\build
pyinstaller -F E:\workspace\FastAPI-admin\app\main.py ^
--hidden-import passlib.handlers ^
--hidden-import passlib.handlers.md5_crypt ^
--hidden-import passlib.handlers.argon2 ^
--hidden-import passlib.handlers.pbkdf2 ^
--hidden-import passlib.handlers.bcrypt ^
--hidden-import passlib.handlers.des_crypt ^
--hidden-import passlib.handlers.windows ^
--hidden-import passlib.handlers.cisco ^
--hidden-import passlib.handlers.django ^
--hidden-import passlib.handlers.fshp ^
--hidden-import passlib.handlers.digests ^
--hidden-import passlib.handlers.ldap_digests ^
--hidden-import passlib.handlers.roundup ^
--hidden-import passlib.handlers.mssql ^
--hidden-import passlib.handlers.mysql ^
--hidden-import passlib.handlers.oracle ^
--hidden-import passlib.handlers.phpass ^
--hidden-import passlib.handlers.misc ^
--hidden-import passlib.handlers.postgres ^
--hidden-import passlib.handlers.scram ^
--hidden-import passlib.handlers.scrypt ^
--hidden-import passlib.handlers.sha1_crypt ^
--hidden-import passlib.handlers.sha2_crypt ^
--hidden-import passlib.handlers.sun_md5_crypt ^
--hidden-import reportlab.graphics.barcode.common ^
--hidden-import reportlab.graphics.barcode.code39 ^
--hidden-import reportlab.graphics.barcode.code93 ^
--hidden-import reportlab.graphics.barcode.code128 ^
--hidden-import reportlab.graphics.barcode.usps ^
--hidden-import reportlab.graphics.barcode.usps4s ^
--hidden-import reportlab.graphics.barcode.widgets ^
--hidden-import reportlab.graphics.barcode.eanbc ^
--hidden-import reportlab.graphics.barcode.ecc200datamatrix ^
--hidden-import reportlab.graphics.barcode.fourstate ^
--hidden-import reportlab.graphics.barcode.lto ^
--hidden-import reportlab.graphics.barcode.qr ^
--hidden-import reportlab.graphics.barcode.qrencoder ^
--hidden-import babel.messages.pofile