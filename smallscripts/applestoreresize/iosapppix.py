#!python3

import PIL
import PIL.ImageColor
import PIL.Image
import PIL.ImageFile
# from PIL import Image
import sys

hwsize_ll = [
    ["6.5", [1284, 2778]],
    ["5.5", [1242, 2208]],
    ["12.9g3", [2048, 2732]],
    # ["12.9g2", [1668, 2388]],
    # ["4.7", [750, 1334]],
]

revdict = dict([(tuple(ii[1]), ii[0]) for ii in hwsize_ll])
# print(revmap)

for fn in sys.argv[1:]:
    img_pil: PIL.ImageFile.ImageFile = PIL.Image.open(fn)
    osize = img_pil.size
    sizekey = tuple(sorted(osize))
    portrait = sizekey == osize
    hwtype = None
    if sizekey in revdict:
        hwtype = revdict[sizekey]
    print(img_pil, img_pil.size, hwtype, portrait)

    for tgt_hw, tgt_rawsize in hwsize_ll:
        tgtsize = tgt_rawsize if portrait else reversed(tgt_rawsize)

        _xscale = tgtsize[0] / sizekey[0]
        _yscale = tgtsize[1] / sizekey[1]

        _scale = min(_xscale, _yscale)

        _ispad = tgt_hw[-2] == "g"

        if _ispad:
            _scale = 1.0
        ntsize = (int(sizekey[0] * _scale), int(sizekey[1]*_scale))
        print(tgt_hw, tgt_rawsize, ntsize, _scale)

        # https://note.nkmk.me/python-pillow-add-margin-expand-canvas/
        back_pil: PIL.Image = PIL.Image.new(
            img_pil.mode, tgtsize)

        rzimg_pil: PIL.Image = img_pil.resize(ntsize)

        back_pil.paste(rzimg_pil,
                       ((tgtsize[0]-ntsize[0])//2,
                           (tgtsize[1]-ntsize[1])//2))

        newfn = "[%s]%s-%s" % (tgt_hw, tuple(tgtsize), fn)
        # print(rz, fnt)
        back_pil.save(newfn)
