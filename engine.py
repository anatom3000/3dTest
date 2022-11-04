from typing import Optional

import numpy as np


class Camera:

    def update_fov(self, fov: np.ndarray | float) -> None:

        if isinstance(fov, (float, int)):
            fov = np.array([fov, fov / self.resolution[0] * self.resolution[1]])

        self.fov = fov

        fov = fov / 180 * np.pi

        x = 2 * self.focal_lenght * np.tan(fov / 2.0)

        self.camera_plane = np.array([
            x[0],
            x[1],
            self.focal_lenght,
        ])

    def update_focal(self, length: float) -> None:
        self.camera_plane *= length / self.focal_lenght
        self.focal_lenght = length

    def __init__(self, resolution: np.ndarray, fov: float = 90.0, focal_length: float = 1.0):
        self.resolution = resolution
        self.focal_lenght = focal_length

        self.update_fov(fov)

        self.position = np.zeros(3, dtype=float)
        self.orientation = np.zeros(3, dtype=float)

    def to_camera_space(self, point: np.ndarray) -> np.ndarray:
        sin_x = np.sin(self.orientation[2])
        sin_y = np.sin(self.orientation[1])
        cos_x = np.cos(self.orientation[2])
        cos_y = np.cos(self.orientation[1])
        sin_z = np.sin(self.orientation[0])
        cos_z = np.cos(self.orientation[0])

        transformed = point - self.position

        # TODO: rewrite camera space rotation
        transformed[:2] = np.matmul(
            np.array([cos_z, -sin_z, sin_z, cos_z]).reshape((2, 2)),
            transformed[:2]
        )  # yaw
        transformed[::2] = np.matmul(
            np.array([cos_y, -sin_y, sin_y, cos_y]).reshape((2, 2)),
            transformed[::2]
        )  # pitch
        transformed[1:] = np.matmul(
            np.array([cos_x, -sin_x, sin_x, cos_x]).reshape((2, 2)),
            transformed[1:]
        )  # roll

        return transformed

    def project_camera_space_point(self, point: np.ndarray) -> Optional[np.ndarray]:

        if point[2] < 0:
            return None

        return (point[:2] * self.focal_lenght) / (point[2]) / self.camera_plane[:2]

    def project_point(self, point: np.ndarray) -> Optional[np.ndarray]:

        camera_space_point = self.to_camera_space(point)

        if camera_space_point[2] < 0:
            return None

        return self.project_camera_space_point(camera_space_point)

    def project_line(self, start_point, end_point) -> Optional[tuple[np.ndarray, np.ndarray]]:
        cs_start = self.to_camera_space(start_point)
        cs_end = self.to_camera_space(end_point)

        if cs_start[2] >= self.focal_lenght:
            if cs_end[2] >= self.focal_lenght:
                return self.project_camera_space_point(cs_start), self.project_camera_space_point(cs_end)
            elif 0.0 < cs_end[2] < self.focal_lenght:
                return self.project_camera_space_point(cs_start), self.project_camera_space_point(cs_end)
            else:
                intersection = cs_start[2] - self.focal_lenght
                intersection *= cs_end[:2] - cs_start[:2]

                intersection /= cs_end[2] - cs_start[2]
                intersection += cs_start[:2]

                return self.project_camera_space_point(cs_start), intersection

        elif 0.0 < cs_start[2] < self.focal_lenght:
            if cs_end[2] >= self.focal_lenght:
                return self.project_camera_space_point(cs_start), self.project_camera_space_point(cs_end)
            elif 0.0 < cs_end[2] < self.focal_lenght:
                return self.project_camera_space_point(cs_start), self.project_camera_space_point(cs_end)
            else:
                intersection = cs_start[2] - self.focal_lenght
                intersection *= cs_end[:2] - cs_start[:2]

                intersection /= cs_end[2] - cs_start[2]
                intersection += cs_start[:2]

        else:
            if cs_end[2] >= self.focal_lenght:
                intersection = cs_end[2] - self.focal_lenght
                intersection *= cs_end[:2] - cs_start[:2]

                intersection /= cs_end[2] - cs_start[2]
                intersection += cs_end[:2]
            elif 0.0 < cs_end[2] < self.focal_lenght:
                intersection = cs_end[2] - self.focal_lenght
                intersection *= cs_end[:2] - cs_start[:2]

                intersection /= cs_end[2] - cs_start[2]
                intersection += cs_end[:2]
            else:
                return None

