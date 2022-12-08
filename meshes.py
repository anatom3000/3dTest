from __future__ import annotations

import numpy as np


def lerp(start: float | np.ndarray, end: float | np.ndarray, t: float):
    return (1 - t) * start + t * end


def index_to_vertex(i: int):
    return np.ndarray([lerp()])


def grid(length: int, width: int, start_corner: np.ndarray, end_corner: np.ndarray):
    n = length * width
    indices = np.arange(n)

    heights = np.repeat(start_corner[2], n)
    lengths: np.ndarray = lerp(start_corner[1], end_corner[1], (indices % width) / (width - 1))
    widths: np.ndarray = lerp(start_corner[0], end_corner[0], (indices // width) / (length - 1))

    vertex_buffer = np.vstack((widths, lengths, heights)).T  # ordered grid of points
