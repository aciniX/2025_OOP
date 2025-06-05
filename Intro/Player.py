import Objects
import pygame
import math

class Player(Objects.Objects):
    def __init__(self, surface, sprite, sPoint, wallSprite, spawnDist, pNum):
        super().__init__(surface, sprite, sPoint)
        self.__speed = 2  # player speed
        self.__height = super().GetSprite().get_height()  # height of sprite
        self.__width = super().GetSprite().get_width()  # width of sprite
        super().SetPos((super().GetPos()[0]//2 - self.__width//2), (super().GetPos()[1]//2 - self.__height//2))  # set spawn location
        if pNum == 0:
            super().SetPos((super().GetPos()[0] - 100), (super().GetPos()[1]))
        else:
            super().SetPos((super().GetPos()[0] + 100), (super().GetPos()[1]))
        self.__rotation_speed = 3  # degrees per frame
        self.__angle = 90  # rotation angle in degrees
        self.__spawnDist = spawnDist  #spawn distance of projectile from player
        self.__lastShotTime = 0  #track of taime taken between shots
        self.__cooldown = 500  # minimum ms between shots taken
        self.__ogCD = self.__cooldown
        self.__wallWidth, self.__wallHeight = wallSprite.get_size()
        self.__pNum = pNum
               
    def Movement(self, keysPressed):      
        # set desired rotation
        if self.__pNum == 0:
            if keysPressed[pygame.K_a]:
                self.__angle += self.__rotation_speed
            if keysPressed[pygame.K_d]:
                self.__angle -= self.__rotation_speed
        else:
            if keysPressed[pygame.K_LEFT]:
                self.__angle += self.__rotation_speed
            if keysPressed[pygame.K_RIGHT]:
                self.__angle -= self.__rotation_speed
        
        # angle conversion from rad to deg for trigonometry
        rad = math.radians(self.__angle)
        super().SetPos((super().GetPos()[0] + math.cos(rad) * self.__speed), (super().GetPos()[1] + -math.sin(rad) * self.__speed))
        #self.__xPos += math.cos(rad) * self.__speed
        #self.__yPos += -math.sin(rad) * self.__speed  # negative because screen y increases downward   
  
    def GetXPos(self):
        return super().GetPos()[0]
    
    def GetYPos(self):
        return super().GetPos()[1]
        
    def GetPos(self):
        return super().GetPos()
       
    def DrawSprite(self):
        # Rotate the original image by the current angle
        rotated_sprite = pygame.transform.rotate(super().GetSprite(), self.__angle - 90)
        # Get the new rect and center it at the current position
        rect = rotated_sprite.get_rect(center=(self.GetCenter()))
        # Draw the rotated image
        super().GetSurface().blit(rotated_sprite, rect.topleft)
        #self.__surface.blit(self.__sprite, (self.__xPos, self.__yPos),)

    def GetRect(self):
        # get rotated hit box
        rotatedSprite = pygame.transform.rotate(super().GetSprite(), self.__angle)
        rect = rotatedSprite.get_rect(center=self.GetCenter())
        # Shrink the rect by 20% in width and height
        return rect.inflate(-rect.width * 0.2, -rect.height * 0.2)
    
    def GetCenter(self):
        # calculate the center position of the sprite
        width, height = super().GetSprite().get_size()
        return (self.GetXPos() + width / 2, self.GetYPos() + height / 2)
    
    def GetAngle(self):
        return self.__angle
    
    def CalcSpawnPoint(self):
        # Use math.cos(angle) and math.sin(angle) to get the forward vector
        # Multiply by the desired distance (10 units)
        # Add to player’s center position
        # Subtract sin from Y to compensate for pygame’s inverted Y axis
        rad = math.radians(self.__angle)
        center = self.GetCenter()
        x = center[0] + math.cos(rad) * self.__spawnDist
        y = center[1] - math.sin(rad) * self.__spawnDist
        return (x, y)
    
    def CalcWallSpawnPoint(self):
        rad = math.radians(self.__angle + 180)  # behind player
        center = self.GetCenter()
        x = center[0] + math.cos(rad) * self.__spawnDist
        y = center[1] - math.sin(rad) * self.__spawnDist
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

    def IsOffScreen(self, width, height):
        # check if object is within screen bounds
        if super().GetPos() is not None:
            x, y = super().GetPos()
            return not (0 <= x <= width and 0 <= y <= height)
        else:
            return False