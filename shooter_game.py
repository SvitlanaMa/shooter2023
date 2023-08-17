#Створи власний Шутер!
import pygame
from random import randint

pygame.init()

FPS = 60
window = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (700, 500))

fire_snd = pygame.mixer.Sound("fire.ogg")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.transform.scale(image, (w, h))
        self.speed = speed
    def paint(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

hart_img = pygame.image.load("hart.jpg")

class Player(GameSprite): 
    def __init__(self, x, y, w, h, image, speed, hp):
        super().__init__(x, y, w, h, image, speed)
        self.hp = hp
        harts = []
        x = 650
        for i in range(self.hp):
            h = GameSprite(x, 0, 20, 20,hart_img,0)
            harts.append(h)
            x -= 25
        self.harts = harts


    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed
        if k[pygame.K_d]:
            if self.rect.right <= 700:
                self.rect.x += self.speed
    
    def spawn_bullet(self):
        bullet = Bullet(self.rect.centerx - 10, self.rect.y, 20, 30, bullet_img, 8)
        # fire_snd.play()
    

enemies_group = pygame.sprite.Group()
lost = 0

class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        enemies_group.add(self)
        self.x_speed = randint(-1, 1)
        self.x_wait = randint(20, 50) 

    def start(self):
        self.rect.y = 0
        self.rect.x = randint(0, 700 - self.rect.w)

    def update(self):
        global lost
        self.rect.y += self.speed
        self.rect.x += self.x_speed
        if self.x_wait <= 0 or self.rect.x <=0 or self.rect.right >= 700:
            self.x_speed *= -1
            self.x_wait = randint(20, 50)
        else:
            self.x_wait -= 1
        if self.rect.y >= 500:
            enemies_group.remove(self)
            lost += 1

bullets_group = pygame.sprite.Group()

class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        bullets_group.add(self)
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullet_img = pygame.image.load("bullet.png")

player_img = pygame.image.load("rocket.png")
player1 = Player(320, 420, 50, 50, player_img, 3, 5)

enemy_img = pygame.image.load("ufo.png")

enemy_wait = 50
score = 0
while True:
    try:
        with open("record.txt", "r+") as file:
            max_score = 0
            try:        
                data = file.read()
                max_score = int(data)
            except:
                print("Щось не так")
        print(max_score)
        break
    except FileNotFoundError:
        file = open("record.txt", "x")
        file.close()


font = pygame.font.Font("font1.ttf", 30)

game = True
finish = False

while game:

    if not finish:
        lost_lb = font.render("Lost: "+str(lost), True, (255, 255, 255))
        kill_lb = font.render("Kill: "+str(score), True, (255, 255, 255))

        if enemy_wait == 0:
            enemy = Enemy(randint(0, 650), 0, 50, 40, enemy_img, randint(1, 3))
            enemy_wait = randint(70, 140)
        else:
            enemy_wait -= 1

        window.blit(background, (0, 0))
        window.blit(lost_lb, (0,0))
        window.blit(kill_lb, (0,50))
        for h in player1.harts:
            h.paint()
        player1.paint()
        player1.move()

        bullets_group.draw(window)
        bullets_group.update()

        enemies_group.draw(window)
        enemies_group.update()
        
        if pygame.sprite.groupcollide(enemies_group, bullets_group, True, True):
            score += 1
            # print(score)

        if pygame.sprite.spritecollide(player1, enemies_group, True):
            player1.hp -= 1
            print(player1.hp)
        
        if player1.hp <=0 or lost >= 3:
            if score > max_score:
                max_score = score
                with open("record.txt", "w") as file:
                    file.write(str(score))

            finish = True
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN and not finish:
            player1.spawn_bullet()

    clock.tick(FPS)
    pygame.display.update()