import pygame
import math

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
