import pygame

class Walls():
    def __init__(self, surface, sprite, sPoint, owner, origin=(0,0)):
        self.__surface = surface
        self.__sprite = sprite
        self.__height = sprite.get_height()  # height of sprite
        self.__width = sprite.get_width()
        self.__xPos = sPoint[0]
        self.__yPos = sPoint[1]
        self.__owner = owner
        self.__name = "WALL"
        self.__origin = origin
        # print(self.__owner)
        if self.__owner == 1:
            self.__color = (255, 0, 0)
        else:
            self.__color = (0, 255, 0)
        self.__sprite.fill(self.__color)
        
        #if self.CheckWallCollision(obstacles):
        #    self.DestroyObject(obstacles)
    
    # def __del__(self):
    #     print(f"Object {self.__name} {self.__owner} destroyed")
    
    def GetPosition(self):
        width, height = self.__sprite.get_size()
        return (self.__xPos + width / 2, self.__yPos + height / 2)

    def DrawSprite(self):
        sprite_rect = self.__sprite.get_rect(center=(self.__xPos, self.__yPos))
        self.__surface.blit(self.__sprite, sprite_rect)
        pygame.draw.circle(self.__surface, (0, 255, 0), (self.__xPos, self.__yPos), 3)

    def GetRect(self):
        return pygame.Rect(self.__xPos, self.__yPos, self.__width, self.__height)
    
    def GetCenter(self):
        width, height = self.__sprite.get_size()
        return (self.__xPos + width / 2, self.__yPos + height / 2)
    
    def GetOrigin(self):
        return self.__origin
    
    