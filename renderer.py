from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pygame

from structures import Object
from viewport import Viewport


class Renderer:
    def __init__(self, camera: Viewport, objects: Iterable[Object] = None, default_vertex_color: np.ndarray = None):
        self.camera = camera
        self.objects = [] if objects is None else objects

        if default_vertex_color is None:
            default_vertex_color = 255 * np.ones(3, dtype=int)
        self.default_vertex_color = default_vertex_color
        # print(self.default_vertex_color)

        self.vertex_buffer = []
        self.edge_buffer = []
        self.edge_color_buffer = []

    def update_buffers(self):
        self.vertex_buffer = []
        self.edge_buffer = []
        self.edge_color_buffer = []

        for obj in self.objects:
            for triangle in obj.triangles:
                last_vertex = len(self.vertex_buffer)
                self.vertex_buffer.extend(triangle.vertices)
                self.edge_buffer.extend([
                    (last_vertex + 0, last_vertex + 1),
                    (last_vertex + 1, last_vertex + 2),
                    (last_vertex + 2, last_vertex + 0),
                ])

                if triangle.color is None:
                    self.edge_color_buffer.extend([self.default_vertex_color] * 3)
                else:
                    self.edge_color_buffer.extend([triangle.color] * 3)

    def render(self, surface: pygame.Surface, update: bool = True):
        if update:
            self.update_buffers()

        # print(self.vertex_buffer)
        # print(self.edge_buffer)
        # print(self.edge_color_buffer)

        for (start, end), color in zip(self.edge_buffer, self.edge_color_buffer):

            projected_line = self.camera.project_line(self.vertex_buffer[start], self.vertex_buffer[end])

            if projected_line is None:
                continue
            projected_start, projected_end = projected_line
            if projected_start is None or projected_end is None:
                continue

            # print(color)
            pygame.draw.line(surface, (255, 255, 255), projected_start, projected_end)
