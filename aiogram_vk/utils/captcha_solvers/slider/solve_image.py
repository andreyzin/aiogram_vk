import base64
from io import BytesIO

import numpy as np
from PIL import Image


def score_canvas(img: Image.Image, N: int = 5) -> int:
    """
    Считает разрывы по стыкам NxN тайлов.
    Возвращает целочисленное значение ошибки (чем меньше, тем лучше).
    """
    arr = np.array(img.convert("RGB"))
    h, w, _ = arr.shape
    cell_w = w // N
    cell_h = h // N

    diff = 0

    # вертикальные стыки
    for gy in range(N):
        for gx in range(1, N):
            x = gx * cell_w
            y1, y2 = gy * cell_h, (gy + 1) * cell_h
            left = arr[y1:y2, x - 1, :]
            right = arr[y1:y2, x, :]
            diff += np.abs(left - right).sum()

    # горизонтальные стыки
    for gx in range(N):
        for gy in range(1, N):
            y = gy * cell_h
            x1, x2 = gx * cell_w, (gx + 1) * cell_w
            top = arr[y - 1, x1:x2, :]
            bottom = arr[y, x1:x2, :]
            diff += np.abs(top - bottom).sum()

    return int(diff)


def build_tiles(w, h, N=5):
    """Вернёт список тайлов (sx, sy, sw, sh)."""
    bx = [round(i * w / N) for i in range(N + 1)]
    by = [round(i * h / N) for i in range(N + 1)]
    tiles = []
    for ty in range(N):
        for tx in range(N):
            sx, sy = bx[tx], by[ty]
            sw, sh = bx[tx + 1] - bx[tx], by[ty + 1] - by[ty]
            tiles.append((sx, sy, sw, sh))
    return tiles, bx, by


def draw_with_steps(img: Image.Image, swap_array, A: int, N=5) -> Image.Image:
    """Возвращает новое изображение после применения A шагов из swap_array."""
    w, h = img.size
    tiles, bx, by = build_tiles(w, h, N)
    perm = list(range(N * N))

    max_len = min(A * 2, len(swap_array))
    for i in range(0, max_len, 2):
        a, b = swap_array[i], swap_array[i + 1]
        if 0 <= a < len(perm) and 0 <= b < len(perm):
            perm[a], perm[b] = perm[b], perm[a]

    out = Image.new("RGB", (w, h))
    d = 0
    for dy in range(N):
        for dx in range(N):
            destX, destY = bx[dx], by[dy]
            destW, destH = bx[dx + 1] - bx[dx], by[dy + 1] - by[dy]

            src_index = perm[d]
            sx, sy, sw, sh = tiles[src_index]
            tile = img.crop((sx, sy, sx + sw, sy + sh))
            tile = tile.resize((destW, destH))
            out.paste(tile, (destX, destY))
            d += 1
    return out


def find_best_A(img: Image.Image, swap_array, maxA=50, N=5):
    best_A, best_score = 0, float("inf")
    best_candidate = None
    for A in range(maxA):

        candidate = draw_with_steps(img, swap_array, A, N)
        sc = score_canvas(candidate, N)
        if sc < best_score:
            best_candidate = candidate
            best_score, best_A = sc, A
    if best_candidate:
        best_candidate.show()
    answer = swap_array[: best_A * 2]
    return best_A, answer


def solve_image(base64_img: str, steps: list[int], N=5):
    img = Image.open(BytesIO(base64.b64decode(base64_img)))
    best_A, answer = find_best_A(img, steps[1:], maxA=50, N=5)
    return best_A, answer
