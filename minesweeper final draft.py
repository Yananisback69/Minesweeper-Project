import pygame
import button
import sys
import random


# This calls the __init__ functions of every pygame module
pygame.init()

# Load and play the background music
pygame.mixer.music.load("assets/bg music.mp3")
#click_sound = pygame.mixer.Sound()
pygame.mixer.music.play(-1)  # -1 means loop indefinitely



# Setting screen size
screen_width = 1066
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")
timer = pygame.time.Clock()

#bg images
bg_images = []
for i in range(1,6):
    bg_image = pygame.image.load(f"assets/bgs{i}.png").convert_alpha()
    bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()


#End Game Image
end = pygame.image.load(f"assets/Gameover.png").convert_alpha()
end = pygame.transform.scale(end, (400, 100))

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


#Button images load
start_image = pygame.image.load('assets/startgreen1.png')
help_image = pygame.image.load('assets/helpgreen.png')  
try_again_image = pygame.image.load('assets/try again.png')  
exit_image = pygame.image.load('assets/Exit.png')
mute_image = pygame.image.load('assets/mute button.png')



# Loading other images
title_image = pygame.image.load('assets/title 4.png')
tiles_surface_image = pygame.image.load('assets/background.png')
tiles_surface_image = pygame.transform.scale(tiles_surface_image, (screen_width, screen_height))


# Creating button instances
start_button = button.Button(screen_width * 0.5, screen_height * 0.43, start_image, 0.2925)
help_button = button.Button(screen_width * 0.5, screen_height * 0.57, help_image, 0.2925)
exit_button = button.Button(screen_width * 0.5, screen_height * 0.71, exit_image, 0.2925)
mute_button = button.Button(screen_width * 0.8, screen_height * 0.89, mute_image, 1)

#Creating title animation
title = button.Title(screen_width * 0.5, screen_height * 0.17, title_image, 0.5)


num = 0
correct_flag = 0

end_screen = pygame.Surface((1066,600), pygame.SRCALPHA)# clear secondary background. 
bg_screen = pygame.Surface((1066, 600))


# Drawing the the animated surface, Credits to the youtube video that showed me how, can be found in the documents. 
def draw_bg(surface):
        global num
        #surface.fill((255, 255, 255))

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


def convert_bomb_tile():
    for cube1 in tiles:
        if cube1.is_mine: 
            cube1.image = bomb_tile
            cube1.image = pygame.transform.scale(cube1.image, (tile_size,tile_size))
            cube1.state = 'clicked'

        else:                           
            cube1.state = 'clicked'

    for tile in tiles: # Draws the tiles onto the screen2
        action = tile.draw(screen2)


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

def mines_and_numbers(tiles, num_mines):
            mine_positions = random.sample([(row, col) for row in range(10) for col in range(10)], num_mines)
            
            for row, col in mine_positions:
                # Calculate the index of the tile based on row and col
                index = row * 10 + col
                tiles[index].is_mine = True
            
            #print(mine_positions)


            for tile in tiles:
                # Check adjacent tiles and update adjacent_mines
                row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap) # Determines grid position of tiles
                
                for i in range(-1, 2): # Creates a 3*3 grid
                    for j in range(-1, 2):
                        if 0 <= row + i < 10 and 0 <= col + j < 10:   # Checks to see if neighbouring tile is within the screen2 boundary
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

# This is the game function
def game():
        global tile_size,tile_gap, screen2, tiles, tile, num_mines,count, correct_flag, clicks, resets # i know this is not ideal, and parameters are much better however for some reason they were not working for the tiles class 
                                                                                                        # and since i would have to learn classes which i did not have the time for i just made them global 

        print("START")
        looped_once = False
        tile_print = True 


        pygame.time.delay(200)
        screen2 = pygame.display.set_mode((1066, 600)) # Creating the screen2
        pygame.display.set_caption('Minesweeper')
        screen2.fill("black")
        

        clicks = 0
        resets = 0
        clicked = ()
        dug = set()

        tile_gap = 1  # this is how you can tell the tiles apart

        tile_size = 50  
        tiles_per_row = 10 

        width = tiles_per_row * (tile_size + tile_gap)



        tiles = []

            
        


        mine_pos = []

        start_x = 0
        start_y = 0


        for row in range(10):
            for col in range(10):
                tile = TileFunction(start_x + col * (tile_size + tile_gap), start_y + row * (tile_size + tile_gap), normal_tile, tile_size, tile_size)
                tiles.append(tile)

        
 

        # Randomly place mines and assort numbers
        mines_and_numbers(tiles, num_mines)


        right_click_pressed = False
        win_displayed = False


        # Tile while loop 
        while tile_print == True:
                
                # if all the mines are revealed the game ends
                all_mines_revealed = all(tile.image == bomb_tile for tile in tiles if tile.is_mine)
                

                if count == num_mines:
                    looped_once = True # this tries to only loop the end game once so that the whole thing doesnt get covered with a white screen. 
                    end_game()

                if not all_mines_revealed:
                    for tile in tiles: # Draws the tiles onto the screen2
                            action = tile.draw(screen2)

                

                for event in pygame.event.get():
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 3:  # Right mouse button clicked
                            right_click_pressed = True  # Set the flag
                        
                        if event.button == 1:
                            #print("left clicked")  # Check if any action was performed
                            for tile in tiles:
                                if tile.rect.collidepoint(event.pos):  # Check which tile was clicked
                                    if tile.is_mine and clicks != 0: # if the tile clicked on was a mine

                                        print("You clicked on a mine!")

                                        for cube1 in tiles: # reveals all the mines by iterating through the tiles list finding the mines and changing their image
                                            if cube1.is_mine: 
                                                cube1.image = bomb_tile
                                                pygame.display.flip()
                                                cube1.image = pygame.transform.scale(cube1.image, (tile_size,tile_size))
                                                cube1.state = 'clicked'
                                                count += 1
                                                print(count)

                                            else:                           
                                                cube1.state = 'clicked'
                                    



                        
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
                                    if tile.is_mine:
                                        correct_flag += 1
                                        print("correct flag:", correct_flag)
                                elif tile.state == "flagged":  # Right-click to unflag
                                    tile.image = normal_tile  # changing state back to normal state
                                    tile.image = pygame.transform.scale(tile.image, (tile_size,tile_size))  # resizing the image
                                    tile.state = "normal"  # when the flag is unflagged
                                    print("unflagged")
                                    if tile.is_mine:
                                        correct_flag -= 1
                                        print("correct flag:", correct_flag)
                
                    if correct_flag == num_mines and not win_displayed:  # Check if all flags are placed correctly
                        # Reveal all mines
                        end_game()

                        # Disable further clicks
                        for tile in tiles:
                            tile.state = "clicked"

                        # Print "You win"
                        print("You win")
                        running = False
                        show_end = True

                        win_displayed = True



                    pygame.display.flip()
    
    


def end_game():
    global running
    end_loop = True

    convert_bomb_tile()

    
    # Drawing onto the overlay surface
    end_screen.fill((255, 255, 255, 70))  # Fill with semi-transparent white color

    # Blit the overlay surface onto the main screen
    screen.blit(end_screen, (0, 0))
                            

    while end_loop == True:
                     

        # Drawing the screen buttons
        screen.blit(end, (50,0))
        try_again_button = button.Button(300,530, try_again_image, 0.2)
        exit_button = button.Button(50,530, exit_image, 0.2)
        


        # exit buttons function
        if exit_button.draw(screen2):
            print("Exitting")
            pygame.quit()
            exit()

        try_again_button.draw(screen2)# Draws the try game button
                            

                                    
                            
        # Did the user click the window to close the button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_button.draw(screen2):# Try again buttons Function
                    
                    for tile in tiles:
                        tile.state = "normal"
                        tile.image = normal_tile
                    
                    print("START AGAIN") # check to see if clicked
                    #pygame.Surface.fill(0,0,0)
                    end_loop == False
                    end_screen.fill ((0,0,0,0))
                    reset_grid()

                    pygame.display.flip()
                    
                    game() # running the game 
                    break
            
        pygame.display.flip()







count = 0

i = 0
#Main Loop
running = True
while running:
    timer.tick(60)
    
    

    # Drawing the scrolling background 
    draw_bg(bg_screen)
    
        

    # Blit a clear screen ontop of the previous screen,  this allows seperation between the moving screen and buttons preventing flickering
    screen.blit(bg_screen, (0, 0))

    title.draw(screen)
    num -= 1


    def toggle_mute():
        global muted
        if pygame.mixer.music.get_busy():  # Check if music is currently playing
            if muted:
                pygame.mixer.music.unpause()  # Unpause the music if it's currently muted
                muted = False
            else:
                pygame.mixer.music.pause()  # Pause the music if it's currently playing
                muted = True
        else:
            pygame.mixer.music.play(-1)  # Start playing music if it's not currently playing
            muted = False

    running = True
    muted = False  # To track the mute state

    if start_button.draw(screen): # Start Button Function
        print("start")

        running = True
        while running:
             
            for event in pygame.event.get():
                 if event.type == pygame.QUIT: 
                      running = False

            #creating screen
            screen = pygame.display.set_mode((1066,600))
            screen.fill((202,228,241))

    # Load the button image
            back_img = pygame.image.load('assets/back_btn.png').convert_alpha()
            easy_btn = pygame.image.load('assets/easy_btn.png').convert_alpha()
            medium_btn = pygame.image.load('assets/medium_btn.png').convert_alpha()
            hard_btn = pygame.image.load('assets/hard_btn.png').convert_alpha()

            class Button():
                def __init__(self, x, y, image):
                    self.image = image
                    self.rect = self.image.get_rect(topleft=(x, y))
                    self.clicked = False  # Track if the button has been clicked
                    self.prev_clicked = False  # Track previous click state

                def draw(self, screen):
                    action = False
                    screen.blit(self.image, self.rect)
                    pos = pygame.mouse.get_pos()
        
                    # Check if mouse is over the button
                    if self.rect.collidepoint(pos):
                        if pygame.mouse.get_pressed()[0] == 1 and not self.prev_clicked:
                        # If mouse button is pressed and previous click state is False
                            self.clicked = True
                            action = True
                        else:
                            self.clicked = False
                    else:
                        self.clicked = False
        
        # Update previous click state
                    self.prev_clicked = pygame.mouse.get_pressed()[0]

                    return action



# Scale the button image
            scaled_back_img = pygame.transform.scale(back_img, (200, 200))
            scaled_easy_img = pygame.transform.scale(easy_btn, (200, 200))
            scaled_medium_img = pygame.transform.scale(medium_btn, (200, 200))
            scaled_hard_img = pygame.transform.scale(hard_btn, (200, 200))

# Create an instance of the Button class
            back_button = Button(433, 500, scaled_back_img)
            easy_btn = Button(200, 200, scaled_easy_img)
            medium_btn = Button(400, 200, scaled_medium_img)
            hard_btn = Button(600, 200, scaled_hard_img)           

            num_mines_easy = 10  # Number of mines for easy difficulty
            num_mines_medium = 30  # same thing here
            num_mines_hard = 40 #same thing here

    

    # Game loop
            running = True 
            while running:
           
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        running = False
            
                    if back_button.draw(screen):
                        print('BACK')

                    if easy_btn.draw(screen):
                            print('EASY')
                            num_mines = num_mines_easy                   
                            game()

                        
                    

    

                    
                    if medium_btn.draw(screen):
                        print('MEDIUM')
                        num_mines = num_mines_medium
                        game()
                    
                    


                                    

                    
                    if hard_btn.draw(screen):
                        print('HARD')
                        num_mines = num_mines_hard
                        game()            
                    
                pygame.display.flip()



    if help_button.draw(screen):
        print("help")
        screen = pygame.display.set_mode((1066, 600))
        screen.fill((202,228,241))

        text_font = pygame.font.SysFont("Impact", 20)
        tile_font = pygame.font.SysFont("Impact", 40)

        def draw_text_center(text, font, text_col, y):
            text_surface = font.render(text, True, text_col)
            text_rect = text_surface.get_rect()
            text_rect.center = (screen.get_width() // 2, y)
            screen.blit(text_surface, text_rect)


        draw_text_center("Minesweeper Instructions", tile_font, (0, 0, 0), 40)
        draw_text_center("Welcome to Minesweeper! This classic puzzle game requires logic and strategy to uncover hidden mines without detonating them.", text_font, (0, 0, 0), 100)
        
        running = True
        while running:
            pygame.display.flip()
        #handle events here 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

  
    if mute_button.draw(screen):
         toggle_mute()


    
    
    if exit_button.draw(screen):
        print("EXIT")
        pygame.quit()
        exit()

# Did the user click the window to close the button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()
