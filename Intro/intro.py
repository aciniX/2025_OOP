# importing the library
import pygame
import random

class DrawRect:
    def __init__(self, surface, color, xPos, yPos, width, height):
        self.__surface = surface
        self.__color = color
        self.__xPos = xPos
        self.__yPos = yPos
        self.__width = width
        self.__height = height
        # __ means that the attribute is protected and cannot be directly accessed by another object

    def DrawShape(self):
        pygame.draw.rect(self.__surface, self.__color, [self.__xPos, self.__yPos, self.__width, self.__height], 0)
        # pygame.display.update()
    
    def ReadXPos(self):
        # read the value of an attribute
        return self.__xPos
    
    def SetXPos(self, moveValue):
        # set/change the value of an attribute
        self.__xPos += moveValue


def DrawShapes(shapeList):
    for shape in shapeList:
        shape.DrawShape()

def MoveShapes(shapeList, moveValue):
    for shape in shapeList:
        shape.SetXPos(moveValue)
        # shape.__yPos += moveValue
        


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

# instantiate objects from the DrawRect class
# rect1 = DrawRect(surface, (0, 0, 255), 100, 100, 400, 100)
# rect2 = DrawRect(surface, (0, 255, 0), screenWidth, screenHeight, 200, 50)
rectList = []  # store out rect objects
for i in range(5):
    col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    sizeX = random.randint(1,250)
    sizeY = random.randint(1,250)
    posX = random.randint(0, screenWidth - sizeX)
    posY = random.randint(0, screenHeight - sizeY)
    rectList.append(DrawRect(surface, col, posX, posY, sizeX, sizeY))
    # print(rectList[i].ReadXPos())
    

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
    # rect1.DrawShape()
    # rect2.DrawShape()
    MoveShapes(rectList, 1)
    DrawShapes(rectList)
      
    
    #pygame.display.flip()  # render the bgcolor
    pygame.display.update()  # update the display

