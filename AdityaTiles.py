import pygame 
from sys import exit 

pygame.init()

screen = pygame.display.set_mode((800,800))
pygame.display.set_caption('Minesweeper')

button_size = 60
button_gap = 1 # this is how you can tell the buttons apart

tile = pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/tile.png")
tile = pygame.transform.scale(tile, (100, 100))  # Resize the tile image to fit the button size

buttons = []
for row in range(8):  
    for col in range(8): 
        button = pygame.Rect(col * (button_size + button_gap), row * (button_size + button_gap), button_size, button_size)
        buttons.append(button)

while True: 
    screen.fill(('grey'))

    for button_rect in buttons:
        screen.blit(tile, button_rect)  # Draw the tile image onto each button position
    
    # buttons
    for button in buttons:
        if button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (180, 180, 180), button)  # when hovering
        
        else:
            pygame.draw.rect(screen, (110, 200, 110), button)  # default color

        if pygame.mouse.get_pressed()[0] == True: 
            for button in buttons:
                if button.collidepoint(pygame.mouse.get_pos()): 
                    buttons.remove(button)
        
    

    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 
        
          
