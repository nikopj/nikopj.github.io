"""
Make a wavelet-tree hover image for the index page headshot: a multi-level 2D
CDF 9/7 DWT (the JPEG2000 wavelet) of each RGB channel, laid out as the usual
Mallat pyramid and stacked back into an RGB image.

    python3 _assets/scripts/headshot_wavelet.py _assets/headshot1.jpg _assets/headshotW.jpg

Each subband is scaled jointly across R, G, B so its colors are the real ones.
Detail subbands show |coefficient| on black (--style abs) or the signed
coefficient around mid-gray (--style signed).
"""
import argparse

import numpy as np
from PIL import Image

# CDF 9/7 lifting coefficients
ALPHA, BETA, GAMMA, DELTA, ZETA = -1.586134342, -0.05298011854, 0.8829110762, 0.4435068522, 1.149604398


def dwt97(x, axis):
    # one level along axis (even length), symmetric boundary extension
    x = np.moveaxis(x, axis, 0)
    s, d = x[0::2].copy(), x[1::2].copy()
    nxt = lambda u: np.concatenate([u[1:], u[-1:]])
    prv = lambda u: np.concatenate([u[:1], u[:-1]])
    d += ALPHA * (s + nxt(s))
    s += BETA * (prv(d) + d)
    d += GAMMA * (s + nxt(s))
    s += DELTA * (prv(d) + d)
    return np.moveaxis(s * ZETA, 0, axis), np.moveaxis(d / ZETA, 0, axis)


def dwt2(x):
    L, H = dwt97(x, 0)
    LL, LH = dwt97(L, 1)
    HL, HH = dwt97(H, 1)
    return LL, (LH, HL, HH)


def wavedec2(x, levels):
    details = []
    for _ in range(levels):
        x, d = dwt2(x)
        details.append(d)
    return x, details[::-1]  # coarsest first


def scale(c, style, pct, gamma):
    if style == "abs":
        return np.clip(np.abs(c) / np.percentile(np.abs(c), pct), 0, 1) ** gamma
    return np.clip(0.5 + 0.5 * c / np.percentile(np.abs(c), pct), 0, 1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--levels", type=int, default=3)
    p.add_argument("--style", choices=["abs", "signed"], default="abs")
    p.add_argument("--pct", type=float, default=99, help="detail percentile mapped to full scale")
    p.add_argument("--gamma", type=float, default=0.75, help="gamma for --style abs")
    p.add_argument("--line", type=int, default=3, help="subband separator width in px (0 = none)")
    args = p.parse_args()

    x = np.asarray(Image.open(args.src).convert("RGB"), dtype=np.float64) / 255
    H, W, _ = x.shape
    m = 2 ** args.levels
    x = np.pad(x, ((0, -H % m), (0, -W % m), (0, 0)), mode="symmetric")

    LL, details = wavedec2(x, args.levels)
    lo, hi = np.percentile(LL, 0.5), np.percentile(LL, 99.5)
    out = np.clip((LL - lo) / (hi - lo), 0, 1)
    for LH, HL, HH in details:
        out = np.block([
            [[out], [scale(LH, args.style, args.pct, args.gamma)]],
            [[scale(HL, args.style, args.pct, args.gamma)], [scale(HH, args.style, args.pct, args.gamma)]],
        ])

    if args.line:
        h, w = LL.shape[:2]
        for _ in range(args.levels):
            out[h - args.line // 2 : h + (args.line + 1) // 2, : 2 * w] = 1
            out[: 2 * h, w - args.line // 2 : w + (args.line + 1) // 2] = 1
            h, w = 2 * h, 2 * w

    img = Image.fromarray((255 * out).round().astype(np.uint8))
    img.save(args.dst, quality=85)


if __name__ == "__main__":
    main()
