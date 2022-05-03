import math
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


class Collision:
    def between(self, obj1, obj2):
        distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
        return distance < 35


class Score:
    def __init__(self, high_score: int):
        self.high_score = high_score
        self.act = 0
        self.font = pygame.font.SysFont("monospace", 18)
        self.show()

    def show(self):
        self.label = self.font.render(f"HI {self.high_score} {self.act}", True, "black")
        label_width = self.label.get_rect().width
        screen.blit(self.label, (WIDTH - label_width - 10, 10))

    def update(self, loop: int):
        self.act = loop // 10
        if self.act > self.high_score:
            self.high_score = self.act


class Game:
    def __init__(self):
        self.bg = BG(0, 0)
        self.speed = 180

        self.dino = Dino()

        self.obstacles: List[Cactus] = []

        self.collision = Collision()
        self.is_playing = False

        self.score = Score(0)

    def start(self):
        self.is_playing = True

    def over(self):
        self.is_playing = False

    def spawn_cactus(self):
        if self.obstacles:
            prev_cactus = self.obstacles[-1]
            # 84 = minimum space between obstacles
            px = int(prev_cactus.x)
            x = random.randint(
                px + self.dino.width + 84, WIDTH + px + self.dino.width + 84
            )
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
        if game.is_playing:
            # background
            screen.fill("black")
            game.bg.update(-game.speed * dt)
            game.bg.show()

            # dino
            dino.update()
            dino.show()

            # cactus
            if loop % 100 == 0:
                game.spawn_cactus()

            for cactus in game.obstacles:
                cactus.update(-game.speed * dt)
                cactus.show()

                # collision
                if game.collision.between(dino, cactus):
                    game.over()

            # score
            game.score.update(loop)
            game.score.show()

        for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game.is_playing:
                        game.start()
                    else:
                        dino.jump()

        pygame.display.update()
        dt = clock.tick(60) / 1000
        loop += 1


if __name__ == "__main__":
    main()
