import numpy as np


class Camera:

    def update_fov(self, fov: np.ndarray | float):

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

    def update_focal(self, length: float):
        self.camera_plane *= length / self.focal_lenght
        self.focal_lenght = length

    def __init__(self, resolution: np.ndarray, fov: float = 90.0, focal_length: float = 1.0):
        self.resolution = resolution
        self.focal_lenght = focal_length

        self.update_fov(fov)

        self.position = np.zeros(3, dtype=float)
        self.orientation = np.zeros(3, dtype=float)

    def to_camera_space(self, point: np.ndarray):
        sin_x = np.sin(self.orientation[2])
        sin_y = np.sin(self.orientation[1])
        sin_z = np.sin(self.orientation[0])
        cos_x = np.cos(self.orientation[2])
        cos_y = np.cos(self.orientation[1])
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

    def project(self, point: np.ndarray):

        transformed = self.to_camera_space(point)

        if transformed[2] < 0:
            return None

        return (transformed[:2] * self.focal_lenght) / (transformed[2] * self.focal_lenght) / self.camera_plane[:2]
