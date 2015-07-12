"""Generate test images for EAN13 barcode encoder"""

from pystrich.ean13 import EAN13Encoder
from pystrich.ean13.test_ean13 import EAN13Test


for index, string in enumerate(EAN13Test.test_strings):
    enc = EAN13Encoder(string)
    enc.save("pystrich/ean13/test_img/%d.png" % (index + 1))
