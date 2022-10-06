import pygame as pg
import os.path
import random
pg.init()
from pygame import mixer
game_active = True
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
anim = 3
ALPHA =(0, 0, 0)
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))       #Screen size, should this be changed? 
pg.display.set_caption("Pygameforever")         #Game title
clock = pg.time.Clock()                         #How fast we want to run our game (fps/hz/pps)
bg = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg.fill((255,255,255))

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'Graphics', file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pg.get_error()))
    return surface

#Background Sound

mixer.init()
mixer.music.load(f"{main_dir}/Graphics/WoodlandFantasy.wav")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Object class Player


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        self.sprites.append(load_image('player1.png').convert_alpha())
        self.sprites.append(load_image('player2.png').convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.start_x = SCREEN_WIDTH//2
        self.start_y = SCREEN_HEIGHT-110
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.frame = 0
        self.animation = False

    def animate(self, trueorfalse):
        self.animation = trueorfalse
    def update(self):
        if self.animation == True:
            self.current_sprite += 0.05

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

    def moveRight(self, pixels):
        if self.rect.right > SCREEN_WIDTH+20:
            pixels = 0
        else:
            self.rect.x += pixels


    def moveLeft(self, pixels):
        if self.rect.left < 0:
            pixels = 0
        else:    
            self.rect.x -= pixels

    def moveForward(self, pixels):    
        self.rect.y -= pixels

    def moveBack(self, pixels):
        if self.rect.bottom > SCREEN_HEIGHT+20:
            pixels = 0
        else:
            self.rect.y += pixels
        

# Speed of Player Character
speed = 5

class Boulder(pg.sprite.Sprite):
    def __init__(self):
        super(Boulder, self).__init__()
        x = random.randint(100, 900)
        self.image = load_image('gif.gif3.gif').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, 0))

    def update(self):
        self.rect.move_ip(0, +7)
        if self.rect.top > 1000:
            self.kill()



# A stationary enemy, that kills on contact. For holes and water etc.

class Hole(pg.sprite.Sprite):
    def __init__(self, width, height, posx, posy):
        super(Hole, self).__init__()
        
        self.image = pg.Surface((width,height))
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(center=(posx, posy))

boulders = pg.sprite.Group()
ADDBOULDER = pg.USEREVENT +1
pg.time.set_timer(ADDBOULDER, 3000)


holes = pg.sprite.Group()
boulders = pg.sprite.Group()
all_sprites_list = pg.sprite.Group()
playerCar = Player()
# Water-hole
hole1 = Hole(300, 20, 420, 360)
hole2 = Hole(20, 200, 270, 200)
hole3 = Hole(20, 200, 560, 200)
hole8 = Hole(400, 20, 450, 100)
# Dirt-hole
hole4 = Hole(70, 20, 460, 635)
hole5 = Hole(20, 70, 635, 550)
hole6 = Hole(70, 20, 600, 490)
hole7 = Hole(10, 70, 430, 600)
holes.add(hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8)

# Variables and list for shrink
liten = pg.transform.scale(playerCar.image, (75, 75))
mindre = pg.transform.scale(playerCar.image, (50, 50))
minst = pg.transform.scale(playerCar.image, (25, 25))
shrink = [liten, mindre, minst]


all_sprites_list.add(playerCar)
all_sprites_list.add(hole1, hole2, hole3, hole4, hole5, hole6, hole7, hole8)
#Load Images
map_surface = load_image('preview.png')
map_surface = pg.transform.scale(map_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

maps_cleared = 0

while True:                                     #Infinite loop
    for events in pg.event.get():               #Our event-loop
        if events.type == pg.QUIT:
            pg.quit()
            exit()
        if events.type == ADDBOULDER:
            new_boulder = Boulder()
            boulders.add(new_boulder)
            all_sprites_list.add(new_boulder)


    if game_active:                             #What to do when game is active
        boulders.update()
        for entity in all_sprites_list:
            screen.blit(entity.image, entity.rect)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            playerCar.animate(True)
            playerCar.moveLeft(speed)
        if keys[pg.K_RIGHT]:
            playerCar.animate(True)
            playerCar.moveRight(speed)
        if keys[pg.K_DOWN]:
            playerCar.animate(True)
            playerCar.moveBack(speed)
        if keys[pg.K_UP]:
            playerCar.animate(True)
            playerCar.moveForward(speed)

        if pg.sprite.spritecollideany(playerCar, boulders):
            # If so, then remove the player and quit the game
            playerCar.kill()
            pg.quit()
            exit()
        if pg.sprite.spritecollideany(playerCar, holes):
            # If so, then remove the player and quit the game
            for i in shrink:
                screen.blit(map_surface, (0,0))
                screen.blit(i, (playerCar.rect))  
                pg.display.update()
                pg.time.wait(300)

            playerCar.kill()
            pg.quit()
            exit()
        if playerCar.rect.bottom < 0:
            # If player clears the course
            print("Du har nu klarat bana1")
            maps_cleared += 1
            game_active = False




    else:                                       #What to do when game is not active, aka gameover?
        if maps_cleared == 1:
            print("Starting next map")
        else:
            print("Gameover?")
    
    holes.update()
    playerCar.update()                          # PLayer update /JL
    screen.blit(map_surface, (0,0))
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    pg.display.update()                         
    clock.tick(60)                              #Updates disp 60 times per sec
