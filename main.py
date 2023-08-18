#Підключення біблеотек
from pygame import *
from random import randint
import time as t
#Ініціалізація всіх процесів
init()
#Розміри екрану
w = 700
h = 800
#Создавання вікна
window = display.set_mode((w, h))
display.set_caption("Shooter")
display.set_icon(image.load("icoc.png"))
#Фон вікна
back = transform.scale(image.load("back.png"), (w, h))
#Змінні
lost = 0
killed = 0  
live = 5  

speed_enemy = 6

# clock = time.Clock()

"""SOUND"""
#Ініціалізація музики
mixer.init()
#Фонова музика
mixer.music.load("space.ogg")
mixer.music.set_volume(0.3)
#Музика стрельби
fire = mixer.Sound("fire.ogg")

"""FONTS"""

#Ініціалізація шрифту
font.init()
#Шрифти
font1 = font.SysFont("Arial", 50)
font_int = font.SysFont("Almaz Medium", 100, bold = True)

"""CLASSES"""

#Клас для спрайтов 
class GameSprite(sprite.Sprite):
    #Конструктор
    def __init__(self, player_img, player_x, player_y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_img), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed
    #Відмальовування обєкта
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#Клас для гравця
class Player(GameSprite):
    #Функція для рухів
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < w - 100:
            self.rect.x += self.speed

    #Функція для создавання пулі та додавання до группи
    def fire(self):
        bullet = Bullet("goroh.png", self.rect.centerx, self.rect.top, 10, 10, 10)
        bullets.add(bullet)

#Клас для ворога
class Enemy(GameSprite):
    def update(self):
        global lost

        self.rect.y += self.speed

        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(0, w - 100)
            lost += 1

class Asteroid(Enemy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(0, w - 100)

#Клас для пулі
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()


#Группи спрайтів
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
#Создавання спрайтів 5 разів та додавання до группи
for i in range(5):
    monster = Enemy("enemy.png", randint(0, w - 100), -50, 80, 0, speed_enemy)
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid("asteroid.png", randint(0, w - 100), randint(-1000, 0), 80, 0, 5)
    asteroid.add(asteroids)

#Гравець
player = Player("player.png", w/2, h-100, 80, 650, 20)

#Змінна для циклу
finish = False
game = True
num_fire = 0
rel_time = False
#Ігровий цикл
while game:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 10 and rel_time is False:
                    num_fire += 1
                    player.fire()
                    fire.play()
                if num_fire > 10 and rel_time is False:
                    rel_time = True
                    last_time = t.time()
    if not finish: #Перевірка на закінчення ГРИ а не програми

        window.blit(back, (0, 0))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()
        
        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        if rel_time: #Перевірка чи йде перезарядка
            new_time = t.time()
            if new_time - last_time < 3:    
                reload_txt = font1.render("RELOADING...", True, (255, 0, 0))
                window.blit(reload_txt, (w/2 - 100, h/2))
            else:
                rel_time = False
                num_fire = 0

        #Тексти
        lost_txt = font1.render("Пропустив: " + str(lost), 1, (0, 0, 0))
        killed_txt = font1.render("Збито: " + str(killed), 1, (0, 0, 0))
        live_txt_1 = font_int.render(str(live), 1, (27, 150, 1))
        live_txt_2 = font_int.render(str(live), 1, (0, 255, 0))
        live_txt_3 = font_int.render(str(live), 1, (242, 255, 0))
        live_txt_4 = font_int.render(str(live), 1, (255, 153, 0))
        live_txt_5 = font_int.render(str(live), 1, (255, 0, 0))

        #Відмальовування
        window.blit(lost_txt, (10, 10))
        window.blit(killed_txt, (10, 55))
        window.blit(live_txt_1, (650, 10))

        if sprite.spritecollide(player, monsters, True): #Перевірка зіткнень гравця та групи монстрів
            live -= 1
            monster = Enemy("enemy.png", randint(0, w - 100), -50, 80, 0, speed_enemy)
            monsters.add(monster)
        
        if sprite.spritecollide(player, asteroids, True): #Перевірка зіткнень гравця та групи астероідів
            live -= 1
            asteroid = Asteroid("asteroid.png", randint(0, w - 100), randint(-1000, 0), 80, 0, 5)
            asteroid.add(asteroids)

        collides_ast = sprite.groupcollide(asteroids, bullets, False, True)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for col in collides: #Перебираємо церез цикл
            monster = Enemy("enemy.png", randint(0, w - 100), -50, 80, 0, speed_enemy)
            monsters.add(monster)
            killed += 1

        if killed >= 255:#Перевірка виграшу
            win = font1.render("Ти защитився", True, (0, 255, 0)) 
            window.blit(win, (w/2 - 100, h/2))
            finish = True

        if live <= 0 or lost >= 5:# Перевірка Програшу
            lost_1 = font1.render("У тебе нема мозгів", True, (255, 0, 0)) 
            window.blit(lost_1, (w/2 - 100, h/2))
            finish = True

        #Зміна колорів життя
        if live == 4:
            window.blit(live_txt_2, (650, 10))
        if live == 3:
            window.blit(live_txt_3, (650, 10))
        if live == 2:
            window.blit(live_txt_4, (650, 10))
        if live == 1 or live == 0:
            window.blit(live_txt_5, (650, 10))
    
    #Перезагрузка 
    else:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_r]:
            live = 5 
            killed = 0
            lost = 0

            for m in monsters:
                m.kill()

            for b in bullets:
                b.kill()

            for i in range(5):
                monster = Enemy("enemy.png", randint(0, w - 100), -50, 80, 0, speed_enemy)
                monsters.add(monster)

            finish = False

    #Оновлення екрану
    display.update()
        