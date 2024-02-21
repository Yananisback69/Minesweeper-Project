import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 800))  # Creating the screen
pygame.display.set_caption('Minesweeper')
num_mines = 12

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

            # Right Click!
            elif pygame.mouse.get_pressed()[2] == 1 and self.state == "normal":
                self.image = flag_tile
                self.image = pygame.transform.scale(self.image, (100, 100))  # resizing the image
                self.state = "flagged"  # now can't click it again
                action = True

            # Right Click again to unflag!
            elif pygame.mouse.get_pressed()[2] == 1 and self.state == "flagged":
                self.image = normal_tile
                self.image = pygame.transform.scale(self.image, (100, 100))  # resizing the image
                self.state = "normal"  # now can't click it again
                action = True

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


tile_size = 100
tile_gap = 1  # this is how you can tell the tiles apart
normal_tile = pygame.image.load("C:/Users/Aditya Singh/assets/tile1.png")
bomb_tile = pygame.image.load("C:/Users/Aditya Singh/assets/mine placeholder.png")
flag_tile = pygame.image.load("C:/Users/Aditya Singh/assets/flag tile.png")
clicked_tile = pygame.image.load("C:/Users/Aditya Singh/assets/tile broken.png")  # Use broken.png for clicked state
number_tiles = [
    pygame.image.load("C:/Users/Aditya Singh/assets/1 tile.png"),
    pygame.image.load("C:/Users/Aditya Singh/assets/2 tile.png"),
    pygame.image.load("C:/Users/Aditya Singh/assets/3 tile.png"),
    pygame.image.load("C:/Users/Aditya Singh/assets/4 tile.png"),
    pygame.image.load("C:/Users/Aditya Singh/assets/5 tile.png"),
    pygame.image.load("C:/Users/Aditya Singh/assets/6 tile.png"),
    pygame.image.load("C:/Users/Aditya Singh/assets/7 tile.png"),
    pygame.image.load("C:/Users/Aditya Singh/assets/8 tile.png")
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


first_click = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and first_click:
            # On first click, randomly select the clicked tile
            clicked_tile = random.choice(tiles)
            row, col = clicked_tile.rect.y // (tile_size + tile_gap), clicked_tile.rect.x // (tile_size + tile_gap)
            clicked_tile.state = "clicked"
            clicked_tile.image = pygame.transform.scale(clicked_tile.image, (100, 100))

            # Generate random number of surrounding tiles between 6 and 13
            num_surrounding_tiles = random.randint(6, 13)
            surrounding_tiles = []

            while len(surrounding_tiles) < num_surrounding_tiles:
                # Generate a random surrounding tile
                i, j = random.randint(-1, 1), random.randint(-1, 1)
                index = (row + i) * 8 + (col + j)
                if 0 <= row + i < 8 and 0 <= col + j < 8 and tiles[index] not in surrounding_tiles:
                    surrounding_tiles.append(tiles[index])

            # Mark surrounding tiles as clicked
            for tile in surrounding_tiles:
                tile.state = "clicked"
                tile.image = pygame.transform.scale(tile.image, (100, 100))
                
            first_click = False


    for tile in tiles:
        tile.draw(screen)

    pygame.display.flip()
