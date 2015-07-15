from distutils.core import setup

setup(
    name='pyStrich',
    version='0.1.1',
    packages=['pystrich', 'pystrich.ean13', 'pystrich.qrcode', 'pystrich.code128', 'pystrich.datamatrix'],
    url='http://method-b.uk/pystrich/',
    license='Apache 2.0',
    author='Michael Mulqueen',
    author_email='michael@mulqueen.me.uk',
    description='PyStrich is a Python module to generate 1D and 2D barcodes (Code 128, DataMatrix, QRCode and EAN13).'
                'Forked from huBarcode.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Office/Business"
    ]
)
