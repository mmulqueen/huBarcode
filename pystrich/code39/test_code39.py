import filecmp
import os.path
import tempfile
import unittest

from pystrich.code39 import Code39Encoder

test_strings = [
    "1234567890",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
]


class Code39Test(unittest.TestCase):
    def test_against_generated(self):
        """Compare the output of this library with generated barcodes"""

        with tempfile.TemporaryDirectory() as tmpdirname:
            for index, string in enumerate(test_strings):
                generated = os.path.join(tmpdirname, "%d.png" % (index + 1))
                encoder = Code39Encoder(string)
                encoder.save(generated)


                test_against = 'pystrich/code39/test_img/%d.png' % (index + 1)
                self.assertTrue(filecmp.cmp(generated, test_against),
                                msg="{} didn't match {}".format(test_against, generated))
