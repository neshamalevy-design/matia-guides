"""The footprints from Gemini (feet2_src.jpg) walk upwards. Turn them to walk right-to-left (toes pointing left),
keeping the word 'צעד' upright: the letters are lifted out, the feet are rotated, and the letters are put back upright.
Run from the repo root:  python -X utf8 _build/rotatefeet.py   ->  _build/steps-feet2.png"""
from collections import deque
import pathlib
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).parent
src = Image.open(HERE / 'feet2_src.jpg').convert('RGB')
src = src.resize((src.width // 2, src.height // 2), Image.LANCZOS)           # 806x1000 is plenty for a ~220px graphic
W, H = src.size
a = np.asarray(src).astype(float)
BOXES = [(200, 510, 330, 575), (485, 372, 610, 437)]                        # the word in the red foot, in the teal foot


def grow(m, n):
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(n))) > 0


def components(mask, min_size):
    """keep only the connected shapes of at least min_size pixels."""
    seen = np.zeros_like(mask); keep = np.zeros_like(mask)
    for y, x in zip(*np.nonzero(mask)):
        if seen[y, x]:
            continue
        comp, q = [], deque([(y, x)]); seen[y, x] = True
        while q:
            cy, cx = q.popleft(); comp.append((cy, cx))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
        ys, xs = zip(*comp)
        if len(comp) >= min_size and (a.shape[:2] != mask.shape or a[list(ys), list(xs)].sum(axis=1).mean() < 570):   # pale = dots, shadow
            keep[list(ys), list(xs)] = True
    return keep


# 1) the letters: bright cream pixels inside each word box
L = []
for x0, y0, x1, y1 in BOXES:
    m = np.zeros((H, W), bool)
    m[y0:y1, x0:x1] = a[y0:y1, x0:x1].sum(axis=2) > 600
    L.append(m)

# 2) erase the whole word area (letters and their 3D shading), filling from the coloured sole around it
mask = np.zeros((H, W), bool)
for x0, y0, x1, y1 in BOXES:
    mask[y0 - 4:y1 + 4, x0 - 4:x1 + 4] = True
clean = a.copy()
for x0, y0, x1, y1 in BOXES:                                                 # start from the mean of the box border
    ring = np.concatenate([a[y0 - 6, x0 - 6:x1 + 6], a[y1 + 5, x0 - 6:x1 + 6], a[y0 - 6:y1 + 6, x0 - 6], a[y0 - 6:y1 + 6, x1 + 5]])
    clean[y0 - 4:y1 + 4, x0 - 4:x1 + 4] = ring.mean(axis=0)
for _ in range(1500):                                                       # smooth (Laplace) fill: no seams
    avg = (np.roll(clean, 1, 0) + np.roll(clean, -1, 0) + np.roll(clean, 1, 1) + np.roll(clean, -1, 1)) / 4
    clean[mask] = avg[mask]

# 3) transparent background; keep only the feet and toes (drop the small dots, dashed arrows and the floor shadow)
fg = clean.sum(axis=2) < 640                                                # the background and the floor shadow are lighter
fg = np.asarray(Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))) > 0   # detach the dashes
fg = components(fg, 1800)
fg = grow(fg, 5)
fg &= clean.sum(axis=2) < 600                                             # drop the soft shadow ring that joins the arrow dashes to the feet
fg = components(fg, 1800)
alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
out = Image.fromarray(clean.clip(0, 255).astype(np.uint8)).convert('RGBA')
out.putalpha(alpha)

# 4) turn a quarter to the left: toes point left, the walk goes right-to-left
out = out.rotate(90, expand=True)                                           # (x, y) -> (y, W-1-x)

# drop any small leftover (arrow dashes): only big solid shapes stay
arr = np.asarray(out).copy(); H2, W2 = arr.shape[:2]
H, W = H2, W2                                                                # components() works on the rotated size now
solid = components(arr[..., 3] > 128, 600)
arr[..., 3] = (arr[..., 3] * grow(solid, 5)).astype(np.uint8)
out = Image.fromarray(arr)
H, W = src.height, src.width
# the two arrow dashes that touch the feet' outer shadow (measured spots, outside the outline): clear them
box = out.getbbox(); out = out.crop(box)                                  # zones below are in cropped coordinates
arr = np.asarray(out).astype(float)
for x0, y0, x1, y1 in [(628, 405, 663, 455), (466, 470, 510, 525)]:
    zone = arr[y0:y1, x0:x1]
    dark = zone[..., :3].sum(axis=2) < 232                                  # the navy dash (the foot's teal edge is ~240+)
    dark = np.asarray(Image.fromarray((dark * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
    for _ in range(400):                                                    # paint it over from the shadow around it
        avg = (np.roll(zone, 1, 0) + np.roll(zone, -1, 0) + np.roll(zone, 1, 1) + np.roll(zone, -1, 1)) / 4
        zone[dark] = avg[dark]
out = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
out.save(HERE / 'steps-feet2-blank.png')              # without words: preview_cards writes them

# 5) the original letters back, upright, at their new place
for (x0, y0, x1, y1), lm in zip(BOXES, L):
    patch = src.crop((x0, y0, x1, y1)).convert('RGBA')
    pa = np.asarray(patch).astype(float)
    op = ((pa[..., :3].sum(axis=2) - 520) / 120).clip(0, 1) * 255            # cream strokes, antialiased
    op *= grow(lm, 3)[y0:y1, x0:x1]
    patch.putalpha(Image.fromarray(op.astype(np.uint8)))
    cx, cy = (y0 + y1) / 2, W - 1 - (x0 + x1) / 2
    out.alpha_composite(patch, (round(cx - patch.width / 2), round(cy - patch.height / 2)))

out = out.crop(out.getbbox())
out.save(HERE / 'steps-feet2.png')
print('ok', out.size)
