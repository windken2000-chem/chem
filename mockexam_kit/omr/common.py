import numpy as np
from PIL import Image
import os; D=os.environ.get('MOCK_BASE','.').rstrip('/')+'/'
import glob
ROT = int(os.environ.get('MOCK_ROTATE', '0'))   # 掃描整疊上下顛倒時設 180
ROT_K = int(os.environ.get('MOCK_ROTATE_K', '0'))  # 只有反面（偶數頁）上下顛倒時設 180（雙面掃描常見）
def page_path(i):
    for fmt in ('{:02d}', '{:03d}', '{:d}'):
        p = D + 'raw/s-' + fmt.format(i) + '.pgm'
        if os.path.exists(p): return p
    raise FileNotFoundError(i)
NPAGES = len(glob.glob(D + 'raw/s-*.pgm'))
def load_u8(i):
    im = Image.open(page_path(i))
    r = (ROT + (ROT_K if i % 2 == 0 else 0)) % 360
    if r: im = im.rotate(r)
    return np.asarray(im, dtype=np.uint8)
def load(i):
    return 1.0 - load_u8(i).astype(np.float32)/255.
def down(a, f=4):
    h, w = a.shape; h -= h % f; w -= w % f
    return a[:h, :w].reshape(h // f, f, w // f, f).mean(axis=(1, 3))
def phase_shift(a, b):
    A = np.fft.fft2(a); B = np.fft.fft2(b)
    R = A * np.conj(B); R /= np.abs(R) + 1e-9
    r = np.fft.ifft2(R).real
    dy, dx = np.unravel_index(np.argmax(r), r.shape)
    if dy > a.shape[0] // 2: dy -= a.shape[0]
    if dx > a.shape[1] // 2: dx -= a.shape[1]
    return int(dy), int(dx), float(r.max())
