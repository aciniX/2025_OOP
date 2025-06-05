import Objects
import pygame

class Walls(Objects.Objects):
    def __init__(self, surface, sprite, sPoint, owner, origin=(0,0)):
        super().__init__(surface, sprite, sPoint)
        super().SetPos(super().GetPos()[0], super().GetPos()[1])  # set position
        self.__owner = owner  # set owner of object
        self.__name = "WALL"
        self.__origin = origin
        if self.__owner == 1:
            self.__color = (255, 0, 0)
        else:
            self.__color = (0, 255, 0)
            
    def GetPosition(self):
        return (super().GetPos()[0], super().GetPos()[1])

    def DrawSprite(self):
        sprite_rect = super().GetSprite().get_rect(center=(super().GetPos()[0], super().GetPos()[1]))
        super().GetSprite().fill(self.__color)
        super().GetSurface().blit(super().GetSprite(), sprite_rect)
        # pygame.draw.circle(self.__surface, (0, 255, 0), (self.__xPos, self.__yPos), 3)  # visual debugging

    def GetRect(self):
        sprite_rect = super().GetSprite().get_rect(center=(super().GetPos()[0], super().GetPos()[1]))
        return sprite_rect
    
    def GetCenter(self):
        return (super().GetPos()[0], super().GetPos()[1])
    
    def GetOrigin(self):
        return self.__origin
    
    