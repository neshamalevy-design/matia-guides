"""A version of the footprints with both feet in teal: the red sole and the orange toes take the colours of the teal foot
(matched by brightness, so the 3D shading stays). Run from the repo root -> _build/steps-feet2-teal.png"""
import pathlib
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).parent
im = np.asarray(Image.open(HERE / 'steps-feet2-blank.png')).astype(float)
r, g, b, al = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
H, W = al.shape
lum = 0.3 * r + 0.59 * g + 0.11 * b
warm = (r > g + 20) & (r > b + 20) & (al > 0)
yy, xx = np.mgrid[0:H, 0:W]
top = yy < 290                                                   # the teal foot
teal = top & (al > 200) & (b >= r)
src_toes = warm & (xx < 225)                                     # the orange toes
src_sole = warm & (xx >= 225)                                    # the red sole
tgt_toes = teal & (xx < 115) & (lum < 120)                       # the teal toes
tgt_sole = teal & (xx > 140) & (xx < 480) & (yy > 70) & (yy < 230) & (lum < 125)   # the dark teal sole


def match(src, tgt):
    """give each source pixel the colour of the target pixel at the same brightness rank."""
    s_idx = np.argsort(lum[src]); t = im[tgt][np.argsort(lum[tgt])][:, :3]
    pos = (np.arange(len(s_idx)) * (len(t) - 1) / max(len(s_idx) - 1, 1)).astype(int)
    out = np.empty((len(s_idx), 3)); out[s_idx] = t[pos]
    return out


res = im.copy()
for s, t in ((src_toes, tgt_toes), (src_sole, tgt_sole)):
    res[s, :3] = match(s, t)
Image.fromarray(res.clip(0, 255).astype(np.uint8)).save(HERE / 'steps-feet2-teal.png')
print('ok', int(src_toes.sum()), int(src_sole.sum()))
