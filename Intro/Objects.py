class Objects():
    def __init__(self, surface, sprite, sPoint):
        self.__surface = surface  # surface to draw on
        self.__sprite = sprite  # sprite to draw
        self.__xPos = sPoint[0]  # x spawn point
        self.__yPos = sPoint[1]  # y spawn point
        
    def GetPos(self):
        # current object position
        return (self.__xPos, self.__yPos)
    
    def SetPos(self, x, y):
        self.__xPos = x
        self.__yPos = y

    def GetSprite(self):
        return self.__sprite
    
    def GetSurface(self):
        return self.__surface
    
    
    