from __future__ import annotations

import numpy as np
import pygame

from viewport import Viewport


class Renderer:
    def __init__(self, camera: Viewport, vertex_buffer: np.ndarray, edge_buffer: list[tuple[int, int]], edge_colors: list[tuple[int, int, int]]):
        self.vertex_buffer = vertex_buffer
        self.edge_buffer = edge_buffer
        self.edge_colors = edge_colors

        self.camera = camera

    def render(self, surface: pygame.Surface):
        for (start, end), color in zip(self.edge_buffer, self.edge_colors):

            projected_line = self.camera.project_line(self.vertex_buffer[start], self.vertex_buffer[end])

            if projected_line is None:
                continue
            projected_start, projected_end = projected_line
            if projected_start is None or projected_end is None:
                continue

            pygame.draw.line(surface, color, projected_start, projected_end)
