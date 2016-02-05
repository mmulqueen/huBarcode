#!/usr/bin/env python

"""2D Datamatrix barcode encoder

All needed by the user is done via the DataMatrixEncoder class:

>>> encoder = DataMatrixEncoder("HuDoRa")
>>> # encoder.save( "test.png" )
>>> print encoder.get_ascii()
XX  XX  XX  XX  XX  XX  XX
XX  XXXX  XXXXXX      XXXXXX
XXXXXX    XX          XX
XXXXXX    XX        XXXX  XX
XXXX  XX  XXXXXX
XXXXXX    XXXXXXXX    XXXXXX
XX    XX  XXXXXXXX  XXXX
XX    XX      XXXX      XXXX
XX  XXXXXXXXXX    XXXX
XX  XXXX    XX            XX
XX  XXXXXX  XXXXXX      XX
XXXXXX  XX  XX  XX  XX    XX
XX    XX              XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXX


Implemented by Helen Taylor for HUDORA GmbH.
Updated and ported to Python 3 by Michael Mulqueen for Method B Ltd.

Detailed documentation on the format here:
http://grandzebu.net/informatique/codbar-en/datamatrix.htm
Further resources here: http://www.libdmtx.org/resources.php

You may use this under a BSD License.
"""

from __future__ import print_function

__revision__ = "$Rev$"

import numpy as np

try:
    from .textencoder import TextEncoder
    from .placement import DataMatrixPlacer
    from .renderer import DataMatrixRenderer
except ValueError:
    from textencoder import TextEncoder
    from placement import DataMatrixPlacer
    from renderer import DataMatrixRenderer


class DataMatrixEncoder:
    """Top-level class which handles the overall process of
    encoding input data, placing it in the matrix and
    outputting the result"""

    def __init__(self, text, sz=None):
        """Set up the encoder with the input text.
        This will encode the text,
        and create a matrix with the resulting codewords"""

        enc = TextEncoder()
        self.codewords = enc.encode(text, sz=sz)
        self.width = 0
        self.height = 0
        matrix_size = enc.mtx_size
        self.regions = enc.regions

        self.matrix = [[None] * matrix_size[1] for _ in range(0, matrix_size[0])]

        placer = DataMatrixPlacer()
        placer.place(self.codewords, self.matrix)

    def save(self, filename, cellsize=5):
        """Write the matrix out to an image file"""
        dmtx = DataMatrixRenderer(self.matrix, self.regions)
        dmtx.write_file(cellsize, filename)

    def get_imagedata(self, cellsize=5):
        """Write the matrix out to an PNG bytestream"""
        dmtx = DataMatrixRenderer(self.matrix, self.regions)
        self.width = dmtx.width
        self.height = dmtx.height
        return dmtx.get_imagedata(cellsize)

    def get_ascii(self):
        """Return an ascii representation of the matrix"""
        dmtx = DataMatrixRenderer(self.matrix, self.regions)
        return dmtx.get_ascii()

def add_margins(matrix, regions=2):
    nrow, ncol = np.shape(matrix)
    print(nrow)
    print(ncol)

    assert regions<=2
    for i in range(regions):
        nc = ncol/regions
        nr = nrow

        if i==0:
            m = matrix[:, 0:nc]
        else:
            m = matrix[:, nc:]

        left_col = np.ones((nr+2,1))
        bottom_row = np.ones((1, nc))
        top_row = np.reshape([[0,1] for _ in range(nc/2)], (1, nc))
        right_row = np.reshape([[0,1] for _ in range(nr/2+1)], (nr+2, 1))
        m = np.row_stack((top_row, m))
        m = np.row_stack((m, bottom_row))
        m = np.column_stack((left_col, m))
        m = np.column_stack((m, right_row))
        if i == 0:
            ans = m
        else:
            ans = np.column_stack((ans, m))
    return ans

if __name__=='__main__':
    from PIL import Image
    sz = None
    test_string = 'wikipedia'
#    test_string = 'what is question of the century? romeo must die. juliet should die also. lorem ipsum, a nods as good as a wink to a blind bat.'

    encoder = DataMatrixEncoder(test_string)

    print(np.mat(encoder.matrix))

    ans = add_margins(np.mat(encoder.matrix), encoder.regions[1])
    print(ans)
    m = np.array(ans, dtype='u1')
    m[m==0] = 9
    m[m==1] = 0
    m[m==9] = 1
    im = Image.fromarray(m*255)
    im.show()

