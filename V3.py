import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Minesweeper')


class TileFunction:
    def __init__(self, x, y, image, w, h):
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.state = "normal"

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # flag mouse over button
        if self.rect.collidepoint(pos):
            # Left Click!
            if pygame.mouse.get_pressed()[0] == 1 and self.state == "normal":
                self.image = clicked_tile  # changing the state to clicked
                self.image = pygame.transform.scale(self.image, (100, 100))  # resizing the image
                self.state = "clicked"  # now cant click it again
                action = True

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


tile_size = 100
tile_gap = 1  # this is how you can tell the tiles apart
normal_tile = pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/tile.png")
bomb_tile = pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/bomb_tile.png")
flag_tile = pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/flag.png")
clicked_tile = pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/clicked_tile.png")

tiles = []
for row in range(8):
    for col in range(8):
        tile = TileFunction(col * (tile_size + tile_gap), row * (tile_size + tile_gap), normal_tile, tile_size, tile_size)
        tiles.append(tile)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        for tile in tiles:
            action = tile.draw(screen)
            if action:  # Check if any action was performed
                print("Tile action performed")

        # Right Click!
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Check for right mouse button click
            for tile in tiles:
                if tile.rect.collidepoint(event.pos):
                    if tile.state == "normal":  # Right-click to flag
                        tile.image = flag_tile  # changing the state to flag state
                        tile.image = pygame.transform.scale(tile.image, (100, 100))  # resizing the image
                        tile.state = "flagged"  # Now its flagged
                        print("flagged")
                    elif tile.state == "flagged":  # Right-click to unflag
                        tile.image = normal_tile  # changing state back to normal state
                        tile.image = pygame.transform.scale(tile.image, (100, 100))  # resizing the image
                        tile.state = "normal"  # when the flag is unflagged
                        print("unflagged")

    pygame.display.flip()