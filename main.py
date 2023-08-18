#Підключення біблеотеки
from pygame import *
#Ініліцілізація звуків і обєктів
init()
mixer.init()
#Розміри вікна
w = 1000
h = 700

#Создавання вікна
window = display.set_mode((w, h))
display.set_caption("Labyrinth")
display.set_icon(image.load("diamong.png"))
#Задній фон
back = transform.scale(image.load('back.jpg'), (w, h))
#Таймер
clock = time.Clock()
#Підключення звука
mixer.music.load("fon_musics.ogg")
mixer.music.play()
mixer.music.set_volume(1)
#Звуки
kick = mixer.Sound("kick.ogg")
money = mixer.Sound("money.ogg")
walls_sound = mixer.Sound("wall_rect.ogg")
win = mixer.Sound("finish.ogg")
#Клас для спрайтів
class GameSprite(sprite.Sprite):
    #Конструктор
    def __init__(self, player_img, player_x, player_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_img), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed
    #Відмальовування обєкта
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    #Зміна картинки
    def image_swipe(self):
        self.image = transform.scale(image.load("fake_block_part_2.png"), (100, 100))


#Класс для ігрока
class Player(GameSprite):
    def update(self): #Функція для обробки руху
        keys_pressed = key.get_pressed()

        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys_pressed[K_s] and self.rect.y < h - 65:
            self.rect.y += self.speed

        if keys_pressed[K_a] and self.rect.x > 0:
            self.image = transform.scale(image.load("hero_L.png"), (100, 100))
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < w - 65:
            self.rect.x += self.speed
            self.image = transform.scale(image.load("hero_R.png"), (100, 100))
#Класс для ворога
class Enemy(GameSprite):
    direction = "right"
    def update(self, start, end): #Функція для обробки руху
        if self.rect.x >= end:
            self.direction = "left"

        if self.rect.x <= start:
            self.direction = "right"

        if self.direction == "left":
            self.image = transform.scale(image.load("enemy_L.png"), (125, 125))
            self.rect.x -= self.speed

        if self.direction == "right":
            self.image = transform.scale(image.load("enemy_R.png"), (125, 125))
            self.rect.x += self.speed

#Класс для стін
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_w, wall_h, wall_x, wall_y):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_w
        self.height = wall_h
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color_1, self.color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Спрайти
hero = Player("hero_R.png", 50, 550, 4) # Гравець
enemy = Enemy("enemy_R.png", 530, 450, 6) # Ворог
enemy_1 = Enemy("enemy_R.png", 200, 200, 5) # Ворог
gold = GameSprite("diamong.png", 250, 500, 0) #Добича
fake_gold = GameSprite("fake_finish.png", 790, 150, 0) # Фейк
fake_gold_2 = GameSprite("fake_finish.png", 230, 330, 0) # Фейк

#Стіни
walls_1 = Wall(0, 0, 0, 20, 600, 200, 100)
walls_2 = Wall(0, 0, 0, 250, 20, 200, 100)
walls_3 = Wall(0, 0, 0, 300, 20, 600, 100)
walls_4 = Wall(0, 0, 0, 20, 100, 450, 100)
walls_5 = Wall(0, 0, 0, 20, 100, 450, 350)
walls_6 = Wall(0, 0, 0, 250, 20, 200, 430)
walls_7 = Wall(0, 0, 0, 20, 300, 900, 100)
walls_8 = Wall(0, 0, 0, 20, 100, 600, 100)
walls_9 = Wall(0, 0, 0, 20, 100, 600, 350)
walls_10 = Wall(0, 0, 0, 160, 20, 600, 180)
walls_11 = Wall(0, 0, 0, 160, 20, 600, 350)
walls_12 = Wall(0, 0, 0, 20, 190, 760, 180)
walls_13 = Wall(0, 0, 0, 20, 190, 450, 400)
walls_14 = Wall(0, 0, 0, 500, 20, 400, 580)
walls_15 = Wall(0, 0, 0, 100, 20, 100, 100)
walls_16 = Wall(0, 0, 0, 80, 20, 0, 300)
walls_17 = Wall(0, 0, 0, 100, 20, 100, 500)


#Змінна для гри
game = True
#Ігровий цикл
while game:
    #Для закриття вікна
    for e in event.get():
        if e.type == QUIT:
            game = False
    #Відмальвування обєктів
    window.blit(back, (0, 0))
    gold.reset()

    fake_gold.reset()
    fake_gold_2.reset()

    enemy.reset()
    enemy.update(500, 870)

    enemy_1.reset()
    enemy_1.update(200, 630)


    hero.reset()
    hero.update()

    walls_1.reset()
    walls_2.reset()
    walls_3.reset()
    walls_4.reset()
    walls_5.reset()
    walls_6.reset()
    walls_7.reset()
    walls_8.reset()
    walls_9.reset()
    walls_10.reset()
    walls_11.reset()
    walls_12.reset()
    walls_13.reset()
    walls_14.reset()
    walls_15.reset()
    walls_16.reset()
    walls_17.reset()

    #Перевірка зіткнень
    if sprite.collide_rect(hero, enemy) or sprite.collide_rect(hero, enemy_1): # Ворога
        hero.rect.x = 50
        hero.rect.y = 550

    #Стін
    if sprite.collide_rect(hero, walls_1) or sprite.collide_rect(hero, walls_2) or sprite.collide_rect(hero, walls_3) or sprite.collide_rect(hero, walls_4) or sprite.collide_rect(hero, walls_5) or sprite.collide_rect(hero, walls_6) or sprite.collide_rect(hero, walls_7) or sprite.collide_rect(hero, walls_8) or sprite.collide_rect(hero, walls_9) or sprite.collide_rect(hero, walls_10) or sprite.collide_rect(hero, walls_11) or sprite.collide_rect(hero, walls_12) or sprite.collide_rect(hero, walls_13) or sprite.collide_rect(hero, walls_14) or sprite.collide_rect(hero, walls_15) or sprite.collide_rect(hero, walls_16) or sprite.collide_rect(hero, walls_17):
        walls_sound.play()
        hero.rect.x = 50
        hero.rect.y = 550
    #Фейка
    if sprite.collide_rect(hero, fake_gold):
        fake_gold.image_swipe()
        hero.rect.x = 50
        hero.rect.y = 550
    #Фейка
    if sprite.collide_rect(hero, fake_gold_2):
        fake_gold_2.image_swipe()
        hero.rect.x = 50
        hero.rect.y = 550
    #Виграшу
    if sprite.collide_rect(hero, gold):
        win.play()
        game = False
        
    #ФПС і оновлення екрану
    display.update()
    clock.tick(60)