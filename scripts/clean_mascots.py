import json, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

m = json.load(open('data/mascots.json'))
fixed = []
for k, v in m.items():
    im = Image.open(v['file']).convert('RGBA')
    a = np.array(im)[:, :, 3]
    # hard threshold, then keep only the largest connected blob -> kills corner remnants
    mask = a > 140
    lab, n = ndimage.label(mask)
    if n > 1:
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        keep = (np.argmax(sizes) + 1)
        mask = lab == keep
    mask = ndimage.binary_fill_holes(mask)
    new_a = (a * mask).astype(np.uint8)
    out = Image.fromarray(np.dstack([np.array(im)[:, :, :3], new_a]), 'RGBA')
    # feather 1px so edges aren't jagged
    alpha = out.getchannel('A').filter(ImageFilter.GaussianBlur(0.8))
    out.putalpha(alpha)
    bb = out.getbbox()
    if bb: out = out.crop(bb)
    out.save(v['file'])
    v['size'] = out.size
    fixed.append(k)
json.dump(m, open('data/mascots.json', 'w'), indent=1)
print(len(fixed), 'cleaned')
