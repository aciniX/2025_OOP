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
resolution = (screenWidth, screenHeight)
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
gameFont = pygame.font.Font("Intro\Resources\systemerror.ttf", 24)

wallSpacing = 30
#endregion

# sprites
playerSprite = []
playerSprite.append(pygame.image.load("Intro\sprites\pGreen.png"))
playerSprite.append(pygame.image.load("Intro\sprites\pRed.png"))
playerSprite[0] = pygame.transform.scale(playerSprite[0],(12, 11)).convert_alpha()
playerSprite[1] = pygame.transform.scale(playerSprite[1],(12, 11)).convert_alpha()
proSprite = pygame.image.load("Intro\sprites\projectile.png")
projectileSprite = pygame.transform.scale(proSprite,(12, 16)).convert_alpha()
wSprite = pygame.image.load("Intro\sprites\wall.png")
wallSprite = pygame.transform.scale(proSprite,(16, 16)).convert_alpha()
wallWidth, wallHeight = wallSprite.get_size()

# instantiate players
#player = Player.Player(surface, playerSprite, resolution, wallSprite, wallSpacing, 1)  # instantiate player object

# object lists
players = []
walls = []  # wall list
projectiles = []

# score
score = 0
pScores = [0,0]
lastScoreInc = pygame.time.get_ticks()

# walls
lastWallPos = [None, None]
lastWall = [None, None]
lastSpawnPoint = [None, None]

# player deaath states
dead = [False, False]

# creating a bool value which checks allows the game to run
running = True

#region subroutines
def NewGame():
    global players
    for i in range(2):
        players.append(Player.Player(surface, playerSprite[i], resolution, wallSprite, wallSpacing, i))

def UpdateScore(s):
    global score
    score += s

def SetScore(s):
    global score
    score = s

def GetScore():
    return score

def GetPScore(pNum):
    return pScores[pNum]

def SetPScore(pNum,s):
    pScores[pNum] = s

def UpdatePScore(pNum,s):
    pScores[pNum] += s

def GameScore():
    # increment score each second
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
    for player in players:    
        player.DrawSprite()

    # draw projectiles
    for projectile in projectiles:
        projectile.DrawSprite()
    
    # draw UI
    txtScoreRect = txtScore.get_rect(center=(screenWidth/2, 10))
    surface.blit(txtScore, txtScoreRect)
    txtP1ScoreRect = txtP1Score.get_rect(center=(screenWidth/5,10))
    surface.blit(txtP1Score, txtP1ScoreRect)
    txtP2ScoreRect = txtP2Score.get_rect(center=(4*screenWidth/5,10))
    surface.blit(txtP2Score, txtP2ScoreRect)

    # display hit boxes and object centers
    # VisualDebugger()
    
def CheckCollisions():
    global dead
    
    # if player hit player
    if players[0].GetRect().colliderect(players[1].GetRect()):
        GameOver(3)

    # player --> walls -- trigger death
    for i in range(len(players)):
        player_rect = players[i].GetRect()  # reference player hit box
        if len(walls) > 0:
            dead[i] = False
            for wall in walls:
                if player_rect.colliderect(wall.GetRect()):
                    dead[i] = True
                    GameOver(i)
                    break
        # player collide with projectile
        if len(projectiles) > 0:
            dead[i] = False
            for projectile in projectiles:
                if player_rect.colliderect(projectile.GetRect()):
                    dead[i] = True
                    GameOver(i)
                    break
        
        

    # projectile --> wall
    for projectile in projectiles[:]:
        pRect = projectile.GetRect()  # reference projectile hit box
        for wall in walls[:]:
            if pRect.colliderect(wall.GetRect()):
                walls.remove(wall)
                break

def GameOver(pNum):
    # wipe out all objects
    players.clear()
    walls.clear()
    projectiles.clear()

    # update scores
    if pNum <= 1:
        if pNum == 0:
            pNum = 1
        else:
            pNum = 0
        UpdatePScore(pNum, GetScore())
    SetScore(0)
    Draw()

    # instantiate players
    NewGame()

def Shoot(pNum):
    projectiles.append(Projectile.Projectile(surface, projectileSprite, players[pNum].GetAngle(), players[pNum].CalcSpawnPoint()))

def GenerateWall(pNum):
    # check distance from last wall spawned to the to wall spawn point on the player, if > distance then spawn wall
    global lastWall, lastSpawnPoint

    spawn = players[pNum].CalcWallSpawnPoint()

    if lastWall[pNum] == None:  # if no walls exist
        lastWall[pNum] = Wall.Walls(surface, wallSprite, spawn, pNum)
        lastSpawnPoint[pNum] = spawn
        walls.append(lastWall[pNum])
    elif GetDistance(spawn, lastSpawnPoint[pNum]) >= wallSpacing/2:  # check if distance between last wall and wall spawn is large enough
        lastWall[pNum] = Wall.Walls(surface, wallSprite, spawn, pNum)
        lastSpawnPoint[pNum] = spawn
        walls.append(lastWall[pNum])

def GetDistance(a,b):
    # calculate straight line distance between 2 points
    return math.hypot(a[0] - b[0], a[1] - b[1])

def VisualDebugger():
    global dead
    # === Debug Lines & Markers ===
    global lastWall
    for player in players:
        player_center = player.GetCenter()
        spawn_point = player.CalcWallSpawnPoint()
        proj_spawn = player.CalcSpawnPoint()
    
        # Draw line from center to spawn point (wall direction)
        pygame.draw.line(surface, (255, 255, 0), player_center, spawn_point, 2)

        # Draw circle at center of player (green)
        if dead:
            pygame.draw.circle(surface, (255, 0, 0), (int(player_center[0]), int(player_center[1])), 5)
        else:
            pygame.draw.circle(surface, (0, 255, 0), (int(player_center[0]), int(player_center[1])), 5)

        # Draw circle at spawn point (blue)
        pygame.draw.circle(surface, (0, 0, 255), (int(spawn_point[0]), int(spawn_point[1])), 5)
        # Draw circle at spawn point
        pygame.draw.circle(surface, (0, 255, 255), (int(proj_spawn[0]), int(proj_spawn[1])), 5)

        # draw wall spacing radius as a circle
        pygame.draw.circle(surface, (255, 0, 255), (int(player_center[0]), int(player_center[1])), wallSpacing, 1)

    # Draw circle at last wall origin/position (yellow)
    if lastWall:
        pygame.draw.circle(surface, (255, 255, 0), (int(lastWall.GetPosition()[0]), int(lastWall.GetPosition()[1])), 5)

    # hitboxes
    pygame.draw.rect(surface, (255, 0, 0), player.GetRect(), 1)
    for projectile in projectiles:
        pygame.draw.rect(surface, (0, 255, 0), projectile.GetRect(), 1)
    for wall in walls:
        pygame.draw.rect(surface, (0, 255, 255), wall.GetRect(), 1)
#endregion

# instantiate players
NewGame()

# set text boxes
txtScore = gameFont.render(f"Score: {GetScore()}", True, (255, 255, 255))
txtP1Score = gameFont.render(f"Player 1: {GetPScore(0)}", True, (255, 255, 255))
txtP2Score = gameFont.render(f"Player 2: {GetPScore(1)}", True, (255, 255, 255))

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
    if keys[pygame.K_SPACE] and players[0].CanShoot():
        players[0].UpdateLastShotTime()
        Shoot(0)
    if keys[pygame.K_UP] and players[1].CanShoot():
        players[1].UpdateLastShotTime()
        Shoot(1)

    # call player movement to get new player position
    for i in range(len(players)):
        players[i].Movement(keys)
        # check if leave screen
        if players[i].IsOffScreen(screenWidth,screenHeight):
            GameOver(i)

    # generate walls while players move
    for i in range(len(players)):
        GenerateWall(i)

    # increment score / time
    GameScore()
    txtScore = gameFont.render(f"Score: {GetScore()}", True, (255, 255, 255))
    txtP1Score = gameFont.render(f"Player 1: {GetPScore(0)}", True, (255, 255, 255))
    txtP2Score = gameFont.render(f"Player 2: {GetPScore(1)}", True, (255, 255, 255))

    # remove projectiles that go off the screen
    for projectile in projectiles:
        projectile.Movement()
        if projectile.IsOffScreen(screenWidth, screenHeight):
            projectiles.remove(projectile)

    # render the game        
    Draw()

    # check for any collisions
    CheckCollisions()

    pygame.display.update()  # update the display    
    clock.tick(cSpeed) # sets the FPS
#endregion