import pygame
import math

#region player
class Player():
    def __init__(self, surface, sprite, xPos, yPos):
        self.__surface = surface
        self.__sprite = sprite
        self.__speed = 2
        self.__height = sprite.get_height()  # height of sprite
        self.__width = sprite.get_width()
        self.__xPos = xPos/2 - self.__width/2  # set spawn to centre of screen
        self.__yPos = yPos/2 - self.__height/2
        self.__rotation_speed = 3  # degrees per frame
        self.__angle = 90  # rotation angle in degrees

    def Movement(self, keysPressed, obstacles):
        old_x = self.__xPos  # save a reference to the players current location
        old_y = self.__yPos

        # set desired rotation
        if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]:
            self.__angle += self.__rotation_speed
        if keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]:
            self.__angle -= self.__rotation_speed

        # angle conversion from rad to deg for trigonometry
        rad = math.radians(self.__angle)
        dx = math.cos(rad) * self.__speed
        dy = -math.sin(rad) * self.__speed  # negative because screen y increases downward

        # if keysPressed[pygame.K_w] or keysPressed[pygame.K_UP]:
        #     self.__yPos -= self.__speed
        # if keysPressed[pygame.K_s] or keysPressed[pygame.K_DOWN]:
        #     self.__yPos += self.__speed

        # always move forward
        self.__xPos += dx
        self.__yPos += dy        
        
        # if player desired position collides with object dont move it
        player_rect = self.GetRect() # Check collisions
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                self.__xPos = old_x
                self.__yPos = old_y
    
    def GetXPos(self):
        return self.__xPos
    
    def GetYPos(self):
        return self.__yPos
    
    def GetPos(self):
        return (self.__xPos, self.__yPos)
    
    def DrawSprite(self):
        # Rotate the original image by the current angle
        rotated_sprite = pygame.transform.rotate(self.__sprite, self.__angle - 90)
        # Get the new rect and center it at the current position
        rect = rotated_sprite.get_rect(center=(self.__xPos, self.__yPos))
        # Draw the rotated image
        self.__surface.blit(rotated_sprite, rect.topleft)
        #self.__surface.blit(self.__sprite, (self.__xPos, self.__yPos),)

    def GetRect(self):
        return pygame.Rect(self.__xPos, self.__yPos, self.__width, self.__height)    
#endregion player

#region walls
class Walls():
    def __init__(self, surface, sprite, xPos, yPos, owner):
        self.__surface = surface
        self.__sprite = sprite
        self.__height = sprite.get_height()  # height of sprite
        self.__width = sprite.get_width()
        self.__xPos = xPos/2 - self.__width/2  # set spawn to centre of screen
        self.__yPos = yPos/2 - self.__height/2
        self.__owner = owner
        if owner == 1:
            sprite.fill(255, 255, 0)
        else:
            sprite.fill(0, 255, 255)
        
        def DrawSprite(self):
            self.__surface.blit(self.__sprite, (self.__xPos, self.__yPos),)

        def GetRect(self):
            return pygame.Rect(self.__xPos, self.__yPos, self.__width, self.__height)
        
        def DestroyObject(self, objectList):
            objectList.remove(self)

        def CheckWallCollision(self, objectList):
            print('check')
            thisRect = GetRect()
            for object in objectList:
                if thisRect.collideRect(object):
                    return True
            return False
 

#endregion walls
# initializing all the imported pygame modules
(numpass,numfail) = pygame.init()
 
# printing the number of modules initialized successfully
print('Number of modules initialized successfully:', numpass)

#region setup
# resolution of the window
screenWidth = 1280
screenHeight = 720 
pygame.display.set_mode((screenWidth, screenHeight))

# Initializing RGB Color
bgColor = (0, 120, 120)

# Creating a reference to the surface
surface = pygame.display.get_surface()

# set title in the title bar
title = 'Game Test'
pygame.display.set_caption(title)

# set a reference to the clock speed
clock = pygame.time.Clock()
cSpeed = 60  # limit the FPS

#endregion

# player shape
# player = pygame.Rect(150, 150, 50, 50)
playerSprite = pygame.image.load("Intro\sprites\player.png").convert_alpha()
wallSprite = pygame.image.load("Intro\sprites\wall.png").convert_alpha()
# surface.blit(playerSprite, (20,20),)  # needs to move to draw function

player = Player(surface, playerSprite, screenWidth, screenHeight)  # instantiate player object

obstacles = []  # obstacle list
obstacles.append(pygame.Rect(100, 100, 50, 300))  # object for collision testing
obstacles.append(pygame.Rect(200, 200 ,200, 50))

def Draw():
    # Changing surface color
    surface.fill(bgColor)  # setting acolor for the background
    # pygame.draw.rect(surface, (255, 0, 0), player)
    # surface.blit(playerSprite, (20,20),)
    for obstacle in obstacles:
        pygame.draw.rect(surface, (255, 255, 0), obstacle)  # Draw the obstacle (yellow)

    player.DrawSprite()
    
# creating a bool value which checks allows the game to run
running = True
  
# keep game running till running is true (run the game loop while true)
while running: 
    
    # Check for event if user has pushed any event in queue 
    for event in pygame.event.get(): 
          
        # if event is of type quit then set running bool to false 
        if event.type == pygame.QUIT: 
            running = False
               
    # store all keys pressed
    keys = pygame.key.get_pressed()
    # call player movement to get new player position
    player.Movement(keys, obstacles)
        
    # print(player.GetPos())
    Draw()
    pygame.display.update()  # update the display    
    clock.tick(cSpeed) # sets the FPS
    