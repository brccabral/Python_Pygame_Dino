import os
import random
import sys
from typing import List
import pygame


WIDTH = 623
HEIGHT = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()


class Cactus:
    def __init__(self, x: int):
        self.width = 44
        self.height = 44
        self.x = x
        self.y = 80
        self.set_texture()
        self.show()

    def update(self, dx: float):
        self.x += dx

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join("assets", "images", "cactus.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.texture.convert_alpha()


class Dino:
    def __init__(self):
        self.width = 44
        self.height = 44
        self.x = 10
        self.y = 80

        # animation
        self.texture_num = 0
        self.textures = []
        self.animation_speed = 0.1
        self.texture_float = 0

        # jump
        self.dy = 7
        self.gravity = 0
        self.fall_stop = self.y

        self.preload_textures()
        self.set_texture()
        self.show()

    def jump(self):
        self.gravity = -self.dy
        self.texture_num = 0

    def update(self):
        self.gravity += 0.3
        self.y += self.gravity

        if self.y >= self.fall_stop:
            self.y = self.fall_stop

            self.texture_float += self.animation_speed
            if self.texture_float >= 3:
                self.texture_float = 0
            self.texture_num = int(self.texture_float)  # round floor

    def show(self):
        self.set_texture()
        screen.blit(self.texture, (self.x, self.y))

    def preload_textures(self):
        for i in range(3):
            path = os.path.join("assets", "images", f"dino{i}.png")
            texture = pygame.image.load(path)
            texture = pygame.transform.scale(texture, (self.width, self.height))
            texture.convert_alpha()
            self.textures.append(texture)

    def set_texture(self):
        self.texture = self.textures[self.texture_num]


class BG:
    def __init__(self, x: int, y: int):
        self.width = WIDTH
        self.height = HEIGHT
        self.surface = pygame.Surface((self.width * 2, self.height))
        self.x = x
        self.y = y
        self.set_texture()
        self.show()

    def update(self, dx: float):
        self.x += dx
        if self.x <= -WIDTH:
            self.x = 0

    def set_texture(self):
        path = os.path.join("assets", "images", "bg.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.texture.convert_alpha()
        self.surface.blit(self.texture, (0, 0))
        self.surface.blit(self.texture, (self.width, 0))

    def show(self):
        screen.blit(self.surface, (self.x, self.y))


class Game:
    def __init__(self):
        self.bg = BG(0, 0)
        self.speed = 120

        self.dino = Dino()

        self.obstacles: List[Cactus] = []

    def spawn_cactus(self):
        if self.obstacles:
            prev_cactus = self.obstacles[-1]
            # 44 = dino width
            # 84 = minimum space between obstacles
            px = int(prev_cactus.x)
            x = random.randint(px + 44 + 84, WIDTH + px + 44 + 84)
        else:
            x = random.randint(WIDTH + 100, WIDTH + 200)

        cactus = Cactus(x)
        self.obstacles.append(cactus)


def main():
    game = Game()
    dino = game.dino
    dt = 0
    loop = 0

    while True:
        # background
        screen.fill("black")
        game.bg.update(-game.speed * dt)
        game.bg.show()

        # dino
        dino.update()
        dino.show()

        # cactus
        if loop == 0:
            game.spawn_cactus()

        for cactus in game.obstacles:
            cactus.update(-game.speed * dt)
            cactus.show()

        for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        pygame.display.update()
        dt = clock.tick(60) / 1000
        loop += 1
        loop %= 100


if __name__ == "__main__":
    main()
