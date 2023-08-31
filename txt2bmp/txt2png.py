#!python3
import sys
import os.path
from PIL import Image, ImageDraw, ImageFont

__dir__ = os.path.dirname(__file__) or "."

fnt = ImageFont.truetype(
    __dir__ +
    "/ASCII.ttf"  # https://alinamosig.eu/eistee.gmxhome.de/ascii/indexen.htm
)
mt = fnt.getmetrics()

for fn in sys.argv[1:]:
    test_str = open(fn).readlines()
    #test_str = test_str[:6]

    ysize = len(test_str)
    xsize = max([len(xx) for xx in test_str])

    pil_img = Image.new('RGB', (xsize*8+5, ysize*13+30), (255, 255, 255))
    _drawer = ImageDraw.Draw(pil_img)
    nn = 1
    for l1 in test_str:
        try:
            yy = 5 + nn * 12
            _drawer.text((3, yy), "%3d:" % nn, font=fnt, fill=(128, 128, 128))
            _drawer.text((30, yy), l1, font=fnt, fill=(0, 0, 0))
        except UnicodeEncodeError:
            pass
        nn += 1
    pil_img.save(fn+".png")
