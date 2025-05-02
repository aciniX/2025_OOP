# importing the library
import pygame

class DrawRect:
    def __init__(self, surface, color, xPos, yPos, width, height):
        self.surface = surface
        self.color = color
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height

    def DrawShape(self):
        pygame.draw.rect(self.surface, self.color, [self.xPos, self.yPos, self.width, self.height], 0)
        # pygame.display.update()

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

rect1 = DrawRect(surface, (0, 0, 255), 100, 100, 400, 100)
rect2 = DrawRect(surface, (0, 255, 0), screenWidth, screenHeight, 200, 50)
# creating a bool value which checks allows the game to run
running = True
  
# keep game running till running is true (run the game loop while true)
while running: 
    
    # Check for event if user has pushed any event in queue 
    for event in pygame.event.get(): 
          
        # if event is of type quit then set running bool to false 
        if event.type == pygame.QUIT: 
            running = False
    
    # Changing surface color
    surface.fill(bgColor)  # setting acolor for the background

    # Using draw.rect module of
    # pygame to draw the outlined rectangle
    # (what we draw on, color of shape, size and position of shape, width of outline)
    # pygame.draw.rect(surface, (0, 0, 255), [100, 100, 400, 100], 0)
    rect1.DrawShape()
    rect2.DrawShape()  
    
    #pygame.display.flip()  # render the bgcolor
    pygame.display.update()  # update the display

