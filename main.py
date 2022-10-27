import numpy as np
import pygame
from pygame.locals import *

from engine import Camera

RESOLUTION = np.array([720, 720])
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

camera = Camera(RESOLUTION, focal_length=1.0, fov=120)

vertex_buffer = np.array([
    [-1, -1, 1],
    [1, -1, 1],
    [-1, 1, 1],
    [1, 1, 1],
    [-1, -1, 3],
    [1, -1, 3],
    [-1, 1, 3],
    [1, 1, 3],
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

mouse_sensitivity = 1/100.0

updating = False
running = True
while running:
    dt = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEMOTION:
            if any(pygame.mouse.get_pressed(3)):
                camera.orientation += np.array([
                    0.0,
                    event.rel[0] * mouse_sensitivity * RESOLUTION[1] / RESOLUTION[0],
                    0.0#event.rel[1] * mouse_sensitivity,
                ])

    keys = pygame.key.get_pressed()

    if keys[K_LCTRL]:
        player_speed = 5.0
    elif keys[K_LSHIFT]:
        player_speed = 0.5
    else:
        player_speed = 1.0

    if keys[K_z]:
        camera.position += player_speed * dt * np.array([np.sin(camera.orientation[1]), 0.0, np.cos(camera.orientation[1])],
                                                   dtype=float)

    if keys[K_s]:
        camera.position += player_speed * dt * np.array(
            [-np.sin(camera.orientation[1]), 0.0, -np.cos(camera.orientation[1])], dtype=float)

    if keys[K_q]:
        camera.position += player_speed * dt * np.array([-np.cos(camera.orientation[1]), 0.0, np.sin(camera.orientation[1])],
                                                   dtype=float)

    if keys[K_d]:
        camera.position += player_speed * dt * np.array([np.cos(camera.orientation[1]), 0.0, -np.sin(camera.orientation[1])],
                                                   dtype=float)

    screen.fill(BLACK)

    for start, end in edge_buffer:
        projected_start = camera.project(vertex_buffer[start])
        projected_end = camera.project(vertex_buffer[end])

        # print(f"{projected_start = }, {projected_end = }")

        if projected_start is not None and projected_end is not None:
            projected_start *= uv_to_screen_factor
            projected_end *= uv_to_screen_factor

            projected_start += RESOLUTION / 2
            projected_end += RESOLUTION / 2

            pygame.draw.line(screen, WHITE, projected_start, projected_end)

    pygame.display.flip()

pygame.quit()
