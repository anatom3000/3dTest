import numpy as np
import pygame
from pygame.locals import *

from engine import Camera

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()


class MainWindow:
    resolution = np.array([960, 720])
    uv_to_screen_factor = resolution * np.array([1, -1])
    font = pygame.font.Font(pygame.font.get_default_font(), 12)

    label_mode_names = [
        "Screen Space",
        "Camera Space",
        "World Space"
    ]

    _vertex_buffer = np.array([
        [-1, -1, -1],
        [1, -1, -1],
        [-1, 1, -1],
        [1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
        [-1, 1, 1],
        [1, 1, 1],
    ], dtype=float)
    _edge_buffer = [
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
        (0, 7),
        (1, 6),
        (2, 5),
        (3, 4)
    ]

    vertex_buffer = np.array([[x, y, z] for z in range(2) for x in range(2) for y in range(2)], dtype=float)
    print(vertex_buffer)
    print(len(vertex_buffer))

    edge_buffer = [
        (start, 4+start) for start in range(4)
    ]

    mouse_sensitivity = 1 / 100.0

    def __init__(self):

        self.camera = Camera(self.resolution, focal_length=1.0, fov=120)

        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()

        self.display_labels = True
        self.label_mode = 0

        self.factor = 1.0

        self.dt = 1.0

    def handle_keypresses(self):
        keys = pygame.key.get_pressed()

        if keys[K_LCTRL]:
            player_speed = 5.0
        else:
            player_speed = 2.0

        if keys[K_z]:
            self.camera.position += player_speed * self.dt * np.array(
                [np.sin(self.camera.orientation[1]), 0.0, np.cos(self.camera.orientation[1])],
                dtype=float)

        if keys[K_s]:
            self.camera.position += player_speed * self.dt * np.array(
                [-np.sin(self.camera.orientation[1]), 0.0, -np.cos(self.camera.orientation[1])], dtype=float)

        if keys[K_q]:
            self.camera.position += player_speed * self.dt * np.array(
                [-np.cos(self.camera.orientation[1]), 0.0, np.sin(self.camera.orientation[1])],
                dtype=float)

        if keys[K_d]:
            self.camera.position += player_speed * self.dt * np.array(
                [np.cos(self.camera.orientation[1]), 0.0, -np.sin(self.camera.orientation[1])],
                dtype=float)

        if keys[K_LSHIFT]:
            self.camera.position += player_speed * self.dt * np.array([0, -1, 0])

        if keys[K_SPACE]:
            self.camera.position += player_speed * self.dt * np.array([0, 1, 0])

        if keys[K_o]:
            self.factor = 1.0

    def draw_screen(self):
        self.screen.fill(BLACK)

        for start, end in self.edge_buffer:
            projected_line = self.camera.project_line(self.vertex_buffer[start], self.vertex_buffer[end])

            # print(f"{projected_start = }, {projected_end = }")

            if projected_line is None:
                continue

            projected_start, projected_end = projected_line

            if projected_start is None or projected_end is None:
                continue

            projected_start *= self.uv_to_screen_factor / self.factor
            projected_end *= self.uv_to_screen_factor / self.factor

            projected_start += self.resolution / 2
            projected_end += self.resolution / 2

            pygame.draw.line(self.screen, WHITE, projected_start, projected_end)

        if self.display_labels:
            for pt in self.vertex_buffer:
                screen_pos = self.camera.project_point(pt)

                if screen_pos is not None:
                    if self.label_mode == 0:
                        rsp = (screen_pos * self.uv_to_screen_factor + self.resolution / 2).astype(int)
                        txt = self.font.render(f"({rsp[0]}, {rsp[1]})", True, WHITE)
                    elif self.label_mode == 1:
                        cam_space_pos = self.camera.to_camera_space(pt).round(2)
                        txt = self.font.render(f"({cam_space_pos[0]}, {cam_space_pos[1]}, {cam_space_pos[2]})", True,
                                               WHITE)
                    else:
                        rpt = pt.round(2)
                        txt = self.font.render(f"({rpt[0]}, {rpt[1]}, {rpt[2]})", True, WHITE)

                    txt_rect = txt.get_rect()
                    txt_rect.topleft = np.maximum(
                        0.0,
                        screen_pos * self.uv_to_screen_factor / self.factor + self.resolution / 2,
                    )
                    txt_rect.bottomright = np.minimum(self.resolution, txt_rect.bottomright)


                    self.screen.blit(txt, txt_rect)

        pygame.display.flip()

    def update(self):
        self.dt = self.clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == MOUSEMOTION:
                if pygame.mouse.get_pressed(3)[0]:
                    self.camera.orientation += np.array([
                        0.0,
                        event.rel[0] * self.mouse_sensitivity * self.resolution[1] / self.resolution[0],
                        0.0  # event.rel[1] * self.mouse_sensitivity,
                    ])

            if event.type == MOUSEWHEEL:
                if event.y > 0:
                    self.factor /= 1.05
                else:
                    self.factor *= 1.05

            if event.type == KEYUP:
                if event.key == K_l:
                    self.display_labels = not self.display_labels
                if event.key == K_TAB:
                    self.label_mode = (self.label_mode + 1) % 3

        self.handle_keypresses()

        self.draw_screen()

        rounded_pos = list(map(lambda x: round(x, 2), self.camera.position))

        pygame.display.set_caption(f"Position: {rounded_pos} | Mouse: {pygame.mouse.get_pos()} | {self.label_mode_names[self.label_mode]}")

        return True

    def mainloop(self):
        running = True
        while running:
            running = self.update()
        pygame.quit()

if __name__ == "__main__":
    win = MainWindow()
    win.mainloop()
