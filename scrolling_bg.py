import pygame

import sys



# This calls the __init__ functions of every pygame module
pygame.init()



# Setting screen size
screen = pygame.display.set_mode((1066,600))
pygame.display.set_caption("Minesweeper")
timer = pygame.time.Clock()



#bg images
bg_images = []
for i in range(1,6):
    bg_image = pygame.image.load(f"C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/bgs/{i}.png").convert_alpha()
    bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()

num = 0

def draw_bg():
        global num

        if num > -bg_width:
                for x in range(5):
                    speed = 1
                    for i in bg_images:
                        screen.blit(i,(bg_width*x + num*speed,0))
                        speed += 1
        else: 
             num= 0
             for i in bg_images:
                screen.blit(i,(num,0))
        


        pygame.display.flip()
    


#Main Loop
running = True
while running:
    timer.tick(60)
    screen.fill("white")


    draw_bg()


    num -= 1

            


    
# Did the user click the window to close the button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()


