import pygame
import math
import Player, Wall, Projectile




# initializing all the imported pygame modules
(numpass,numfail) = pygame.init()

pygame.font.init()  # initialise the use of fonts

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

# set fonts
gameFont = pygame.font.Font("Intro\Resources\systemerror.ttf")

#endregion

# sprites
playerSprite = pygame.image.load("Intro\sprites\player.png").convert_alpha()
proSprite = pygame.image.load("Intro\sprites\projectile.png").convert_alpha()
projectileSprite = pygame.transform.scale(proSprite,(8, 8))
wSprite = pygame.image.load("Intro\sprites\wall.png").convert_alpha()
wallSprite = pygame.transform.scale(proSprite,(16, 16))
wallWidth, wallHeight = wallSprite.get_size()

player = Player(surface, playerSprite, screenWidth, screenHeight, wallSprite)  # instantiate player object

walls = []  # wall list
projectiles = []
# obstacles.append(pygame.Rect(100, 100, 50, 300))  # object for collision testing
# obstacles.append(pygame.Rect(200, 200 ,200, 50))
# obstacles.append(Walls(surface, wallSprite, 1200, 500, 1))
# obstacles.append(Walls(surface, wallSprite, 600, 600, 2))

score = 0


# creating a bool value which checks allows the game to run
running = True

#region subroutines
def UpdateScore(s):
    score += s

def SetScore(s):
    score = s

def GetScore():
    return score

def Draw():
    # Changing surface color
    surface.fill(bgColor)  # setting acolor for the background
    
    # draw obstacles
    for obstacle in obstacles:
        # pygame.draw.rect(surface, (255, 255, 0), obstacle)  # Draw the obstacle (yellow)
        obstacle.DrawSprite()

    # draw player    
    player.DrawSprite()

    # draw projectiles
    for projectile in projectiles:
        projectile.DrawSprite()
    
    # draw UI
    surface.blit(txtScore, (10, 10))
    
def CheckCollisions():
    # player --> walls -- trigger death
    player_rect = player.GetRect()
    if len(walls) > 0:
        for wall in walls:
            if player_rect.colliderect(wall.GetRect()):
                print('dead')

    # projectile --> wall
    for projectile in projectiles[:]:
        pRect = projectile.GetRect()
        for wall in walls[:]:
            if pRect.colliderect(wall.GetRect()):
                walls.remove(wall)
                break

def Shoot():
    projectiles.append(Projectile(surface, projectileSprite, player.GetAngle(), player.CalcSpawnPoint()))

def GenerateWall():
    # check distance from last wall spawned to the to wall spawn point on the player, if > distance then spawn wall
    spawn = player.CalcWallSpawnPoint()
        if GetDistance(spawn, self.__lastWallPos) >= self.__wallSpacing:
            walls.append(Wall(surface, wallSprite, spawn, 1))
            self.__lastWallPos = spawn

def GetDistance(a,b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
#endregion

# set text boxes
txtScore = gameFont.render(f"Score: {GetScore()}", True, (255, 255, 255))

# keep game running till running is true (run the game loop while true)
while running: 
    
    # Check for event if user has pushed any event in queue 
    for event in pygame.event.get(): 
          
        # if event is of type quit then set running bool to false 
        if event.type == pygame.QUIT: 
            running = False
               
    # store all keys pressed
    keys = pygame.key.get_pressed()
    # handle player shooting
    if keys[pygame.K_SPACE] and player.CanShoot():
        player.UpdateLastShotTime()

    # call player movement to get new player position
    player.Movement(keys, walls)
    player.UpdateScore()

    for projectile in projectiles:
        projectile.Movement()
        if projectile.IsOffScreen(screenWidth, screenHeight):
            projectiles.remove(projectile)
            Shoot()
    # print(player.GetPos())
    Draw()
    CheckCollisions()
    pygame.display.update()  # update the display    
    clock.tick(cSpeed) # sets the FPS
    