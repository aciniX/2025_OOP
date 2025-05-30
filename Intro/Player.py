import pygame
import math

class Player():
    def __init__(self, surface, sprite, xPos, yPos, wallSprite):
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
        self.__wallSpacing = 14  # Minimum distance before next wall
        self.__lastWallPos = (self.__xPos, self.__yPos)
        self.__lastScoreInc = 0
        self.__wallWidth, self.__wallHeight = wallSprite.GetSize()
        

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

        # self.__wallSpawn = self.CalcWallSpawnPoint(self.__xPos, self.__yPos, -self.__spawnDist, self.__angle)
        self.SpawnWall()

    
    
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

        x -= self.__wallWidth / 2
        y -= self.__wallHeight / 2

        return (x,y)

        

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

    def UpdateScore(self):
        now = pygame.time.get_ticks()
        if (now - self.__lastScoreInc) >= 10:
            self.__lastScoreInc = now
            UpdateScore(1)