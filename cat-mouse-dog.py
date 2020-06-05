import pygame
import random
from pygame.locals import (RLEACCEL, K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,KEYDOWN,QUIT,K_PAUSE)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Define Colors - RGB
black = (0,0,0)
white = (255,255,255)
green = (34,177,76)
red = (255,0,0)

# Initialize pygame
pygame.init()

#set width and height
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

#name the game window 
pygame.display.set_caption("Catch the mouse and avoid the dogs!")

# set clock for framerate
clock = pygame.time.Clock()

# Set positions of graphics
background_position = [0, 0]

#background image
background_image = pygame.image.load("E:/AWS/Python/game3/background.png").convert()

#score display
score = 0

#set the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("E:/AWS/Python/game3/cat2.png").convert()
        self.surf.set_colorkey((white), RLEACCEL)
        self.rect = self.surf.get_rect()

    #set movement control + sounds
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            #move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            #move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_ESCAPE] :
            exit_sound.play()
    #keep player in screen on green field
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 125:
            self.rect.top = 125
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
#define dog class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("E:/AWS/Python/game3/dog.PNG").convert()
        self.surf.set_colorkey((white), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(170, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(3, 7)
    # move enemy based on speed, but remove it when it passes the left edge of the screen.
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#define mouse class (power up)
class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super(Mouse, self).__init__()
        self.surf = pygame.image.load("E:/AWS/Python/game3/mouse.png").convert()
        self.surf.set_colorkey((white), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(170, SCREEN_HEIGHT),
            )
        )
    # Move the mouse based on a constant speed, but remove it when it passes the left edge of the screen.
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        #if pygame.sprite.spritecollideany(player, mouse):
        #    score +=1
        if pygame.sprite.spritecollideany(player, mouse):
            global score
            score += 1
            self.kill()

# Setup for sounds
pygame.mixer.init()


# Create custom events for adding a new dog and mouse
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 420)
ADDMOUSE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDMOUSE, 450)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, mouse sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for collision detection - score up and position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
mouse = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Load and play our background music
# Sound source: http://www.orangefreesounds.com/analog-dream-electronic-downtempo-music/
pygame.mixer.music.load("E:/AWS/Python/game3/background_music.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
#cat meow : http://www.orangefreesounds.com/cat-meow-short/
#move_up_sound = pygame.mixer.Sound("E:/AWS/Python/game3/Cat-meow-short.ogg")
#move_down_sound = pygame.mixer.Sound("E:/AWS/Python/game3/Cat-meow-short.ogg")
#dog bark sound: http://soundbible.com/70-Dog-Barking.html
collision_sound = pygame.mixer.Sound("E:/AWS/Python/game3/dog.ogg")
#game end sound: http://soundbible.com/1687-TomCat.html
exit_sound = pygame.mixer.Sound("E:/AWS/Python/game3/catEnd.ogg")
#purr: http://soundbible.com/1002-Purring.html
happy_sound = pygame.mixer.Sound("E:/AWS/Python/game3/purr.ogg")

# Set the base volume for all sounds
#move_up_sound.set_volume(0.01)
#move_down_sound.set_volume(0.01)
collision_sound.set_volume(3)
happy_sound.set_volume(3)
exit_sound.set_volume(5)

def redrawGameWindow():
    screen.blit(background_image, (0,0))
    font = pygame.font.SysFont("helvetica", 30, True)
    text = font.render("Score: " + str(score), 1, (black))
    screen.blit(text, (610, 10))
    
    pygame.display.update()

# Variable to keep our main loop running
running = True

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new mouse?
        elif event.type == ADDMOUSE:
            # Create the new MOUSE, and add it to our sprite groups
            new_mouse = Mouse()
            mouse.add(new_mouse)
            all_sprites.add(new_mouse)
    
    
    # Refresh background and score:
    redrawGameWindow()

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies and mouse
    enemies.update()
    mouse.update()

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, play collision music and remove the player
        pygame.mixer.music.stop()
        collision_sound.play()
        player.kill()
        exit_sound.play()
        # Stop the loop
        running = False

    elif pygame.sprite.spritecollideany(player, mouse):
        # If so, play happy purr:
        happy_sound.play()

        #Continue the loop
        running = True   

    # Flip everything to the display
    pygame.display.flip()

    # 60 frames per second rate
    clock.tick(60)


# Stop and quit the mixer
#exit_sound.play(5)
pygame.mixer.music.stop()
pygame.mixer.quit()
