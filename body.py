import pygame
import button
import sys
import random


# This calls the __init__ functions of every pygame module
pygame.init()



# Setting screen size
screen = pygame.display.set_mode((1066,600))
pygame.display.set_caption("Minesweeper")
timer = pygame.time.Clock()


#bg images
bg_images = []
for i in range(1,6):
    bg_image = pygame.image.load(f"bgs/{i}.png").convert_alpha()
    bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()


#End Game Image
end = pygame.image.load(f"assets/Gameover.png")#.convert_alpha()
end = pygame.transform.scale(end, (400, 200))


clicked = ()
dug = set()

# Animation of title 
class Player(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
      super().__init__()
      self.sprite = []
      #self.sprite.append(pygame.image.load("assets/pixil-frame-0.png"))
      self.sprite.append(pygame.image.load("assets/pixil-frame-1.png"))
      self.sprite.append(pygame.image.load("assets/pixil-frame-2.png"))
      self.sprite.append(pygame.image.load("assets/pixil-frame-3.png"))
      self.sprite.append(pygame.image.load("assets/pixil-frame-4.png"))
      self.sprite.append(pygame.image.load("assets/pixil-frame-5.png"))
      self.sprite.append(pygame.image.load("assets/pixil-frame-6.png"))
      self.sprite.append(pygame.image.load("assets/pixil-frame-7.png"))
      self.sprite.append(pygame.image.load("assets/pixil-frame-8.png"))
      self.current_sprite = 0
      self.image = self.sprite[self.current_sprite]

      self.rect = self.image.get_rect()
      self.rect.topleft = [pos_x,pos_y]

    def update(self):
        self.current_sprite += 0.2 # slows down the animation 

        if self.current_sprite >= len(self.sprite):
            self.current_sprite = 0

        self.image = self.sprite[int(self.current_sprite)]


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

                if self.rect.collidepoint(pos) and not game_over:
                    
                    # Left Click!
                    if pygame.mouse.get_pressed()[0] == 1 and self.state == "normal":
                        clicks += 1
                        print(clicks)

                        tile_row = int(pos[1]//tile_size) + 1
                        tile_col = int(pos[0]//tile_size) + 1
                    
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

                        self.image = pygame.transform.scale(self.image, (tile_size,tile_size))  # resizing the image
                        self.state = "clicked"  # now can't click it again
                        action = True

                # draw button on screen
                surface.blit(self.image, (self.rect.x, self.rect.y))

                return action

################################################################################################################################################################################
#Button images load
start_image = pygame.image.load('assets/Start.png')
difficulty_image = pygame.image.load('assets/Difficulty.png')
help_image = pygame.image.load('assets/Help.png')  
try_again_image = pygame.image.load('assets/Tryagain.png')  
exit_image = pygame.image.load('assets/Exit.png')  

# Creating button instances
start_button = button.Button(300,200, start_image, 4)
difficulty_button = button.Button(250,300, difficulty_image, 4)
help_button = button.Button(300,400, help_image, 4)



#Creating Sprites
moving_sprites = pygame.sprite.Group()
player = Player(250,50)
moving_sprites.add(player)


num = 0

button_screen = pygame.Surface((1066,600))# clear secondary background. 
bg_screen = pygame.Surface((1066, 600))

# Drawing the the animated surface, Credits to the youtube video that showed me how, can be found in the documents. 
def draw_bg(surface):
        global num
        surface.fill((255, 255, 255))

        if num > -bg_width:
                for x in range(5):
                    speed = 1
                    for i in bg_images:
                        surface.blit(i,(bg_width*x + num*speed,0))# making the screen draw attribute linked to the surface
                        speed += 1
        else: 
             num= 0
             for i in bg_images:
                surface.blit(i,(num,0))# making the functions dependent on the surface its blited to 
        


        pygame.display.flip()




i = 0
#Main Loop
running = True
while running:
    timer.tick(60)
    
    game_over = False
    
    

    
    draw_bg(bg_screen)# drawing the background onto the backscreen
    
        

    # blit a clear screen ontop of the previous screen,  this allows seperation between the moving screen and buttons preventing flickering
    screen.blit(bg_screen, (0, 0))


    num -= 1

    if start_button.draw(screen): # Start Button Function 
        print("START") 


        pygame.time.delay(200)
        screen = pygame.display.set_mode((1066, 600)) # Creating the screen
        pygame.display.set_caption('Minesweeper')
        num_mines = 24

        clicks = 0
        resets = 0
        clicked = ()
        print(clicks)
        dug = set()

        tile_gap = 1  # this is how you can tell the tiles apart

        tile_size = 50  
        tiles_per_row = 10 

        width = tiles_per_row * (tile_size + tile_gap)

        normal_tile = pygame.image.load("assets/tile1.png")
        bomb_tile = pygame.image.load("assets/bomb1.png")
        flag_tile = pygame.image.load("assets/flag tile.png")
        clicked_tile = pygame.image.load("assets/tile broken.png")
        number_tiles = [
            pygame.image.load("assets/1 tile.png"),
            pygame.image.load("assets/2 tile.png"),
            pygame.image.load("assets/3 tile.png"),
            pygame.image.load("assets/4 tile.png"),
            pygame.image.load("assets/5 tile.png"),
            pygame.image.load("assets/6 tile.png"),
            pygame.image.load("assets/7 tile.png"),
            pygame.image.load("assets/8 tile.png")
        ]

        tiles = []

            
        def clear_grid(tile, dug):
            row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap)
            dug.add((row, col))

            tile.state = "clicked"
            tile.image = pygame.transform.scale(clicked_tile, (tile_size,tile_size))

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= row + i < 10 and 0 <= col + j < 10:
                        index = (row + i) * 10 + (col + j)
                        neighbor_tile = tiles[index]

                        if neighbor_tile.adjacent_mines == 0 and (row + i, col + j) not in dug:
                            neighbor_tile.state = "clicked"
                            neighbor_tile.image = pygame.transform.scale(clicked_tile, (tile_size,tile_size))
                            clear_grid(neighbor_tile, dug)

                        elif neighbor_tile.adjacent_mines > 0:
                            neighbor_tile.state = "clicked"
                            neighbor_tile.image = pygame.transform.scale(number_tiles[neighbor_tile.adjacent_mines - 1], (tile_size,tile_size))

                        dug.add((row + i, col + j))



        mine_pos = []


        for row in range(10):
            for col in range(10):
                tile = TileFunction(col * (tile_size + tile_gap), row * (tile_size + tile_gap), normal_tile, tile_size, tile_size)
                tiles.append(tile)

        def mines_and_numbers(tiles, num_mines):
            mine_positions = random.sample([(row, col) for row in range(10) for col in range(10)], num_mines)
            
            for row, col in mine_positions:
                # Calculate the index of the tile based on row and col
                index = row * 10 + col
                tiles[index].is_mine = True
            
            print(mine_positions)


            for tile in tiles:
                # Check adjacent tiles and update adjacent_mines
                row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap) # Determines grid position of tiles
                
                for i in range(-1, 2): # Creates a 3*3 grid
                    for j in range(-1, 2):
                        if 0 <= row + i < 10 and 0 <= col + j < 10:   # Checks to see if neighbouring tile is within the screen boundary
                            index = (row + i) * 10 + (col + j)   # Calculates index of neighbouring tile
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
                tile.image = pygame.transform.scale(normal_tile, (tile_size,tile_size))  # resizing the image

            # Regenerate new mine positions and update adjacent mine counts
            mines_and_numbers(tiles, num_mines)

            resets += 1
            print("resets:", resets)

            # If there's a clicked tile, update its state and image
            if clicked:
                row, col = clicked
                index = (row - 1) * 10 + (col - 1)
                tile = tiles[index]
                if tile.is_mine:
                    reset_grid()
                elif tile.adjacent_mines > 0:
                    reset_grid()
                else:
                    clear_grid(tile, dug)
                tile.image = pygame.transform.scale(tile.image, (tile_size,tile_size))
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
                                        
                                        for tile in tiles:# loops throught the tiles again to find the mines and unveil them
                                            if tile.is_mine:
                                                tile.image = bomb_tile # if the tile is a mine then it's image is converted into a bomb_tile.png
                                                tile.image = pygame.transform.scale(tile.image, (tile_size,tile_size))
                                                pygame.display.flip()
                                        game_over = True

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
                                    tile.image = pygame.transform.scale(tile.image, (tile_size,tile_size))  # resizing the image
                                    tile.state = "flagged"  # Now it's flagged
                                    print("flagged")
                                elif tile.state == "flagged":  # Right-click to unflag
                                    tile.image = normal_tile  # changing state back to normal state
                                    tile.image = pygame.transform.scale(tile.image, (tile_size,tile_size))  # resizing the image
                                    tile.state = "normal"  # when the flag is unflagged
                                    print("unflagged")


                if not game_over:               
                    pygame.display.flip()

                
                if game_over:
                    pygame.time.delay(200)

                    running2 = True
                    while running2 == True:

                        # blittng Game Over On top
                        screen.blit(end, (600,100))

                        # Creating Buttons to start again or exit
                        try_again_button = button.Button(800,400, try_again_image, 0.5)
                        exit_button = button.Button(550,400, exit_image, 0.5)
                        pygame.display.flip()

                        # Try again buttons function


                        # exit buttons function
                        if exit_button.draw(screen):
                            print("Exitting")
                            pygame.quit()
                            exit()

                            
                        # Did the user click the window to close the button
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running2 = False
                                running = False
                            if try_again_button.draw(screen) and event.type == pygame.MOUSEBUTTONDOWN:
                                print("START AGAIN")
                                #clear_grid()
                    
                    

                

    if difficulty_button.draw(screen):
        print("DIFFICULTY")

    if help_button.draw(screen):
        print("CANNOT HELP")
    
    pygame.display.flip()



            

    
# Did the user click the window to close the button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()