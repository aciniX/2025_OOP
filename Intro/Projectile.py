import Objects
import math, pygame

class Projectile(Objects.Objects):
    def __init__(self, surface, sprite, angle, sPoint):
        super().__init__(surface, sprite, sPoint)
        self.__angle = angle  # set projectile to the angle the player is at on spawn
        self.__speed = 10  # projectile speed

    def Movement(self):
        rad = math.radians(self.__angle)  # convert angle to radians
        # calculate and set angular movement positions
        x, y = super().GetPos()
        x += math.cos(rad) * self.__speed
        y -= math.sin(rad) * self.__speed
        super().SetPos(x,y)
    
    def GetRect(self):
        # return projectile hit box (rotated)
        rotatedSprite = pygame.transform.rotate(super().GetSprite(), self.__angle - 90)
        rect = rotatedSprite.get_rect(center=self.GetCenter())
        return rect
    
    def GetCenter(self):
        return (super().GetPos())
     
    def DrawSprite(self):
        # Rotate the original image by the current angle
        rotated_sprite = pygame.transform.rotate(super().GetSprite(), self.__angle -90)
        # Get the new rect and center it at the current position
        rect = rotated_sprite.get_rect(center=(super().GetPos()))
        # Draw the rotated image
        super().GetSurface().blit(rotated_sprite, rect.topleft)
        #self.__surface.blit(super().GetSprite(), (self.__xPos, self.__yPos),)

        # visual debugging
        # pygame.draw.circle(self.__surface, (255, 255, 0), (int(self.__xPos), int(self.__yPos)), 5)

    def IsOffScreen(self, width, height):
        # check if object is within screen bounds
        if super().GetPos() is not None:
            x, y = super().GetPos()
            return not (0 <= x <= width and 0 <= y <= height)
        else:
            return False
