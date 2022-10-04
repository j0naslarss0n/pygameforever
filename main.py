import pygame as pg
import os.path
import random
pg.init() 
game_active = True
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))       #Screen size, should this be changed? 
pg.display.set_caption("Pygameforever")         #Game title
clock = pg.time.Clock()                         #How fast we want to run our game (fps/hz/pps)

main_dir = os.path.split(os.path.abspath(__file__))[0]

# Color variables
green = (0, 200, 0)
# Object class Player
class Sprite(pg.sprite.Sprite):
	def __init__(self, color, height, width):
		super().__init__()

		self.image = pg.Surface([width, height])
		self.image.fill((255,0,0))
		self.image.set_colorkey((0,255,0))

		pg.draw.rect(self.image,color,pg.Rect(0, 0, width, height))

		self.rect = self.image.get_rect()

	def moveRight(self, pixels):
		self.rect.x += pixels

	def moveLeft(self, pixels):
		self.rect.x -= pixels

	def moveForward(self, speed):
		self.rect.y += speed * speed/10

	def moveBack(self, speed):
		self.rect.y -= speed * speed/10

# Enemy-object class boulder
class Boulder(pg.sprite.Sprite):
    def __init__(self):
        super(Boulder, self).__init__()
        
        x = random.randint(50, 950)
        self.image = pg.Surface((100,100))
        self.image.fill(green)
        self.rect = self.image.get_rect(midbottom=(x, 0))

    def update(self):
        self.rect.move_ip(0, +7)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

boulders = pg.sprite.Group()
all_sprites_list = pg.sprite.Group()
playerCar = Sprite((255,0,0), 20, 30)
playerCar.rect.x = 200
playerCar.rect.y = 300


all_sprites_list.add(playerCar)

#Load Images
map_surface = pg.image.load(main_dir+'/Assets/Graphics/preview.png')
map_surface = pg.transform.scale(map_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Custom events
#boulder time event
ADDBOULDER = pg.USEREVENT +1
pg.time.set_timer(ADDBOULDER, 3000)

#Infinite loop
#Our event-loop
while True:                                     
    for events in pg.event.get():               
        if events.type == pg.QUIT:
            pg.quit()
            exit()

        if events.type == ADDBOULDER:
            new_boulder = Boulder()
            boulders.add(new_boulder)
            all_sprites_list.add(new_boulder)
    
    #What to do when game is active                           
    if game_active: 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            playerCar.moveLeft(10)
        if keys[pg.K_RIGHT]:
            playerCar.moveRight(10)
        if keys[pg.K_DOWN]:
            playerCar.moveForward(10)
        if keys[pg.K_UP]:
            playerCar.moveBack(10)

    if pg.sprite.spritecollideany(playerCar, boulders):
        # If so, then remove the player and quit the game
        playerCar.kill()
        pg.quit()
        exit()

    #What to do when game is not active, aka gameover?
    else:                                     
        print("Game is not active. Gameover?")
    boulders.update()
    screen.blit(map_surface, (0,0))
    
    # Puting all items on the screen
    for entity in all_sprites_list:
        screen.blit(entity.image, entity.rect)
   
    
    pg.display.update()                         
    clock.tick(60)                              #Updates disp 60 times per sec
