"""Text encoder for 2D datamatrix barcode encoder"""

__revision__ = "$Rev$"

try:
    from .reedsolomon import get_reed_solomon_code
except ValueError:
    from reedsolomon import get_reed_solomon_code

import logging

log = logging.getLogger("datamatrix")

data_word_length = (3, 5, 8, 12, 18, 22, 30, 36, 44,
                    62, 86, 114, 144, 174, 204,
                    280, 368, 456, 576, 696, 816,
                    1050, 1304, 1558)

error_word_length = (5, 7, 10, 12, 14, 18, 20, 24, 28,
                     36, 42, 48, 56, 68, 84,
                     112, 144, 192, 224, 272, 336,
                     408, 496, 620)

data_region_size = (8, 10, 12, 14, 16, 18, 20, 22, 24,
                    14, 16, 18, 20, 22, 24,
                    14, 16, 18, 20, 22, 24,
                    18, 20, 22)

hv_regions = (1, 1, 1, 1, 1, 1, 1, 1, 1,
              2, 2, 2, 2, 2, 2,
              4, 4, 4, 4, 4, 4,
              6, 6, 6)

rectangular_size_map = {(8, 18): 5,
                         (8, 32): 10,
                         (12, 26): 16,
                         (12, 36): 22,
                         (16, 36): 32,
                         (16, 48): 49
                         }


class DataTooLongForImplementation(Exception):
    pass


class TextEncoder:
    """Text encoder class for 2D datamatrix"""

    def __init__(self):
        self.padsize = None
        self.length = None
        self.unpadded_length = None
        self.codewords = ''
        self.size_index = None
        self.mtx_size = 0
        self.regions = None
        self.initialize_size_map()


    def initialize_size_map(self):
        # eg http://www1.isma.lv/fileadmin/ISMA/Publications/ITMS/2009/ITMS_Volume2_N1/04_it%26m_2009_Krasikov_proceedings.pdf
        self.size_map = {}
        self.size_map[ (8, 8) ]= {'data_word_length': 3, 'hv_regions': (1, 1), 'error_word_length': 5}
        self.size_map[ (10, 10) ]= {'data_word_length': 5, 'hv_regions': (1, 1), 'error_word_length': 7}
        self.size_map[ (12, 12) ]= {'data_word_length': 8, 'hv_regions': (1, 1), 'error_word_length': 10}
        self.size_map[ (14, 14) ]= {'data_word_length': 12, 'hv_regions': (1, 1), 'error_word_length': 12}
        self.size_map[ (16, 16) ]= {'data_word_length': 18, 'hv_regions': (1, 1), 'error_word_length': 14}
        self.size_map[ (18, 18) ]= {'data_word_length': 22, 'hv_regions': (1, 1), 'error_word_length': 18}
        self.size_map[ (20, 20) ]= {'data_word_length': 30, 'hv_regions': (1, 1), 'error_word_length': 20}
        self.size_map[ (22, 22) ]= {'data_word_length': 36, 'hv_regions': (1, 1), 'error_word_length': 24}
        self.size_map[ (24, 24) ]= {'data_word_length': 44, 'hv_regions': (1, 1), 'error_word_length': 28}
        self.size_map[ (28, 28) ]= {'data_word_length': 62, 'hv_regions': (2, 2), 'error_word_length': 36}
        self.size_map[ (32, 32) ]= {'data_word_length': 86, 'hv_regions': (2, 2), 'error_word_length': 42}
        self.size_map[ (36, 36) ]= {'data_word_length': 114, 'hv_regions': (2, 2), 'error_word_length': 48}
        self.size_map[ (40, 40) ]= {'data_word_length': 144, 'hv_regions': (2, 2), 'error_word_length': 56}
        self.size_map[ (44, 44) ]= {'data_word_length': 174, 'hv_regions': (2, 2), 'error_word_length': 68}
        self.size_map[ (48, 48) ]= {'data_word_length': 204, 'hv_regions': (2, 2), 'error_word_length': 84}
        self.size_map[ (56, 56) ]= {'data_word_length': 280, 'hv_regions': (4, 4), 'error_word_length': 112}
        self.size_map[ (64, 64) ]= {'data_word_length': 368, 'hv_regions': (4, 4), 'error_word_length': 144}
        self.size_map[ (72, 72) ]= {'data_word_length': 456, 'hv_regions': (4, 4), 'error_word_length': 192}
        self.size_map[ (80, 80) ]= {'data_word_length': 576, 'hv_regions': (4, 4), 'error_word_length': 224}
        self.size_map[ (88, 88) ]= {'data_word_length': 696, 'hv_regions': (4, 4), 'error_word_length': 272}
        self.size_map[ (96, 96) ]= {'data_word_length': 816, 'hv_regions': (4, 4), 'error_word_length': 336}
        self.size_map[ (108, 108) ]= {'data_word_length': 1050, 'hv_regions': (6, 6), 'error_word_length': 408}
        self.size_map[ (120, 120) ]= {'data_word_length': 1304, 'hv_regions': (6, 6), 'error_word_length': 496}
        self.size_map[ (132, 132) ]= {'data_word_length': 1558, 'hv_regions': (6, 6), 'error_word_length': 620}

        self.size_map[ (6, 16) ]= {'data_word_length': 5, 'hv_regions': (1, 1), 'error_word_length': 7}
        self.size_map[ (6, 28) ]= {'data_word_length': 10, 'hv_regions': (1, 2), 'error_word_length': 11}
        self.size_map[ (10, 24) ]= {'data_word_length': 16, 'hv_regions': (1, 1), 'error_word_length': 14}
        self.size_map[ (10, 32) ]= {'data_word_length': 22, 'hv_regions': (1, 2), 'error_word_length': 18}
        self.size_map[ (14, 32) ]= {'data_word_length': 32, 'hv_regions': (1, 2), 'error_word_length': 24}
        self.size_map[ (14, 44) ]= {'data_word_length': 49, 'hv_regions': (1, 2), 'error_word_length': 28}

    def encode(self, text, sz=None):
        """Encode the given text and add padding and error codes
        also set up the correct matrix size for the resulting codewords"""

        self.encode_text(text)
        self.set_matrix_size(sz)
        self.pad()
        self.append_error_codes()

        log.debug(
            "Codewords: " +
            ' '.join([str(ord(codeword)) for codeword in self.codewords]))

        self.regions = self.specs['hv_regions']

        log.debug("Matrix size will be %d", self.mtx_size)

        return self.codewords

    def encode_text(self, text):
        """Encode the given text into codewords"""

        numbuf = ''

        for char in text:
            if char.isdigit():
                numbuf += char
                if len(numbuf) == 2:
                    # we have collected two numbers: add them as a digit pair
                    self.append_digits(numbuf)
                    numbuf = ''
            else:
                if numbuf:
                    # an unpaired number: add it as an ascii character
                    self.append_ascii_char(numbuf)
                    numbuf = ''

                # a regular ascii character
                self.append_ascii_char(char)

        # there might be a single number left over at the end
        if numbuf:
            self.append_ascii_char(numbuf)

    def determine_mtx_size_from_codewords(self):

        best = {'area': 999*999, 'sz': None}
        for k, v in self.size_map.items():
            wlen = v['data_word_length']
            symbol_area = k[0]*k[1]
            if (wlen>=self.unpadded_len) and (symbol_area<best['area']):
                best['sz'] = k
                best['area'] = symbol_area
        return best['sz']

    def set_matrix_size(self, sz=None):
        self.unpadded_len = len(self.codewords)
        log.debug("Unpadded data size:   %d bytes", self.unpadded_len)

        if self.unpadded_len > 174:
            raise DataTooLongForImplementation("PyStrich does not currently support encoding beyond 174 characters. "
                                               "See https://github.com/mmulqueen/pyStrich/issues/2")

        # Work out how big the matrix needs to be
        if sz is not None:
            self.mtx_size = sz
            self.specs = self.size_map[sz]
        else:
            self.mtx_size = self.determine_mtx_size_from_codewords()
            self.specs = self.size_map[self.mtx_size]


        # Number of characters with which the data will be padded
        self.padsize = self.specs['data_word_length'] - self.unpadded_len


    def pad(self):
        """Pad out the encoded text to the correct word length"""

        log.debug("Pad size: %d bytes", self.padsize)

        # First pad character is 129
        if self.padsize:
            self.codewords += chr(129)

        def rand253(pos):
            """generate the next padding character"""
            rnd = ((149 * pos) % 253) + 1
            return (129 + rnd) % 254

        # Remaining pad characters generated by 253-state algorithm
        for i in range(1, self.padsize):
            self.codewords += chr(rand253(self.unpadded_len + i + 1))

        log.debug("Word size after padding: %d bytes", len(self.codewords))

    def append_error_codes(self):
        """Calculate the necessary number of Reed Solomon error codes for the
        encoded text and padding codewords, and append to the codeword buffer"""

        error_length = self.specs['error_word_length']
        log.debug("Error word length: %d bytes", error_length)

        error_words = get_reed_solomon_code(self.codewords, error_length)

        self.codewords += error_words

    def append_digits(self, digits):
        """Write a pair of digits
        (the appended value is 130 + the integer value of the digits together"""

        append = chr(130 + int(digits))
        self.codewords += append
        log.debug('digits:  "%s" ==> %s', digits, ord(append))

    def append_ascii_char(self, char):
        """Append a single ascii character
        (the appended value is the value of the char plus 1"""

        append = chr(ord(char) + 1)
        self.codewords += append
        log.debug('ascii:   "%c" ==> %d', char, ord(append))
