from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class Edge:
    start: np.ndarray
    end: np.ndarray
    color: Optional[np.ndarray] = None


@dataclass
class Triangle:
    normal: np.ndarray
    vertices: list[np.ndarray]
    color: Optional[np.ndarray] = None

    _edges = None

    @property
    def edges(self) -> list[Edge]:
        if self._edges is None:
            self._edges = [
                Edge(self.vertices[0], self.vertices[1], self.color),
                Edge(self.vertices[1], self.vertices[2], self.color),
                Edge(self.vertices[2], self.vertices[0], self.color),
            ]

        return self._edges

    def apply_transform(self, transform_matrix: np.ndarray = None, offset_vector: np.ndarray = None):
        if transform_matrix is None:
            transform_matrix = np.eye(3)
        if offset_vector is None:
            offset_vector = np.zeros(3, dtype=np.float32)

        self.vertices = [np.matmul(transform_matrix, v) + offset_vector for v in self.vertices]
        self._edges = None


@dataclass
class Object:
    triangles: list[Triangle]

    _center = None

    @property
    def center(self) -> np.ndarray:
        if self._center is None:
            points = []
            for t in self.triangles:
                points.extend(t.vertices)
            self._center = np.sum(np.array(points), axis=0) / len(points)

        return self._center

    @center.setter
    def center(self, value: np.ndarray):
        self.move(value - self.center)

    def apply_transform(self, transform_matrix: np.ndarray = None, offset_vector: np.ndarray = None) -> Self:
        for t in self.triangles:
            t.apply_transform(transform_matrix, offset_vector)
        self._center = None
        return self

    def rotate(self, orientation: np.ndarray, center: np.ndarray = None) -> Self:
        if center is None:
            center = self.center

        sin_x = np.sin(orientation[2])
        sin_y = np.sin(orientation[1])
        cos_x = np.cos(orientation[2])
        cos_y = np.cos(orientation[1])
        sin_z = np.sin(orientation[0])
        cos_z = np.cos(orientation[0])

        rot_yaw_matrix = np.array([
            [cos_z, -sin_z, 0],
            [sin_z, cos_z, 0],
            [0, 0, 1]
        ])

        rot_pitch_matrix = np.array([
            [cos_y, 0, sin_y],
            [0, 1, 0],
            [-sin_y, 0, cos_y]
        ])

        rot_roll_matrix = np.array([
            [1, 0, 0],
            [0, cos_x, -sin_x],
            [0, sin_x, cos_x]
        ])

        rotation_matrix = np.matmul(rot_roll_matrix, np.matmul(rot_pitch_matrix, rot_yaw_matrix))

        self.apply_transform(offset_vector=-center)

        return self.apply_transform(rotation_matrix, center)

    def scale(self, scale_or_x: float, y: float = None, z: float = None, center: np.ndarray = None) -> Self:
        if center is None:
            center = self.center

        if y is None and z is None:
            y = z = scale_or_x

        self.apply_transform(offset_vector=-center)

        return self.apply_transform(np.array([
            [scale_or_x, 0, 0],
            [0, y, 0],
            [0, 0, z]
        ]), center)

    def move(self, offset: np.ndarray) -> Self:
        return self.apply_transform(offset_vector=offset)

    def set_center(self, position: np.ndarray):
        self.center = position
        return self

    def flip(self, x: bool = False, y: bool = False, z: bool = False, center: np.ndarray = None) -> Self:
        if center is None:
            center = self.center

        self.apply_transform(offset_vector=-center)

        return self.apply_transform(np.array([
            [(-1 if x else 1), 0, 0],
            [0, (-1 if y else 1), 0],
            [0, 0, (-1 if z else 1)],
        ]), center)

    def normalize_size(self, min_coords: np.ndarray = None, max_coords: np.ndarray = None) -> Self:
        pass
