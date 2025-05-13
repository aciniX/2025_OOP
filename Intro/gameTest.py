import pygame

# initializing all the imported pygame modules
(numpass,numfail) = pygame.init()
 
# printing the number of modules initialized successfully
print('Number of modules initialized successfully:', numpass)

#region setup
# resolution of the window
screenWidth = 1280
screenHeight = 720 
pygame.display.set_mode((screenWidth, screenHeight))

# Initializing RGB Color
bgColor = (0, 0, 0)

# Creating a reference to the surface
surface = pygame.display.get_surface()

# set title in the title bar
title = 'Game Test'
pygame.display.set_caption(title)

# set a reference to the clock speed
clock = pygame.time.Clock()
cSpeed = 60  # limit the FPS

#endregion

# player shape
player = pygame.Rect(150, 150, 50, 50)

def Draw():
    # Changing surface color
    surface.fill(bgColor)  # setting acolor for the background
    pygame.draw.rect(surface, (255, 0, 0), player)
    
# creating a bool value which checks allows the game to run
running = True
  
# keep game running till running is true (run the game loop while true)
while running: 
    
    # Check for event if user has pushed any event in queue 
    for event in pygame.event.get(): 
          
        # if event is of type quit then set running bool to false 
        if event.type == pygame.QUIT: 
            running = False
        
        # Handle keyboard inputs for movement - event driven
        """ 
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, event.key == pygame.K_w):
                player.y -= 5
            elif event.key in (pygame.K_DOWN, event.key == pygame.K_s):
                player.y += 5
            if event.key in (pygame.K_LEFT, event.key == pygame.K_a):
                player.x -= 5
            elif event.key in (pygame.K_RIGHT, event.key == pygame.K_d):
                player.x += 5 """
        
        # store all keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.y -= 5
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.y += 5
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.x -= 5
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.x += 5

    Draw()
    pygame.display.update()  # update the display    
    clock.tick(cSpeed) # sets the FPS
    