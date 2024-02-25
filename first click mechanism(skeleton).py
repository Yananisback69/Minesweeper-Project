import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 800)) # Creating the screen
pygame.display.set_caption('Minesweeper')
num_mines = 8

clicked = ()
dug = set()

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

        action = False

        # get mouse position
        
        pos = pygame.mouse.get_pos()
        
        # flag mouse over button

        if self.rect.collidepoint(pos):
            
            # Left Click!
            if pygame.mouse.get_pressed()[0] == 1 and self.state == "normal":

                tile_row = int(pos[1]//100) + 1
                tile_col = int(pos[0]//100) + 1
            
                clicked = (tile_row, tile_col)

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
    


'''

def clear_grid(tile: TileFunction, dug: set):
    dug.add( position_of(tile) )
    do_stuff(tile)
    for neighbor in neighbors(tile):
        if position_of(neighbor) not in dug:
            clear_grid(neighbor, dug)

            '''


# blank cell clicked -> 
# reveal all 8 cells around it -> 
# if revealed cell blank -> 
# called function on revealed cell

def clear_grid(tile, dug):
    row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap)
    dug.add((row, col))

    # Show the clicked tile
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

    '''
    global dug

    pos_new = pygame.mouse.get_pos()

    tile_row = int(pos_new[1]//100) + 1
    tile_col = int(pos_new[0]//100) + 1

    
    dug.add((tile_row, tile_col))

    tile.image = clicked_tile
    tile.image = pygame.transform.scale(tile.image, (100, 100))
    tile.state = "clicked"
    print(dug)

    neighbour_tiles = []

    for i in range(-1,2):
        for j in range(-1,2):
            if 0 <= tile_row + i < 8 and 0 <= tile_col + j < 8:
                neighbour_tile_row, neighbour_tile_col = tile_row + i, tile_col + j
                neighbour_tile_index = neighbour_tile_row * 8 + neighbour_tile_col
                neighbour_tile = tiles[neighbour_tile_index]
                if (neighbour_tile_row, neighbour_tile_col) not in dug:
                    if neighbour_tile.adjacent_mines == 0:
                        tiles[neighbour_tile].clear_grid()
                    elif neighbour_tile.adjacent_mines >= 1:
                        neighbour_tile = number_tiles[neighbour_tile.adjacent_mines - 1]
                        #neighbour_tile.state = "clicked"
                        dug.add((neighbour_tile_row, neighbour_tile_col))
                    else:
                        break
                else:
                    break
            else:
                break
    '''
    #pos_new = pygame.mouse.get_pos()

    #tile_row = int(pos_new[1]//100) + 1
    #tile_col = int(pos_new[0]//100) + 1
            
tile_size = 100
tile_gap = 1  # this is how you can tell the tiles apart

tile_size = 100  
tiles_per_row = 8 

width = tiles_per_row * (tile_size + tile_gap)

normal_tile = pygame.image.load("C:/Users/Aditya Singh/assets/tile1.png")
bomb_tile = pygame.image.load("C:/Users/Aditya Singh/assets/mine placeholder.png")
flag_tile = pygame.image.load("C:/Users/Aditya Singh/assets/flag tile.png")
clicked_tile = pygame.image.load("C:/Users/Aditya Singh/assets/tile broken.png")
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



# Randomly place mines and assort numbers
mines_and_numbers(tiles, num_mines)

right_click_pressed = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button clicked
                right_click_pressed = True  # Set the flag
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


    for tile in tiles:
        action = tile.draw(screen)
        if action:  # Check if any action was performed
            if tile.is_mine:
                print("You clicked on a mine!")

    # Right Click!
    
    pygame.display.flip()
'''
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and first_click:
            # On first click, randomly select the clicked tile and its surrounding tiles
            for tile in tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap)
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            index = (row + i) * 8 + (col + j)
                            if 0 <= row + i < 8 and 0 <= col + j < 8:
                                if tiles[index].adjacent_mines == 0:
                                    tiles[index].state = "clicked"
                                    tiles[index].image = pygame.transform.scale(clicked_tile, (100, 100))
                                elif tiles[index].adjacent_mines >= 1:
                                    tiles[index].state = "clicked"
                                    tiles[index].image = number_tiles[tile.adjacent_mines - 1]
                    first_click = False
                    '''