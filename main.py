import pygame

class WFC:
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Wave Function Collapse")
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()

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
    instance = WFC()
    instance.run()