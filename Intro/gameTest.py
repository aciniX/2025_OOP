import pygame
import math
import Player, Wall, Projectile


#region setup
# initializing all the imported pygame modules
(numpass,numfail) = pygame.init()

pygame.font.init()  # initialise the use of fonts

# printing the number of modules initialized successfully
print('Number of modules initialized successfully:', numpass)

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

wallSpacing = 30
#endregion

# sprites
playerSprite = pygame.image.load("Intro\sprites\player.png").convert_alpha()
playerSprite = pygame.transform.scale(playerSprite,(12, 11))
proSprite = pygame.image.load("Intro\sprites\projectile.png").convert_alpha()
projectileSprite = pygame.transform.scale(proSprite,(12, 16))
wSprite = pygame.image.load("Intro\sprites\wall.png").convert_alpha()
wallSprite = pygame.transform.scale(proSprite,(16, 16))
wallWidth, wallHeight = wallSprite.get_size()

player = Player.Player(surface, playerSprite, screenWidth, screenHeight, wallSprite, wallSpacing)  # instantiate player object

walls = []  # wall list
projectiles = []

score = 0
lastScoreInc = pygame.time.get_ticks()

lastWallPos = None
lastWall = None
lastSpawnPoint = None

# creating a bool value which checks allows the game to run
running = True

#region subroutines
def UpdateScore(s):
    global score
    score += s

def SetScore(s):
    global score
    score = s

def GetScore():
    return score

def GameScore():
    global lastScoreInc
    now = pygame.time.get_ticks()
    if (now - lastScoreInc) >= 1000:
        lastScoreInc = now
        UpdateScore(1)

def Draw():
    # Changing surface color
    surface.fill(bgColor)  # setting acolor for the background
    
    # draw obstacles
    for wall in walls:
        # pygame.draw.rect(surface, (255, 255, 0), obstacle)  # Draw the obstacle (yellow)
        wall.DrawSprite()

    # draw player    
    player.DrawSprite()

    # draw projectiles
    for projectile in projectiles:
        projectile.DrawSprite()
    
    # draw UI
    surface.blit(txtScore, (10, 10))

    VisualDebugger()
    
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
    projectiles.append(Projectile.Projectile(surface, projectileSprite, player.GetAngle(), player.CalcSpawnPoint()))

def GenerateWall():
    # check distance from last wall spawned to the to wall spawn point on the player, if > distance then spawn wall
    global lastWall, lastSpawnPoint

    spawn = player.CalcWallSpawnPoint()

    if lastWall == None:
        lastWall = Wall.Walls(surface, wallSprite, spawn, 1)
        lastSpawnPoint = spawn
        walls.append(lastWall)
    elif GetDistance(spawn, lastSpawnPoint) >= wallSpacing/2:
        lastWall = Wall.Walls(surface, wallSprite, spawn, 1)
        lastSpawnPoint = spawn
        walls.append(lastWall)

def GetDistance(a,b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def VisualDebugger():
    # === Debug Lines & Markers ===
    global lastWall
    player_center = player.GetCenter()
    spawn_point = player.CalcWallSpawnPoint()
    
    # Draw line from center to spawn point (wall direction)
    pygame.draw.line(surface, (255, 255, 0), player_center, spawn_point, 2)

    # Draw circle at center of player (green)
    pygame.draw.circle(surface, (0, 255, 0), (int(player_center[0]), int(player_center[1])), 5)

    # Draw circle at spawn point (blue)
    pygame.draw.circle(surface, (0, 0, 255), (int(spawn_point[0]), int(spawn_point[1])), 5)

    # Draw circle at last wall origin/position (yellow)
    if lastWall:
        pygame.draw.circle(surface, (255, 255, 0), (int(lastWall.GetPosition()[0]), int(lastWall.GetPosition()[1])), 5)

    # draw wall spacing radius as a circle
    pygame.draw.circle(surface, (255, 0, 255), (int(player_center[0]), int(player_center[1])), wallSpacing, 1)

    # hitboxes
    pygame.draw.rect(surface, (255, 0, 0), player.GetRect(), 1)
    for projectile in projectiles:
        pygame.draw.rect(surface, (0, 255, 0), projectile.GetRect(), 1)
#endregion

# set text boxes
txtScore = gameFont.render(f"Score: {GetScore()}", True, (255, 255, 255))

#region gameloop
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
        Shoot()

    # call player movement to get new player position
    player.Movement(keys, walls)
    GenerateWall()
    GameScore()
    txtScore = gameFont.render(f"Score: {GetScore()}", True, (255, 255, 255))

    # remove projectiles that go off the screen
    for projectile in projectiles:
        projectile.Movement()
        if projectile.IsOffScreen(screenWidth, screenHeight):
            projectiles.remove(projectile)
            
    Draw()
    CheckCollisions()
    pygame.display.update()  # update the display    
    clock.tick(cSpeed) # sets the FPS
#endregion    