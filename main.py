import pygame
from PIL import Image
import random

class Tile:
    def __init__(self, img, side=32, rotate=0):
        img = pygame.image.load(img)
        img = pygame.transform.scale(img, (side, side))
        self.img = pygame.transform.rotate(img, rotate*90)
        self.len = side
        self.pil_img = Image.frombytes("RGB", (side, side), pygame.image.tostring(self.img, "RGB"))
        f = side//3
        e = f//2
        self.sides = [
            [self.pil_img.getpixel(((x*f)+e, e)) for x in range(3)],
            [self.pil_img.getpixel(((2*f)+e, (y*f)+e)) for y in range(3)],
            [self.pil_img.getpixel((((2-x)*f)+e, (2*f)+e)) for x in range(3)],
            [self.pil_img.getpixel((e, ((2-y)*f)+e)) for y in range(3)],
        ]

class Cell:
    def __init__(self, x, y, tiles:list[Tile], side=32):
        self.x = x
        self.y = y
        self.side = side
        self.tiles = tiles
        self.options = tiles.copy()
        self.current = None


class WFC:
    def __init__(self, tiles:list):
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Wave Function Collapse")
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.tiles = tiles
        self.side = 32
        self.grid = [[Cell(x, y, self.tiles, self.side) for x in range(self.width//self.side)] for y in range(self.height//self.side)]

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((0, 0, 0))

            flat_grid = [x for y in self.grid for x in y if x.current is None]
            if len(flat_grid) >= 1:
                chosen_one = random.choice(flat_grid)
                o = random.choice(chosen_one.options)
                chosen_one.current = o

            for row in self.grid:
                for cell in row:
                    if cell.current is None:
                        pygame.draw.rect(self.screen, (255, 255, 255), (cell.x*self.side, cell.y*self.side, self.side, self.side), 2)
                    else:
                        self.screen.blit(cell.current.img, (cell.x*self.side, cell.y*self.side))

            self.clock.tick(60)
            pygame.display.update()

if __name__ == '__main__':
    tiles = []
    tiles.append(Tile('assets/roads/0.png'))
    tiles.append(Tile('assets/roads/1.png'))
    tiles.append(Tile('assets/roads/1.png', rotate=1))
    tiles.append(Tile('assets/roads/2.png'))
    tiles.append(Tile('assets/roads/2.png', rotate=1))
    tiles.append(Tile('assets/roads/2.png', rotate=2))
    tiles.append(Tile('assets/roads/2.png', rotate=3))
    tiles.append(Tile('assets/roads/3.png'))
    tiles.append(Tile('assets/roads/3.png', rotate=1))
    tiles.append(Tile('assets/roads/3.png', rotate=2))
    tiles.append(Tile('assets/roads/3.png', rotate=3))
    tiles.append(Tile('assets/roads/4.png'))
    instance = WFC(tiles)
    instance.run()