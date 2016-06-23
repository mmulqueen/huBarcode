"""Code-39 barcode encoder

All needed by the user is done via the Code39Encoder class:

>>> encoder = Code39Encoder("MIL-STD-1189")
>>> encoder.save("test.png")

You may use this under a BSD License.
"""
from .textencoder import TextEncoder
from .renderer import Code39Renderer
import logging

log = logging.getLogger("code39")


class Code39Encoder:
    """Top-level class which handles the overall process of
    encoding input string and outputting the result"""

    def __init__(self, text, full_ascii=False, options=None):
        """ The options hash currently supports three options:
            * ttf_font: absolute path to a truetype font file used to render the label
            * ttf_fontsize: the size the label is drawn in
            * label_border: number of pixels space between the barcode and the label
            * bottom_border: number of pixels space between the label and the bottom border
            """

        self.options = options
        self.text = text
        self.height = 0
        self.width = 0
        encoder = TextEncoder()

        self.encoded_text = encoder.encode(self.text, full_ascii)
        log.debug("Encoded text is %s", self.encoded_text)

        self.bars = encoder.get_bars(self.encoded_text)
        log.debug("Bars: %s", self.bars)

    def get_imagedata(self, bar_width=3):
        """Write the matrix out to an PNG bytestream"""
        barcode = Code39Renderer(self.bars, self.text, self.options)
        imagedata = barcode.get_imagedata(bar_width)
        self.width = barcode.image_width
        self.height = barcode.image_height
        return imagedata

    def save(self, filename, bar_width=3):
        """Write the barcode out to an image file"""
        Code39Renderer(
            self.bars, self.text, self.options).write_file(filename, bar_width)
