import pygame as pg
import random


white = (255,255,255)
green = (0, 200, 0)
screen_w = 1000
screen_h = 1000

class Boulder(pg.sprite.Sprite):
    def __init__(self):
        super(Boulder, self).__init__()
        x = random.randint(100, 900)
        self.surf = pg.Surface((200,200))
        self.surf.fill(green)
        self.rect = self.surf.get_rect(midbottom=(x, 0))

    def update(self):
        self.rect.move_ip(0, +7)
        if self.rect.top > 1000:
            self.kill()

boulders = pg.sprite.Group()
all_sprites = pg.sprite.Group()

pg.init() 
game_active = True

screen = pg.display.set_mode((screen_w, screen_h))
bg = pg.Surface((screen_w, screen_h))
bg.fill(white)
pg.display.set_caption("Pygameforever")         #Game title
clock = pg.time.Clock()                         #How fast we want to run our game (fps/hz/pps)


ADDBOULDER = pg.USEREVENT +1
pg.time.set_timer(ADDBOULDER, 3000)


while True:                                     #Infinite loop
    for events in pg.event.get():               #Our event-loop
        if events.type == pg.QUIT:
            pg.quit()
            exit()
        if events.type == ADDBOULDER:
            new_boulder = Boulder()
            boulders.add(new_boulder)
            all_sprites.add(new_boulder)
    

    screen.blit(bg, (0, 0))
    boulders.update()
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    if game_active:                             #What to do when game is active
        print("Game is active")
    else:                                       #What to do when game is not active, aka gameover?
        print("Game is not active. Gameover?")

  
    
    pg.display.update()                         
    clock.tick(60)    