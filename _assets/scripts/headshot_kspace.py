"""
Make the hover image for the index page headshot: the log-magnitude k-space
(centered 2D DFT) of each RGB channel, stacked back into an RGB image.

    python3 _assets/scripts/headshot_kspace.py _assets/headshot1.jpg _assets/headshotK.jpg

The three channel spectra are nearly identical, so the faithful result is close
to grayscale. --chroma > 1 amplifies each pixel's deviation from the channel
mean so the per-channel differences are visible (--chroma 1 is faithful).
"""
import argparse

import numpy as np
from PIL import Image


def periodic_component(u):
    # Moisan's periodic + smooth decomposition. Removes the bright "+" cross the
    # DFT puts on a photo whose opposite edges don't match (MRI k-space has none).
    H, W = u.shape
    v = np.zeros_like(u)
    v[0, :] += u[-1, :] - u[0, :]
    v[-1, :] += u[0, :] - u[-1, :]
    v[:, 0] += u[:, -1] - u[:, 0]
    v[:, -1] += u[:, 0] - u[:, -1]
    q = np.arange(H)[:, None]
    r = np.arange(W)[None, :]
    denom = 2 * np.cos(2 * np.pi * q / H) + 2 * np.cos(2 * np.pi * r / W) - 4
    denom[0, 0] = 1
    S = np.fft.fft2(v) / denom
    S[0, 0] = 0
    return u - np.real(np.fft.ifft2(S))


def log_kspace(x):
    out = np.empty_like(x)
    for c in range(x.shape[-1]):
        K = np.fft.fftshift(np.fft.fft2(periodic_component(x[..., c])))
        out[..., c] = np.log(np.abs(K) + 1e-8)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--lo", type=float, default=10, help="percentile mapped to black")
    p.add_argument("--hi", type=float, default=99.95, help="percentile mapped to white")
    p.add_argument("--chroma", type=float, default=3, help="color boost (1 = faithful)")
    args = p.parse_args()

    x = np.asarray(Image.open(args.src).convert("RGB"), dtype=np.float64) / 255
    L = log_kspace(x)

    # window each channel separately
    a = np.percentile(L, args.lo, axis=(0, 1), keepdims=True)
    b = np.percentile(L, args.hi, axis=(0, 1), keepdims=True)
    y = np.clip((L - a) / (b - a), 0, 1)

    m = y.mean(-1, keepdims=True)
    y = np.clip(m + args.chroma * (y - m), 0, 1)

    img = Image.fromarray((255 * y).round().astype(np.uint8))
    img.save(args.dst, quality=85)


if __name__ == "__main__":
    main()
