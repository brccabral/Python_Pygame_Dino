import os
import sys
import pygame


WIDTH = 623
HEIGHT = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()


class Dino:
    def __init__(self):
        self.width = 44
        self.height = 44
        self.x = 10
        self.y = 80
        self.texture_num = 0
        self.textures = []
        self.preload_textures()
        self.set_texture()
        self.show()

    def update(self):
        self.texture_num = (self.texture_num + 1) % 3

    def show(self):
        self.set_texture()
        screen.blit(self.texture, (self.x, self.y))

    def preload_textures(self):
        for i in range(3):
            path = os.path.join("assets", "images", f"dino{i}.png")
            texture = pygame.image.load(path)
            texture = pygame.transform.scale(texture, (self.width, self.height))
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


def main():
    game = Game()
    dino = game.dino
    dt = 0

    while True:
        # background
        screen.fill("black")
        game.bg.update(-game.speed * dt)
        game.bg.show()

        # dino
        dino.update()
        dino.show()

        for event in pygame.event.get([pygame.QUIT]):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
