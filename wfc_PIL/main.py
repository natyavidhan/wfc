from PIL import Image
import PIL
import random

class Tile:
    def __init__(self, img, side=32, rotate=0, sides=None):
        img = Image.open(img)
        img = img.rotate(rotate*90, PIL.Image.Resampling.NEAREST, expand = 1)
        self.img = img.resize((side, side))
        self.len = side
        f = img.size[0]//3
        e = f//2
        self.sides = [
            [img.getpixel(((x*f)+e, e)) for x in range(3)],
            [img.getpixel(((2*f)+e, (y*f)+e)) for y in range(3)],
            [img.getpixel((((x)*f)+e, (2*f)+e)) for x in range(3)],
            [img.getpixel((e, ((y)*f)+e)) for y in range(3)],
        ] if not sides else sides

class Cell:
    def __init__(self, x, y, tiles:list[Tile], side=32):
        self.x = x
        self.y = y
        self.side = side
        self.tiles = tiles
        self.options = tiles.copy()
        self.current = None


class WFC:
    def __init__(self, width, height, tiles:list[Tile], side=32):
        self.screen = Image.new("RGB", (width, height))
        self.height = height
        self.width = width
        self.tiles = tiles
        self.side = side
        self.grid = [[Cell(x, y, self.tiles, self.side) for x in range(self.width//self.side)] for y in range(self.height//self.side)]
        self.length = len([x for y in self.grid for x in y])


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

    def run(self):
        while len([x for y in self.grid for x in y if x.current is not None]) < self.length:
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
                    self.screen.paste(cell.current.img, (cell.x*self.side, cell.y*self.side))
        self.screen.save("output.png")

if __name__ == '__main__':
    tiles = []
    side_=16
    tiles.append(Tile('../assets/better_roads/0.png', sides=[0, 0, 0, 0], side=side_))

    tiles.append(Tile('../assets/better_roads/1.png', sides=[1, 0, 1, 0], side=side_))
    tiles.append(Tile('../assets/better_roads/1.png', rotate=1, sides=[0, 1, 0, 1], side=side_))

    tiles.append(Tile('../assets/better_roads/2.png', sides=[0, 1, 1, 0], side=side_))
    tiles.append(Tile('../assets/better_roads/2.png', rotate=1, sides=[1, 1, 0, 0], side=side_))
    tiles.append(Tile('../assets/better_roads/2.png', rotate=2, sides=[1, 0, 0, 1], side=side_))
    tiles.append(Tile('../assets/better_roads/2.png', rotate=3, sides=[0, 0, 1, 1], side=side_))

    tiles.append(Tile('../assets/better_roads/3.png', sides=[1, 1, 1, 0], side=side_))
    tiles.append(Tile('../assets/better_roads/3.png', rotate=1, sides=[1, 1, 0, 1], side=side_))
    tiles.append(Tile('../assets/better_roads/3.png', rotate=2, sides=[1, 0, 1, 1], side=side_))
    tiles.append(Tile('../assets/better_roads/3.png', rotate=3, sides=[0, 1, 1, 1], side=side_))

    tiles.append(Tile('../assets/better_roads/4.png', sides=[1, 1, 1, 1], side=side_))
    instance = WFC(3840, 1088, tiles, side_)
    instance.run()