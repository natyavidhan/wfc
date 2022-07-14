import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from main import Cell, Tile, WFC

tiles = []
_side = 16
tiles.append(Tile('../assets/better_roads/0.png', sides=[0, 0, 0, 0], side=_side))

tiles.append(Tile('../assets/better_roads/1.png', sides=[1, 0, 1, 0], side=_side))
tiles.append(Tile('../assets/better_roads/1.png', rotate=1, sides=[0, 1, 0, 1], side=_side))

tiles.append(Tile('../assets/better_roads/2.png', sides=[0, 1, 1, 0], side=_side))
tiles.append(Tile('../assets/better_roads/2.png', rotate=1, sides=[1, 1, 0, 0], side=_side))
tiles.append(Tile('../assets/better_roads/2.png', rotate=2, sides=[1, 0, 0, 1], side=_side))
tiles.append(Tile('../assets/better_roads/2.png', rotate=3, sides=[0, 0, 1, 1], side=_side))

tiles.append(Tile('../assets/better_roads/3.png', sides=[1, 1, 1, 0], side=_side))
tiles.append(Tile('../assets/better_roads/3.png', rotate=1, sides=[1, 1, 0, 1], side=_side))
tiles.append(Tile('../assets/better_roads/3.png', rotate=2, sides=[1, 0, 1, 1], side=_side))
tiles.append(Tile('../assets/better_roads/3.png', rotate=3, sides=[0, 1, 1, 1], side=_side))

tiles.append(Tile('../assets/better_roads/4.png', sides=[1, 1, 1, 1], side=_side))

instance = WFC(tiles, _side)
instance.run()