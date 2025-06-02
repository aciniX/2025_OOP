import pygame

class Walls():
    def __init__(self, surface, sprite, sPoint, owner, origin=(0,0)):
        self.__surface = surface
        self.__sprite = sprite
        self.__height = sprite.get_height()  # height of sprite
        self.__width = sprite.get_width()
        self.__centerX = sPoint[0]
        self.__centerY = sPoint[1]
        self.__owner = owner
        self.__name = "WALL"
        self.__origin = origin
        # print(self.__owner)
        if self.__owner == 1:
            self.__color = (255, 0, 0)
        else:
            self.__color = (0, 255, 0)
        self.__sprite.fill(self.__color)
            
    def GetPosition(self):
        return (self.__centerX, self.__centerY)

    def DrawSprite(self):
        sprite_rect = self.__sprite.get_rect(center=(self.__centerX, self.__centerY))
        self.__surface.blit(self.__sprite, sprite_rect)
        pygame.draw.circle(self.__surface, (0, 255, 0), (self.__centerX, self.__centerY), 3)

    def GetRect(self):
        sprite_rect = self.__sprite.get_rect(center=(self.__centerX, self.__centerY))
        return sprite_rect
    
    def GetCenter(self):
        return (self.__centerX, self.__centerY)
    
    def GetOrigin(self):
        return self.__origin
    
    