import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
pygame.mixer.init()

# Set the width and height of the screen [width, height]
size = (900, 600)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Protect Yourself")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
font_name = pygame.font.match_font('arial')

# set up counting
score = 0

width = 900
height = 600
fps = 60

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)  
        
def show_start_screen():
        screen.fill(BLACK)
        draw_text(screen, "Let's Play:", 64, width / 2, height / 4)
        draw_text(screen, "Arrow keys move, space to fire while avoiding other aliens", 22,
                  width / 2, height / 2)
        draw_text(screen, "Press a key to begin", 18, width / 2, height * 3 / 4)
        pygame.display.flip()
                    
def show_go_screen():
        screen.fill(BLACK)
        draw_text(screen, "Let's Play", 64, width / 2, height / 4)
        draw_text(screen, "Score:" +str(score), 22, width / 2, height / 2)
        draw_text(screen, "Press a key to begin", 18, width / 2, height * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super(Alien, self).__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.radius = 45
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.shield = 300
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.rect.x = 100
        self.rect.y = 100
        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count == 0:
            # No joysticks!
            print("Error, I didn't find any joysticks.")
        else:
            # Use joystick #0 and initialize it
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()
 
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
            
                if self.joystick_count != 0:
 
            # This gets the position of the axis on the game controller
            # It returns a number between -1.0 and +1.0
            horiz_axis_pos = self.my_joystick.get_axis(0)
            vert_axis_pos = self.my_joystick.get_axis(1)
 
            # Move x according to the axis. We multiply by 10 to speed up the
            # movement.
            self.rect.x = self.rect.x+horiz_axis_pos*10
            self.rect.y = self.rect.y+vert_axis_pos*10
            
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-1, 1 )
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        #should spawn directly in front of the alien
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.bottom < 0:
            self.kill()    

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 10
    fill = (pct / 300) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
# Graphics
player_image = pygame.image.load('alien.png').convert()
player_image.set_colorkey(BLACK)
background_image = pygame.image.load('spacebg.jpg').convert()
background_position = [0,0]

# Sound
shoot_sound = pygame.mixer.Sound('spacelaser.wav')
explosion = pygame.mixer.Sound('explosion.wav')
# Enemies
enemy_image = pygame.image.load('enemy2.png').convert()
 
# Add    
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
alien = Alien()
all_sprites.add(alien)
    

# For loop for enemy spawn
for i in range(10):
    newmob()
#background music
pygame.mixer.music.load('battleThemeA.mp3')
pygame.mixer.music.play()
 
# -------- Main Program Loop -----------
# Loop until the user clicks the close button.
done = True
finished = True

while done:
    if finished:
        show_go_screen()
        finished = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        alien = Alien()
        all_sprites.add(alien)
        for i in range(10):
            newmob()
        score = 0
    clock.tick(fps)
    # --- Main event loop
        # Set the speed based on the key pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            finished = False
            done = False
       
    # --- Game logic should go here
    all_sprites.update()
    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 100 - hit.radius
        explosion.play()
        newmob()
    
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(alien, mobs, True)
    for hit in hits:
        alien.shield -= hit.radius * 2
        if alien.shield <= 0:
            finished = True

    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
 
    # --- Drawing code should go here
    screen.blit(background_image, background_position)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, width / 2, 10)
    draw_text(screen, str(score), 18, width / 2, 10)
    draw_shield_bar(screen, 5, 5, alien.shield)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.update()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
del font
# Close the window and quit.
pygame.quit()