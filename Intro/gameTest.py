import pygame

# initializing all the importe
# pygame modules
(numpass,numfail) = pygame.init()
 
# printing the number of modules 
# initialized successfully
print('Number of modules initialized successfully:', numpass)

# displaying a window of height 
# resolution of the window
screenWidth = 1280
screenHeight = 720 
pygame.display.set_mode((screenWidth, screenHeight))

# Initializing RGB Color
bgColor = (0, 0, 0)

# Creating a reference to the surface
surface = pygame.display.get_surface()

# Changing surface color
surface.fill(bgColor)  # setting acolor for the background
pygame.display.flip()  # render the bgcolor

# set title in the title bar
title = 'Intro to pygame'
pygame.display.set_caption(title) 

# creating a bool value which checks allows the game to run
running = True
  
# keep game running till running is true (run the game loop while true)
while running: 
    
    # Check for event if user has pushed any event in queue 
    for event in pygame.event.get(): 
          
        # if event is of type quit then set running bool to false 
        if event.type == pygame.QUIT: 
            running = False
    
    
    pygame.display.update()  # update the display