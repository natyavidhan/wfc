import pygame
from PIL import Image

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

class WFC:
    def __init__(self, tiles:list):
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Wave Function Collapse")
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.tiles = tiles

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((0, 0, 0))

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