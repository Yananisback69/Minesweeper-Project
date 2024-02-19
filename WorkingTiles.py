import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 800)) # Creating the screen
pygame.display.set_caption('Minesweeper')
num_mines = 40

class TileFunction:
    def __init__(self, x, y, image, w, h):
        self.image = pygame.transform.scale(image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.state = "normal"
        self.is_mine = False
        self.adjacent_mines = 0

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
                elif self.adjacent_mines > 0:
                    self.image = number_tiles[self.adjacent_mines - 1]  # Change to number_tile based on adjacent mines.-1 is there to match the image from the list 'number_tiles'
                else:
                    self.image = clicked_tile
                self.image = pygame.transform.scale(self.image, (100, 100))  # resizing the image
                self.state = "clicked"  # now can't click it again
                action = True

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


tile_size = 100
tile_gap = 1  # this is how you can tell the tiles apart
normal_tile = pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/tile1.png")
bomb_tile = pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/mine final.png")
flag_tile = pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/flag tile.png")
clicked_tile = pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/tile broken.png")
number_tiles = [
    pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/1 tile.png"),
    pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/2 tile.png"),
    pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/3 tile.png"),
    pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/4 tile.png"),
    pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/5 tile.png"),
    pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/6 tile.png"),
    pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/7 tile.png"),
    pygame.image.load("C:/Users/Akshat/Documents/Project/pythonProject/assets/8 tile.png")
]

tiles = []
for row in range(8):
    for col in range(8):
        tile = TileFunction(col * (tile_size + tile_gap), row * (tile_size + tile_gap), normal_tile, tile_size, tile_size)
        tiles.append(tile)

def mines_and_numbers(tiles, num_mines):
    mine_positions = random.sample(range(len(tiles)), num_mines)  # Generates random position from sample of tiles for mine placement
    for pos in mine_positions:
        tiles[pos].is_mine = True  # Changes tile state to be a mine

    for tile in tiles:
        # Check adjacent tiles and update adjacent_mines
        row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap) # Determines grid position of tiles
        for i in range(-1, 2): # Creates a 3*3 grid
            for j in range(-1, 2):
                if 0 <= row + i < 8 and 0 <= col + j < 8:   # Checks to see if neighbouring tile is within the screen boundary
                    index = (row + i) * 8 + (col + j)   # Calculates index of neighbouring tile
                    if tiles[index].is_mine:    # Checks if neighbouring tile is a mine
                        tile.adjacent_mines += 1    # Increments current tile adjacent_mines attribute by 1

# Randomly place mines and assort numbers
mines_and_numbers(tiles, num_mines)

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
