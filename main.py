import pygame
from PIL import Image
import random

class Tile:
    def __init__(self, img, side, rotate=0):
        img = pygame.image.load(img)
        img = pygame.transform.rotate(img, rotate*90)
        self.pil_img = Image.frombytes("RGB", (img.get_width(), img.get_width()), pygame.image.tostring(img, "RGB"))
        self.img = pygame.transform.scale(img, (side, side))
        self.len = side
        f = img.get_width()//3
        e = f//2
        self.sides = [
            [self.pil_img.getpixel(((x*f)+e, e)) for x in range(3)],
            [self.pil_img.getpixel(((2*f)+e, (y*f)+e)) for y in range(3)],
            [self.pil_img.getpixel((((x)*f)+e, (2*f)+e)) for x in range(3)],
            [self.pil_img.getpixel((e, ((y)*f)+e)) for y in range(3)],
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
    def __init__(self, tiles:list[Tile], side=32):
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Wave Function Collapse")
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.tiles = tiles
        self.side = side
        self.grid = [[Cell(x, y, self.tiles, self.side) for x in range(self.width//self.side)] for y in range(self.height//self.side)]

        self.clock = pygame.time.Clock()
        self.running = True

    def get_options(self, tile: Tile, available:list[Tile], side:int):
        tile_color = tile.sides[side]
        ret_list = []
        for _tile in available:
            av_color = _tile.sides[(side+2)%4]
            if tile_color == av_color:
                ret_list.append(_tile)
        return ret_list
    
    def fix_neighbors(self, x, y):
        thing = self.grid[y][x]
        neighbours = [
            self.grid[y-1][x] if y > 0 else None,
            self.grid[y][x+1] if x < (self.width//self.side)-1 else None,
            self.grid[y+1][x] if y < (self.height//self.side)-1 else None,
            self.grid[y][x-1] if x > 0 else None
        ]
        for index, cell in enumerate(neighbours):
            if cell:
                if cell.current is None:
                    new = self.get_options(thing.current, cell.options, index)
                    cell.options = new

    def restart(self):
        self.grid = [[Cell(x, y, self.tiles, self.side) for x in range(self.width//self.side)] for y in range(self.height//self.side)]

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
            self.screen.fill((0, 0, 0))

            flat_grid = [x for y in self.grid for x in y if x.current is None]
            flat_grid.sort(key=lambda x: len(x.options))
            if len(flat_grid) >= 1:
                chosen = flat_grid[0]
                o = random.choice(chosen.options)
                chosen.options.remove(o)
                chosen.current = o
                self.fix_neighbors(chosen.x, chosen.y)

            for row in self.grid:
                for cell in row:
                    if cell.current:
                        self.screen.blit(cell.current.img, (cell.x*self.side, cell.y*self.side))

            self.clock.tick(60)
            pygame.display.update()

if __name__ == '__main__':
    tiles = []
    side_=10
    tiles.append(Tile('assets/roads/0.png', side_))
    tiles.append(Tile('assets/roads/1.png', side_))
    tiles.append(Tile('assets/roads/1.png', side_, rotate=1))
    tiles.append(Tile('assets/roads/2.png', side_))
    tiles.append(Tile('assets/roads/2.png', side_, rotate=1))
    tiles.append(Tile('assets/roads/2.png', side_, rotate=2))
    tiles.append(Tile('assets/roads/2.png', side_, rotate=3))
    tiles.append(Tile('assets/roads/3.png', side_))
    tiles.append(Tile('assets/roads/3.png', side_, rotate=1))
    tiles.append(Tile('assets/roads/3.png', side_, rotate=2))
    tiles.append(Tile('assets/roads/3.png', side_, rotate=3))
    tiles.append(Tile('assets/roads/4.png', side_))
    instance = WFC(tiles, side_)
    instance.run()