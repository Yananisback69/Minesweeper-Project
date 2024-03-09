import pygame
import button
import time
import random
import math
import sys


# This calls the __init__ functions of every pygame module
pygame.init()
tiles_per_row_medium = 15
tiles_per_row_easy = 10
tiles_per_row_hard = 20
tile_size_easy = 50
tile_size_medium = 33
tile_size_hard = 24
#### ASSETS ####

# Load and play the background music
pygame.mixer.music.load("assets/bg music.mp3")
# click_sound = pygame.mixer.Sound()
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Setting screen size
screen_width = 1066
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")
timer = pygame.time.Clock()

# bg images
bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"assets/background_images/{i}.png").convert_alpha()
    bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()

# Image behind tiles
bg2_image = pygame.image.load('assets/background.png').convert()
bg2 = pygame.transform.scale(bg2_image, (screen_width, screen_height))
bg2_width = bg2.get_width()

# Help section images
help_section_list = [
    pygame.image.load("assets/help1.png"),
    pygame.image.load("assets/help1.png"),
    pygame.image.load("assets/help3.png"),
    pygame.image.load("assets/help4.png"),
    pygame.image.load("assets/help5.png"),
    pygame.image.load("assets/help6.png"),
]
left_arrow_image = pygame.image.load('assets/left arrow.png')
right_arrow_image = pygame.image.load('assets/right arrow.png')

# Load the button image
back_img = pygame.image.load('assets/back_button.png').convert_alpha()
easy_image = pygame.image.load('assets/Easy.png').convert_alpha()
medium_image = pygame.image.load('assets/Medium.png').convert_alpha()
hard_image = pygame.image.load('assets/Hard.png').convert_alpha()
mute_image = pygame.image.load('assets/mute_button.png')
unmute_image = pygame.image.load('assets/unmute_button.png')
continue_image = pygame.image.load("assets/Continue.png")

# Creating surface to blit tiles onto
tiles_surface_size = width, height = (509, 509)
tiles_surface = pygame.Surface(tiles_surface_size)

# Flag counter image
flag_counter_image = pygame.image.load('assets/flag_counter + timer.png')
flag_counter_image = pygame.transform.scale(flag_counter_image, (200, 145))

# Create an instance of the Button class
back_button = button.Button(540, 450, back_img, 0.3)
easy_btn = button.Button(350, 250, easy_image, 0.3)
medium_btn = button.Button(550, 250, medium_image, 0.3)
hard_btn = button.Button(750, 250, hard_image, 0.3)
mute_button = button.ToggleMuteButton(screen_width * 0.95, screen_height * 0.94, unmute_image, mute_image, 0.2)
continue_button = button.Button(screen_width * 0.1, 450, continue_image, 0.2925)
left_arrow = button.Button(screen_width * 0.45, screen_height * 0.85, left_arrow_image, 0.4)
right_arrow = button.Button(screen_width * 0.55, screen_height * 0.85, right_arrow_image, 0.4)

board_border_image = pygame.image.load("assets/board border.png")
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

# Button images load
start_image = pygame.image.load('assets/Start.png')
help_image = pygame.image.load('assets/Help.png')
try_again_image = pygame.image.load('assets/Retry.png')
exit_image = pygame.image.load('assets/Exit.png')

# Loading other images
title_image = pygame.image.load('assets/Title.png')

# End Game Image
gameover_image = pygame.image.load(f"assets/Gameover.png").convert_alpha()
gamewin_image = pygame.image.load(f"assets/you win.png").convert_alpha()

# Creating button instances
start_button = button.Button(screen_width * 0.5, screen_height * 0.43, start_image, 0.2925)
help_button = button.Button(screen_width * 0.5, screen_height * 0.57, help_image, 0.2925)
exit_button = button.Button(screen_width * 0.5, screen_height * 0.71, exit_image, 0.2925)
retry_button = button.Button(screen_width * 0.5, 350, try_again_image, 0.25)
home_button = button.Button(screen_width * 0.5, 450, back_img, 0.2925)

# Creating title animation
title = button.Title(screen_width * 0.5, screen_height * 0.17, title_image, 0.5)
gameover = button.Title(screen_width * 0.5, screen_height * 0.33, gameover_image, 0.5)
gamewin = button.Title(screen_width * 0.5, screen_height * 0.33, gamewin_image, 0.5)

end_screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)  # clear secondary background.
bg_screen = pygame.Surface((screen_width, screen_height))
bg_screen2 = pygame.Surface((screen_width, screen_height))

# Define variables related to difficulty
num_mines_easy = 5
num_mines_medium = 25
num_mines_hard = 60

clicked = ()
dug = set()


#### CLASS FOR TILE FUNCTIONALITY ####
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

        # convert mouse position to local coordinates on the tiles_surface
        local_pos = pos[0] - 300, pos[1] - 50

        # mouse over button
        if self.rect.collidepoint(local_pos):
            # Left Click!
            if pygame.mouse.get_pressed()[0] == 1 and self.state == "normal":
                clicks += 1
                print(clicks)

                tile_row = int(local_pos[1] // tile_size)
                tile_col = int(local_pos[0] // tile_size)

                clicked = (tile_row, tile_col)

                dug.add(clicked)

                if clicks == 0 or clicks == 1:
                    if self.is_mine or self.adjacent_mines > 0:
                        reset_grid()
                    else:
                        clear_grid(tile, dug)
                else:
                    if self.is_mine:
                        self.image = bomb_tile
                    elif self.adjacent_mines > 0:
                        self.image = number_tiles[self.adjacent_mines - 1]
                        dug.add(clicked)
                    elif self.adjacent_mines == 0:
                        clear_grid(tile, dug)

                    self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
                    self.state = "clicked"
                    action = True

        # draw button on surface instead of screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


num = 0
correct_flag = 0


#### FUNCTIONS ####

# Drawing the the animated surface, Credits to the youtube video that showed me how can be found in the documents.
def draw_bg(surface):
    global num

    if num > -bg_width:
        for x in range(5):
            speed = 1
            for i in bg_images:
                surface.blit(i,
                             (bg_width * x + num * speed, 0))  # making the screen draw attribute linked to the surface
                speed += 1
    else:
        num = 0
        for i in bg_images:
            surface.blit(i, (num, 0))  # making the functions dependent on the surface its blited to

    pygame.display.flip()


scroll = 0


def draw_bg2(surface):
    global scroll

    pixels = math.ceil(screen_width / bg2_width) + 1
    for i in range(0, pixels):
        surface.blit(bg2, (i * bg2_width + scroll, 0))

    scroll -= 2
    if abs(scroll) > bg2_width:
        scroll = 0

    pygame.display.flip()


def display_timer(screen, start_time):
    """
    Display the elapsed time since the game started on the screen.
    """
    timer_font = pygame.font.Font('assets/main_font.ttf', 30)  # Font for the timer text
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    elapsed_time = (current_time - start_time) // 1000  # Calculate elapsed time in seconds
    timer_text = timer_font.render(str(elapsed_time), True, (0, 255, 0))
    text_rect = timer_text.get_rect()
    text_rect.topright = (210, 308)  # Position the timer at the top-right corner of the screen
    screen.blit(timer_text, text_rect)  # Blit the timer text onto the screen


def convert_bomb_tile():
    for cube1 in tiles:
        if cube1.is_mine:
            cube1.image = bomb_tile
            cube1.image = pygame.transform.scale(cube1.image, (tile_size, tile_size))
            cube1.state = 'clicked'

        else:
            cube1.state = 'clicked'

    if continue_button.draw(screen2):
        end_game()


muted = False


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


def clear_grid(tile, dug):
    row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (tile_size + tile_gap)
    dug.add((row, col))

    tile.state = "clicked"
    tile.image = pygame.transform.scale(clicked_tile, (tile_size, tile_size))

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < tiles_per_row and 0 <= col + j < tiles_per_row:
                index = (row + i) * tiles_per_row + (col + j)
                neighbor_tile = tiles[index]

                if neighbor_tile.adjacent_mines == 0 and (row + i, col + j) not in dug:
                    neighbor_tile.state = "clicked"
                    neighbor_tile.image = pygame.transform.scale(clicked_tile, (tile_size, tile_size))
                    clear_grid(neighbor_tile, dug)

                elif neighbor_tile.adjacent_mines > 0:
                    neighbor_tile.state = "clicked"
                    neighbor_tile.image = pygame.transform.scale(number_tiles[neighbor_tile.adjacent_mines - 1],
                                                                 (tile_size, tile_size))

                dug.add((row + i, col + j))


def mines_and_numbers(tiles, num_mines):
    mine_positions = random.sample([(row, col) for row in range(tiles_per_row) for col in range(tiles_per_row)],
                                   num_mines)

    for row, col in mine_positions:
        # Calculate the index of the tile based on row and col
        index = row * tiles_per_row + col
        tiles[index].is_mine = True

    for tile in tiles:
        # Check adjacent tiles and update adjacent_mines
        row, col = tile.rect.y // (tile_size + tile_gap), tile.rect.x // (
                tile_size + tile_gap)  # Determines grid position of tiles

        for i in range(-1, 2):  # Creates a 3*3 grid
            for j in range(-1, 2):
                if 0 <= row + i < tiles_per_row and 0 <= col + j < tiles_per_row:  # Checks to see if neighbouring tile is within the screen2 boundary
                    index = (row + i) * tiles_per_row + (col + j)  # Calculates index of neighbouring tile
                    if tiles[index].is_mine:  # Checks if neighbouring tile is a mine
                        tile.adjacent_mines += 1  # Increments current tile adjacent_mines attribute by 1


def reset_grid():
    print("reset")

    global clicked
    global resets

    # Clear all mine flags and adjacent mine counts
    for tile in tiles:
        tile.is_mine = False
        tile.adjacent_mines = 0
        tile.state = "normal"
        tile.image = pygame.transform.scale(normal_tile, (tile_size, tile_size))  # resizing the image

    # Regenerate new mine positions and update adjacent mine counts
    mines_and_numbers(tiles, num_mines)

    resets += 1
    print("resets:", resets)

    # If there's a clicked tile, update its state and image
    if clicked:
        row, col = clicked
        index = (row - 1) * tiles_per_row + (col - 1)
        tile = tiles[index]
        if tile.is_mine:
            reset_grid()
        elif tile.adjacent_mines > 0:
            reset_grid()
        else:
            clear_grid(tile, dug)
        tile.image = pygame.transform.scale(tile.image, (tile_size, tile_size))
        tile.state = "clicked"

    # Reset clicked variable
    clicked = ()


selected_difficulty = None
clicked_button = None
clicked_button2 = None


def main_menu():
    global selected_difficulty, count, clicked_button, clicked_button2
    global num
    global menu
    menu = True
    while menu == True:
        timer.tick(60)
        # Drawing the scrolling background
        num -= 1
        draw_bg(bg_screen)
        # Blit a clear screen on top of the previous screen to prevent flickering
        global screen
        screen.blit(bg_screen, (0, 0))
        title.draw(screen)

        # Draw the start button
        if start_button.draw(screen):
            start_clicked = True
            clicked_button = start_button
            selected_difficulty = None
            # Redraw the background for the new screen size
            while start_clicked:
                num -= 1
                draw_bg(bg_screen)
                screen.blit(bg_screen, (0, 0))
                global num_mines
                global tile_size
                global tiles_per_row
                # Based on the selected difficulty, you can perform further actions
                if easy_btn.draw(screen) and clicked_button is not start_button:
                    num_mines = num_mines_easy
                    selected_difficulty = 'easy'
                    tiles_per_row = tiles_per_row_easy
                    tile_size = tile_size_easy
                    menu = False
                    game()

                elif medium_btn.draw(screen) and clicked_button is not start_button:
                    num_mines = num_mines_medium
                    selected_difficulty = 'medium'
                    tiles_per_row = tiles_per_row_medium
                    tile_size = tile_size_medium
                    menu = False
                    game()

                elif hard_btn.draw(screen) and clicked_button is not start_button:
                    num_mines = num_mines_hard
                    tiles_per_row = tiles_per_row_hard
                    selected_difficulty = 'hard'
                    tile_size = tile_size_hard
                    menu = False
                    game()

                if clicked_button is not None:
                    clicked_button = None

                if clicked_button2 is not None:
                    clicked_button2 = None

                elif selected_difficulty is None:
                    if back_button.draw(screen):
                        print('BACK')
                        count = 0
                        start_clicked = False
                        clicked_button2 = home_button

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                pygame.display.flip()

        elif exit_button.draw(screen) and clicked_button2 is not home_button:
            print("Exit")
            pygame.quit()
            sys.exit()  # Use sys.exit() instead of exit()

        elif help_button.draw(screen):
            print("HELP")
            help_section()

        elif mute_button.draw(screen):
            print("Toggle Music")
            toggle_mute()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()


def help_section():
    global num
    current_index = 0
    while True:
        num -= 1
        draw_bg(bg_screen)
        screen.blit(bg_screen, (0, 0))
        current_image = help_section_list[current_index]
        screen.blit(current_image, (220, 70))
        # Check for input on left and right arrow buttons
        if right_arrow.draw(screen):
            # Move to the previous image
            if current_index != 5:
                current_index = (current_index + 1) % len(help_section_list)
        if left_arrow.draw(screen):
            # Move to the next image
            if current_index != 0:
                current_index = (current_index -1) % len(help_section_list)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()


def game():
    global tile_size, tile_gap, screen2, tiles, tile, num_mines, count, correct_flag, clicks, resets, board_border
    print("START")
    global looped_once
    looped_once = False
    tile_print = True
    flag_counter = num_mines

    start_time = pygame.time.get_ticks()  # Start the timer

    pygame.time.delay(200)
    screen2 = pygame.display.set_mode((screen_width, screen_height))  # Creating the screen2
    pygame.display.set_caption('Minesweeper')
    screen2.fill("black")
    clicks = 0
    resets = 0
    tile_gap = 1  # this is how you can tell the tiles apart

    tiles = []

    for row in range(tiles_per_row):
        for col in range(tiles_per_row):
            tile = TileFunction(col * (tile_size + tile_gap), row * (tile_size + tile_gap),
                                normal_tile, tile_size, tile_size)
            tiles.append(tile)

    # Randomly place mines and assort numbers
    mines_and_numbers(tiles, num_mines)

    right_click_pressed = False
    win_displayed = False

    # Tile while loop
    while tile_print == True:
        draw_bg2(bg_screen2)
        screen2.blit(bg_screen2, (0, 0))

        # if all the mines are revealed the game ends
        all_mines_revealed = all(tile.image == bomb_tile for tile in tiles if tile.is_mine)

        if count == num_mines:
            looped_once = True
            convert_bomb_tile()

        if not all_mines_revealed:
            for tile in tiles:  # Draws the tiles onto the screen2
                tile.draw(tiles_surface)

        if selected_difficulty == 'hard':
            board_border = pygame.transform.scale(board_border_image, (558, 560))
        else:
            board_border = pygame.transform.scale(board_border_image, (568, 570))

        screen2.blit(tiles_surface, (300, 50))
        tiles_surface.fill((0, 0, 0))
        screen2.blit(board_border, (272, 18))

        # Blitting flag counter
        screen2.blit(flag_counter_image, (60, 228))
        font = pygame.font.Font('assets/main_font.ttf', 30)
        text_surface = font.render(str(flag_counter), True, (0, 255, 0))
        screen2.blit(text_surface, (170, 253))

        # Display timer
        display_timer(screen2, start_time)

        # get mouse position
        pos = pygame.mouse.get_pos()
        # convert mouse position to local coordinates on the tiles_surface
        local_pos = pos[0] - 300, pos[1] - 50

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right mouse button clicked
                    right_click_pressed = True  # Set the flag

                if event.button == 1:
                    # print("left clicked")  # Check if any action was performed
                    for tile in tiles:
                        if tile.rect.collidepoint(local_pos):  # Check which tile was clicked
                            if tile.is_mine and clicks != 0:  # if the tile clicked on was a mine

                                print("You clicked on a mine!")

                                for cube1 in tiles:  # reveals all the mines by iterating through the tiles list finding the mines and changing their image
                                    if cube1.is_mine:
                                        cube1.image = bomb_tile
                                        pygame.display.flip()
                                        cube1.image = pygame.transform.scale(cube1.image, (tile_size, tile_size))
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
                    if tile.rect.collidepoint(local_pos):
                        if tile.state == "normal":  # Right-click to flag
                            tile.image = flag_tile  # changing the state to flag state
                            tile.image = pygame.transform.scale(tile.image,
                                                                (tile_size, tile_size))  # resizing the image
                            tile.state = "flagged"  # Now it's flagged
                            print("flagged")
                            if tile.is_mine:
                                correct_flag += 1
                                if clicks > 0:
                                    flag_counter -= 1

                            else:
                                if clicks > 0:
                                    flag_counter -= 1

                        elif tile.state == "flagged":  # Right-click to unflag
                            tile.image = normal_tile  # changing state back to normal state
                            tile.image = pygame.transform.scale(tile.image,
                                                                (tile_size, tile_size))  # resizing the image
                            tile.state = "normal"  # when the flag is unflagged
                            print("unflagged")
                            if tile.is_mine:
                                correct_flag -= 1
                                if clicks > 0:
                                    flag_counter += 1
                                print("correct flag:", correct_flag)
                            else:
                                if clicks > 0:
                                    flag_counter += 1

            if correct_flag == num_mines and not win_displayed:  # Check if all flags are placed correctly
                # Reveal all mines
                win_game()

                # Print "You win"
                print("You win")

                win_displayed = True
            clicked_tiles = 0
            for tile in tiles:
                if tile.state == "clicked":
                    clicked_tiles += 1

            remaining_tiles = len(tiles) - clicked_tiles
            if remaining_tiles == num_mines:
                convert_bomb_tile()

                win_game()

                print("You win")
                running = False
                win_displayed = True

                game_over == True

            pygame.display.flip()


def win_game():
    convert_bomb_tile()
    screen2.blit(end_screen, (0, 0))
    global num, count, clicked, dug, clicked, clicked_button2
    while True:
        num -= 1
        draw_bg2(bg_screen2)
        screen2.blit(bg_screen2, (0, 0))
        gamewin.draw(screen2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if retry_button.draw(screen2):
            print("Retry")
            count = 0
            clicked = None
            dug.clear()
            game()

        if clicked is not None:
            clicked = None

        elif home_button.draw(screen2):
            print("BACK")
            count = 0
            clicked = None
            clicked_button2 = home_button
            dug.clear()

            main_menu()

        pygame.display.flip()


def end_game():
    convert_bomb_tile()
    # Blit the overlay surface onto the main screen
    screen2.blit(end_screen, (0, 0))
    global num, count, clicked, dug, clicked_button2
    while True:
        num -= 1
        draw_bg2(bg_screen2)
        screen2.blit(bg_screen2, (0, 0))
        gameover.draw(screen2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if retry_button.draw(screen2):
            print("Retry")
            count = 0
            clicked = None
            dug.clear()
            game()

        if clicked_button2 is not None:
            clicked_button2 = None

        elif home_button.draw(screen2):
            print("BACK")
            count = 0
            clicked = None
            clicked_button2 = home_button
            dug.clear()

            main_menu()

        pygame.display.flip()


game_over = False
show_end = False
loop_once_everygame = False
tile_print = True
count = 0

i = 0
# Main Loop
running = True
start_time = time.time()
main_menu()

pygame.quit()
