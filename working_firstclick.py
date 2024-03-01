import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 800)) # Creating the screen
pygame.display.set_caption('Minesweeper')
num_mines = 8

clicks = 0
resets = 0
clicked = ()
print(clicks)
dug = set()

tile_size = 100
tile_gap = 1  # this is how you can tell the tiles apart

tile_size = 100  
tiles_per_row = 8 

width = tiles_per_row * (tile_size + tile_gap)

normal_tile = pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/tile1.png")
bomb_tile = pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/mine placeholder.png")
flag_tile = pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/flag tile.png")
clicked_tile = pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/tile broken.png")
number_tiles = [
    pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/1 tile.png"),
    pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/2 tile.png"),
    pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/3 tile.png"),
    pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/4 tile.png"),
    pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/5 tile.png"),
    pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/6 tile.png"),
    pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/7 tile.png"),
    pygame.image.load("/Users/kabir1/Documents/minesweeper_project/assets/assets/8 tile.png")
]

tiles = []
class TileFunction:
    def __init__(self, x, y, image, w, h):
        self.image = pygame.transform.scale(image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.state = "normal"
        self.is_mine = False
        self.adjacent_mines = 0
        # self.tile_blank = False

    def draw(self, surface):

        global clicked
        global clicks

        action = False

        # get mouse position
        
        pos = pygame.mouse.get_pos()
        
        # flag mouse over button

        if self.rect.collidepoint(pos):
            
            # Left Click!
            if pygame.mouse.get_pressed()[0] == 1 and self.state == "normal":
                clicks += 1
                print(clicks)

                tile_row = int(pos[1]//100) + 1
                tile_col = int(pos[0]//100) + 1
            
                clicked = (tile_row, tile_col)

                dug.add(clicked)

                if clicks == 0 or clicks == 1:  # Check if it's the first or second click
                    if self.is_mine or self.adjacent_mines > 0:
                        reset_grid()
                    else:
                        clear_grid(tile, dug)
                else:
                    if self.is_mine:
                        self.image = bomb_tile  # Change to bomb_tile if it's a mine
                    elif self.adjacent_mines > 0:
                        self.image = number_tiles[self.adjacent_mines - 1]  # Change to number_tile based on adjacent mines.-1 is there to match the image from the list 'number_tiles'
                        dug.add(clicked)
                    elif self.adjacent_mines == 0:
                        clear_grid(tile, dug)

                self.image = pygame.transform.scale(self.image, (100, 100))  # resizing the image
                self.state = "clicked"  # now can't click it again
                action = True

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
def clear_grid(tile, dug):
    row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap)
    dug.add((row, col))

    tile.state = "clicked"
    tile.image = pygame.transform.scale(clicked_tile, (100, 100))

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < 8 and 0 <= col + j < 8:
                index = (row + i) * 8 + (col + j)
                neighbor_tile = tiles[index]

                if neighbor_tile.adjacent_mines == 0 and (row + i, col + j) not in dug:
                    neighbor_tile.state = "clicked"
                    neighbor_tile.image = pygame.transform.scale(clicked_tile, (100, 100))
                    clear_grid(neighbor_tile, dug)

                elif neighbor_tile.adjacent_mines > 0:
                    neighbor_tile.state = "clicked"
                    neighbor_tile.image = pygame.transform.scale(number_tiles[neighbor_tile.adjacent_mines - 1], (100, 100))

                dug.add((row + i, col + j))



mine_pos = []


for row in range(8):
    for col in range(8):
        tile = TileFunction(col * (tile_size + tile_gap), row * (tile_size + tile_gap), normal_tile, tile_size, tile_size)
        tiles.append(tile)

def mines_and_numbers(tiles, num_mines):
    mine_positions = random.sample([(row, col) for row in range(8) for col in range(8)], num_mines)
    
    for row, col in mine_positions:
        # Calculate the index of the tile based on row and col
        index = row * 8 + col
        tiles[index].is_mine = True
    
    print(mine_positions)


    for tile in tiles:
        # Check adjacent tiles and update adjacent_mines
        row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap) # Determines grid position of tiles
        
        for i in range(-1, 2): # Creates a 3*3 grid
            for j in range(-1, 2):
                if 0 <= row + i < 8 and 0 <= col + j < 8:   # Checks to see if neighbouring tile is within the screen boundary
                    index = (row + i) * 8 + (col + j)   # Calculates index of neighbouring tile
                    if tiles[index].is_mine:    # Checks if neighbouring tile is a mine
                        tile.adjacent_mines += 1    # Increments current tile adjacent_mines attribute by 1

def reset_grid():
    print("reset")
    
    global clicked
    global resets

    # Clear all mine flags and adjacent mine counts
    for tile in tiles:
        tile.is_mine = False
        tile.adjacent_mines = 0
        tile.state = "normal"
        tile.image = pygame.transform.scale(normal_tile, (100, 100))  # resizing the image

    # Regenerate new mine positions and update adjacent mine counts
    mines_and_numbers(tiles, num_mines)

    resets += 1
    print("resets:", resets)

    # If there's a clicked tile, update its state and image
    if clicked:
        row, col = clicked
        index = (row - 1) * 8 + (col - 1)
        tile = tiles[index]
        if tile.is_mine:
            reset_grid()
        elif tile.adjacent_mines > 0:
            reset_grid()
        else:
            clear_grid(tile, dug)
        tile.image = pygame.transform.scale(tile.image, (100, 100))
        tile.state = "clicked"

    # Reset clicked variable
    clicked = ()

# Randomly place mines and assort numbers
mines_and_numbers(tiles, num_mines)

right_click_pressed = False

while True:

    for tile in tiles: # Draws the tiles onto the screen
        action = tile.draw(screen)

    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button clicked
                right_click_pressed = True  # Set the flag
            
            if event.button == 1:
                print("left clicked")  # Check if any action was performed
                for tile in tiles:
                    if tile.rect.collidepoint(event.pos):  # Check which tile was clicked
                        if tile.is_mine and clicks != 0:
                            print("You clicked on a mine!")
                            pygame.quit()
                            exit()           

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button released
                right_click_pressed = False  # Reset the flag

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if right_click_pressed:  # Check for right mouse button click
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