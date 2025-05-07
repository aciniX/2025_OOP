# importing the library
import pygame
import random

class Shape:  # Parent Class
    def __init__(self, surface, color, xPos, yPos):
        self.__surface = surface
        self.__color = color
        self.__xPos = xPos
        self.__yPos = yPos
    
    def ReadSurface(self):
        return self.__surface
    
    def ReadColor(self):
        return self.__color

    def ReadXPos(self):
        # read the value of an attribute
        return self.__xPos
    
    def ReadYPos(self):
        return self.__yPos

    def SetXPos(self, moveValue):
        # set/change the value of an attribute
        self.__xPos = moveValue

class DrawRect(Shape):  # inheriting from parent class
    def __init__(self, surface, color, xPos, yPos, width, height):
        super().__init__(surface, color, xPos, yPos)
        self.__width = width
        self.__height = height
        # __ means that the attribute is protected and cannot be directly accessed by another object

    def DrawShape(self):
        pygame.draw.rect(self.ReadSurface(), self.ReadColor(), [self.ReadXPos(), self.ReadYPos(), self.__width, self.__height], 0)
        # pygame.display.update()

    def SetXPos(self, moveValue):  # overriding the parent class
        # setting a new position by reading the current X position and subtracting a inputted value
        newPos = self.ReadXPos() - moveValue
        # running the parent version of this method and sending a new position for it to go to  
        super().SetXPos(newPos)   

class DrawCirle(Shape):  # inheriting from parent class
    def __init__(self, surface, color, xPos, yPos, radius):
        # surface, color, center, radius, linewidth
        super().__init__(surface, color, xPos, yPos)
        self.__radius = radius
    
    def DrawShape(self):
        pygame.draw.circle(self.ReadSurface(), self.ReadColor(), [self.ReadXPos(), self.ReadYPos()], self.__radius, 0)


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
shapeList = []  # store out rect objects
for i in range(5):
    col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    sizeX = random.randint(1,250)
    sizeY = random.randint(1,250)
    posX = random.randint(0, screenWidth - sizeX)
    posY = random.randint(0, screenHeight - sizeY)
    shapeList.append(DrawRect(surface, col, posX, posY, sizeX, sizeY))
    # print(rectList[i].ReadXPos())

for n in range(5):
    col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    radius = random.randrange(1,100)
    posX = random.randint(0, screenWidth - radius)
    posY = random.randint(0, screenHeight - radius)
    shapeList.append(DrawCirle(surface, col, posX, posY, radius))

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
    
    DrawShapes(shapeList)
    # DrawShapes(circleList)
    MoveShapes(shapeList, 1)
      
    
    #pygame.display.flip()  # render the bgcolor
    pygame.display.update()  # update the display

