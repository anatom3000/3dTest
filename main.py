import numpy as np
import pygame
from pygame.locals import *

from engine import Camera

RESOLUTION = np.array([960, 720])
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

camera = Camera(RESOLUTION, focal_length=1.0, fov=120)

vertex_buffer = np.array([
    [-1, -1, 1],
    [1, -1, 1],
    [-1, 1, 1],
    [1, 1, 1],
    [-1, -1, 2],
    [1, -1, 2],
    [-1, 1, 2],
    [1, 1, 2],
], dtype=float)

edge_buffer = [
    (0, 1),
    (0, 2),
    (0, 4),
    (1, 3),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 6),
    (5, 7),
    (6, 7),
    # (0, 7),
    # (1, 6),
    # (2, 5),
    # (3, 4)
]

# points = np.array([
#     [1.0, 1.0, 1.0],
#     [-1.0, 1.0, 1.0],
#     [1.0, -1.0, 1.0],
#     [-1.0, -1.0, 1.0],
# ])
#
# edge_buffer = [
#     (0, 1),
#     (0, 2),
#     (0, 3)
# ]

screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
uv_to_screen_factor = RESOLUTION * np.array([1, -1])

updating = False
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYUP:
            camera.position += np.array([1.0, 0.0, 0.0], dtype=float)

    screen.fill(BLACK)

    for start, end in edge_buffer:
        projected_start = camera.project(vertex_buffer[start])
        projected_end = camera.project(vertex_buffer[end])

        # print(f"{projected_start = }, {projected_end = }")

        projected_start *= uv_to_screen_factor
        projected_end *= uv_to_screen_factor

        projected_start += RESOLUTION / 2
        projected_end += RESOLUTION / 2

        if projected_start is not None and projected_end is not None:
            pygame.draw.line(screen, WHITE, projected_start, projected_end)

    pygame.display.flip()

pygame.quit()
