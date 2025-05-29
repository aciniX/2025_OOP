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
        self.__xPos = float(xPos//2 - self.__width//2)  # set spawn to centre of screen
        self.__yPos = float(yPos//2 - self.__height//2)
        self.__rotation_speed = 3  # degrees per frame
        self.__angle = 90  # rotation angle in degrees
        self.__spawnDist = 20  #spawn distance of projectile from player
        self.__lastShotTime = 0  #track of taime taken between shots
        self.__cooldown = 500  # minimum ms between shots taken
        self.__ogCD = self.__cooldown
        self.__wall_spacing = 10  # Minimum distance before next wall
        self.__last_wall_pos = (self.__xPos, self.__yPos)


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
        self.__xPos += math.cos(rad) * self.__speed
        self.__yPos += -math.sin(rad) * self.__speed  # negative because screen y increases downward

        if keysPressed[pygame.K_SPACE] and self.CanShoot():
            self.Shoot()
            self.UpdateLastShotTime()

        # if player desired position collides with object dont move it
        player_rect = self.GetRect() # Check collisions
        if len(obstacles) > 0:
            for obstacle in obstacles:
                if player_rect.colliderect(obstacle.GetRect()):
                    self.__xPos = old_x
                    self.__yPos = old_y
        


        # self.__wallSpawn = self.CalcWallSpawnPoint(self.__xPos, self.__yPos, -self.__spawnDist, self.__angle)
        self.SpawnWall()

    @staticmethod
    def GetDistance(a,b):
        return math.hypot(a[0] - b[0], a[1] - b[1])
    
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
    
    def GetCenter(self):
        x = self.__xPos + self.__sprite.get_width()/2
        y = self.__yPos + self.__sprite.get_height()/2
        return (x,y)
    
    def GetAngle(self):
        return self.__angle
    
    def CalcSpawnPoint(self):
        # Use math.cos(angle) and math.sin(angle) to get the forward vector
        # Multiply by the desired distance (10 units)
        # Add to player’s center position
        # Subtract sin from Y to compensate for pygame’s inverted Y axis
        rad = math.radians(self.__angle)
        xSpawn = self.__xPos + math.cos(rad) * self.__spawnDist
        ySpawn = self.__yPos - math.sin(rad) * self.__spawnDist
        return (xSpawn, ySpawn)
    
    def CalcWallSpawnPoint(self):
        rad = math.radians(self.__angle + 180)  # behind player
        center = self.GetCenter()
        x = center[0] + math.cos(rad) * self.__spawnDist
        y = center[1] - math.sin(rad) * self.__spawnDist

        x -= wallWidth / 2
        y -= wallHeight / 2

        return (x,y)

    def SpawnWall(self):
        spawn = self.CalcWallSpawnPoint()
        if self.GetDistance(spawn, self.__last_wall_pos) >= self.__wall_spacing:
            obstacles.append(Walls(surface, wallSprite, self.CalcWallSpawnPoint(), 1))
            self.__last_wall_pos = spawn

    def Shoot(self):
        projectiles.append(Projectile(self.__surface, projectileSprite, self.__angle, self.CalcSpawnPoint()))

    def CanShoot(self):
        now = pygame.time.get_ticks()
        return now - self.__lastShotTime >= self.__cooldown

    def UpdateLastShotTime(self):
        self.__lastShotTime = pygame.time.get_ticks()

    def SetCooldown(self, value):
        self.__cooldown = value

    def ChangeCooldown(self, value):
        self.__cooldown += value
    
    def ResetCoolDown(self):
        self.__cooldown = self.__ogCD
#endregion player

#region projectile
class Projectile():
    def __init__(self, surface, sprite, angle, sPoint):
        self.__surface = surface
        self.__sprite = sprite
        self.__angle = angle
        self.__height = sprite.get_height()  # height of sprite
        self.__width = sprite.get_width()
        self.__xPos = int(sPoint[0])
        self.__yPos = int(sPoint[1])
        self.__speed = 10

    def Movement(self):
        rad = math.radians(self.__angle)
        self.__xPos += math.cos(rad) * self.__speed
        self.__yPos -= math.sin(rad) * self.__speed
    
    def GetRect(self):
        return pygame.Rect(self.__xPos, self.__yPos, self.__width, self.__height)
    
    def DrawSprite(self):
        # Rotate the original image by the current angle
        rotated_sprite = pygame.transform.rotate(self.__sprite, self.__angle - 90)
        # Get the new rect and center it at the current position
        rect = rotated_sprite.get_rect(center=(self.__xPos, self.__yPos))
        # Draw the rotated image
        self.__surface.blit(rotated_sprite, rect.topleft)
        #self.__surface.blit(self.__sprite, (self.__xPos, self.__yPos),)

    def IsOffScreen(self, width, height):
        #check if object is within screen bounds
        return not (0 <= self.__xPos <= width and 0 <= self.__yPos <= height)
#endregion

#region walls
class Walls():
    def __init__(self, surface, sprite, sPoint, owner):
        self.__surface = surface
        self.__sprite = sprite
        self.__height = sprite.get_height()  # height of sprite
        self.__width = sprite.get_width()
        self.__xPos = sPoint[0]
        self.__yPos = sPoint[1]
        self.__owner = owner
        self.__name = "WALL"
        print(self.__owner)
        if self.__owner == 1:
            self.__color = (255, 0, 0)
        else:
            self.__color = (0, 255, 0)
        self.__sprite.fill(self.__color)
        
        #if self.CheckWallCollision(obstacles):
        #    self.DestroyObject(obstacles)
    
    def __del__(self):
        print(f"Object {self.__name} {self.__owner} destroyed")
        
    def DrawSprite(self):
        self.__surface.blit(self.__sprite, (self.__xPos, self.__yPos),)

    def GetRect(self):
        return pygame.Rect(self.__xPos, self.__yPos, self.__width, self.__height)
        
    def DestroyObject(self, objectList):
        objectList.remove(self)
        # del(self)

    def CheckWallCollision(self, objectList):
        print('check')
        # thisRect = pygame.Rect(self.__xPos, self.__yPos, self.__width, self.__height)
        for object in objectList:
            if self.GetRect().colliderect(object.GetRect()):
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
# playerSprite.set_colorkey((255,0,0))
proSprite = pygame.image.load("Intro\sprites\projectile.png").convert_alpha()
projectileSprite = pygame.transform.smoothscale(proSprite,(8, 8))
wallSprite = pygame.image.load("Intro\sprites\wall.png").convert_alpha()
wallWidth, wallHeight = wallSprite.get_size()
# surface.blit(playerSprite, (20,20),)  # needs to move to draw function

player = Player(surface, playerSprite, screenWidth, screenHeight)  # instantiate player object

obstacles = []  # obstacle list
projectiles = []
# obstacles.append(pygame.Rect(100, 100, 50, 300))  # object for collision testing
# obstacles.append(pygame.Rect(200, 200 ,200, 50))
# obstacles.append(Walls(surface, wallSprite, 1200, 500, 1))
# obstacles.append(Walls(surface, wallSprite, 600, 600, 2))

def Draw():
    # Changing surface color
    surface.fill(bgColor)  # setting acolor for the background
    # pygame.draw.rect(surface, (255, 0, 0), player)
    # surface.blit(playerSprite, (20,20),)
    for obstacle in obstacles:
        # pygame.draw.rect(surface, (255, 255, 0), obstacle)  # Draw the obstacle (yellow)
        obstacle.DrawSprite()
    player.DrawSprite()

    for projectile in projectiles:
        projectile.DrawSprite()
    
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

    for projectile in projectiles:
        projectile.Movement()
        if projectile.IsOffScreen(screenWidth, screenHeight):
            projectiles.remove(projectile)
        
    # print(player.GetPos())
    Draw()
    pygame.display.update()  # update the display    
    clock.tick(cSpeed) # sets the FPS
    