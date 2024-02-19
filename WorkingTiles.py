import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Minesweeper')
num_mines = 8

class TileFunction:
    def __init__(self, x, y, image, w, h):
        self.image = pygame.transform.scale(image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.state = "normal"
        self.is_mine = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # flag mouse over button
        if self.rect.collidepoint(pos):
            # Left Click!
            if pygame.mouse.get_pressed()[0] == 1 and self.state == "normal":
                if self.is_mine:
                    self.image = bomb_tile  # Change to bomb_tile if it's a mine
                else:
                    self.image = clicked_tile  # Change to clicked_tile
                self.image = pygame.transform.scale(self.image, (100, 100))  # resizing the image
                self.state = "clicked"  # now can't click it again
                action = True

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action



tile_size = 100
tile_gap = 1  # this is how you can tell the tiles apart
normal_tile = pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/tile1.png")
bomb_tile = pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/mine placeholder.png")
flag_tile = pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/flag tile.png")
clicked_tile = pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/tile broken.png")

tiles = []
for row in range(8):
    for col in range(8):
        tile = TileFunction(col * (tile_size + tile_gap), row * (tile_size + tile_gap), normal_tile, tile_size, tile_size)
        tiles.append(tile)

def place_mines(tiles, num_mines):
    mine_positions = random.sample(range(len(tiles)), num_mines) #Generates random position from sample of tiles for mine placement
    for pos in mine_positions:
        tiles[pos].is_mine = True #Changes tile state to be a mine

# Randomly place mines
place_mines(tiles, num_mines)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for tile in tiles:
        action = tile.draw(screen)
        if action:  # Check if any action was performed
            if tile.is_mine:
                print("You clicked on a mine!")

    # Right Click!
    if pygame.mouse.get_pressed()[2]:  # Check for right mouse button click
        for tile in tiles:
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                if tile.state == "normal":  # Right-click to flag
                    tile.image = flag_tile  # changing the state to flag state
                    tile.image = pygame.transform.scale(tile.image, (100, 100))  # resizing the image
                    tile.state = "flagged"  # Now it's flagged
                    print("flagged")
                elif tile.state == "flagged":  # Right-click to unflag
                    tile.image = normal_tile  # changing state back to normal state
                    tile.image = pygame.transform.scale(tile.image, (100, 100))  # resizing the image
                    tile.state = "normal"  # when the flag is unflagged
                    print("unflagged")

    pygame.display.flip()
