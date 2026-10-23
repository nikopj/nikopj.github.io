// Hover animation for the index page headshot (#profpic): a CDF 9/7 (JPEG2000)
// wavelet pyramid of each RGB channel, one more level at a time while hovered,
// and back up to the original image on mouseout. Level k is held for
// STEP_MS * DECAY^(k-1), so decomposition speeds up and recomposition slows
// down. The frames are computed in the browser once the page has loaded, then
// swapped in as the img's src. Display settings match headshot_wavelet.py.
(function () {
  const LEVELS = 6, STEP_MS = 100, DECAY = 0.6;
  const PCT = 0.99, GAMMA = 0.75, LINE = 3;
  const A = -1.586134342, B = -0.05298011854, G = 0.8829110762, D = 0.4435068522, Z = 1.149604398;

  const img = document.getElementById("profpic");
  const frames = [img.getAttribute("src")];
  const decoded = [];  // keep the decoded frames alive so swaps don't flicker
  let level = 0, target = 0, timer = null;

  // one level of the 1D DWT on n samples of x (start off, stride st), lowpass
  // written to the first half and highpass to the second, symmetric boundaries
  function lift(x, off, st, n, buf) {
    const h = n >> 1;
    for (let i = 0; i < h; i++) {
      buf[i] = x[off + 2 * i * st];
      buf[h + i] = x[off + (2 * i + 1) * st];
    }
    const s = (i) => buf[Math.min(i, h - 1)], d = (i) => buf[h + Math.max(i, 0)];
    for (let i = 0; i < h; i++) buf[h + i] += A * (s(i) + s(i + 1));
    for (let i = 0; i < h; i++) buf[i] += B * (d(i - 1) + d(i));
    for (let i = 0; i < h; i++) buf[h + i] += G * (s(i) + s(i + 1));
    for (let i = 0; i < h; i++) buf[i] += D * (d(i - 1) + d(i));
    for (let i = 0; i < h; i++) {
      x[off + i * st] = buf[i] * Z;
      x[off + (h + i) * st] = buf[h + i] / Z;
    }
  }

  async function build() {
    const src = new Image();
    src.src = frames[0];
    await src.decode();
    const W = src.naturalWidth, H = src.naturalHeight;
    const canvas = document.createElement("canvas");
    canvas.width = W;
    canvas.height = H;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(src, 0, 0);
    const frame = ctx.getImageData(0, 0, W, H);
    const px = frame.data;

    // channel planes, symmetric-padded so every level halves evenly
    const m = 1 << LEVELS, Wp = Math.ceil(W / m) * m, Hp = Math.ceil(H / m) * m;
    const planes = [0, 1, 2].map((c) => {
      const p = new Float32Array(Wp * Hp);
      for (let y = 0; y < Hp; y++) {
        const sy = y < H ? y : 2 * H - 1 - y;
        for (let x = 0; x < Wp; x++) {
          const sx = x < W ? x : 2 * W - 1 - x;
          p[y * Wp + x] = px[4 * (sy * W + sx) + c] / 255;
        }
      }
      return p;
    });

    // q-quantile of f(coefficient) over a rect, jointly across R, G, B
    const quantile = (x0, y0, w, h, f, q) => {
      const v = new Float32Array(3 * w * h);
      let k = 0;
      for (const p of planes)
        for (let y = y0; y < y0 + h; y++)
          for (let x = x0; x < x0 + w; x++) v[k++] = f(p[y * Wp + x]);
      v.sort();
      return v[Math.floor(q * (v.length - 1))];
    };
    const paint = (x0, y0, w, h, map) => {
      for (let y = y0; y < Math.min(y0 + h, H); y++)
        for (let x = x0; x < Math.min(x0 + w, W); x++)
          for (let c = 0; c < 3; c++) px[4 * (y * W + x) + c] = 255 * map(planes[c][y * Wp + x]);
    };
    const detail = (x0, y0, w, h) => {
      const s = quantile(x0, y0, w, h, Math.abs, PCT);
      paint(x0, y0, w, h, (v) => Math.min(Math.abs(v) / s, 1) ** GAMMA);
    };
    const fill = (x0, y0, w, h) => {
      for (let y = y0; y < Math.min(y0 + h, H); y++)
        for (let x = x0; x < Math.min(x0 + w, W); x++)
          for (let c = 0; c < 3; c++) px[4 * (y * W + x) + c] = 255;
    };

    const buf = new Float32Array(Math.max(Wp, Hp));
    let w = Wp, h = Hp;
    for (let k = 1; k <= LEVELS; k++) {
      for (const p of planes) {
        for (let y = 0; y < h; y++) lift(p, y * Wp, 1, w, buf);
        for (let x = 0; x < w; x++) lift(p, x, Wp, h, buf);
      }
      w >>= 1;
      h >>= 1;
      detail(w, 0, w, h);
      detail(0, h, w, h);
      detail(w, h, w, h);
      const lo = quantile(0, 0, w, h, (v) => v, 0.005), hi = quantile(0, 0, w, h, (v) => v, 0.995);
      paint(0, 0, w, h, (v) => (v - lo) / (hi - lo));
      // subband separators for every level so far (this frame's paint covers
      // the edge of the previous level's lines)
      for (let j = 0, lw = w, lh = h; j < k; j++, lw *= 2, lh *= 2) {
        const a = LINE >> 1;
        fill(0, lh - a, 2 * lw, LINE);
        fill(lw - a, 0, LINE, 2 * lh);
      }

      ctx.putImageData(frame, 0, 0);
      const blob = await new Promise((r) => canvas.toBlob(r, "image/jpeg", 0.9));
      const im = new Image();
      im.src = URL.createObjectURL(blob);
      await im.decode();
      decoded.push(im);
      frames.push(im.src);
      if (!timer) step();  // catch up if hovered before this frame was ready
    }
  }

  function step() {
    const next = level + Math.sign(target - level);
    if (next === level || next >= frames.length) {
      timer = null;
      return;
    }
    level = next;
    img.src = frames[level];
    timer = level === target ? null : setTimeout(step, STEP_MS * DECAY ** (level - 1));
  }

  function go(t) {
    target = t;
    if (!timer) step();
  }

  img.addEventListener("mouseenter", () => go(LEVELS));
  img.addEventListener("mouseleave", () => go(0));
  if (document.readyState === "complete") build();
  else window.addEventListener("load", build);
})();
