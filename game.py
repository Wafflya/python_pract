import pygame
import random
import os

WIDTH = 700
HEIGHT = 900
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

POWERUP_TIME = 5000


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "DICK IN THE SPACE", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / player.base_hp) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > player.base_hp * (2 / 3):
        pygame.draw.rect(surf, GREEN, fill_rect)
    elif player.base_hp // 3 < pct <= player.base_hp * (2 / 3):
        pygame.draw.rect(surf, YELLOW, fill_rect)
    else:
        pygame.draw.rect(surf, RED, fill_rect)

    pygame.draw.rect(surf, WHITE, outline_rect, 2)


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def newmob(difficulty=0):
    m = Mob()
    # m.speedx += difficulty
    m.speedy += difficulty
    all_sprites.add(m)
    mobs.add(m)


def new_explosion(x, y, size):
    ex = Explosion(x, y, size)
    all_sprites.add(ex)


def new_damage(x, y):
    dmg = ShipDamage(x, y)
    all_sprites.add(dmg)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.speed_chng_start = 2
        self.speed_chng = self.speed_chng_start
        self.lives = 3
        self.hidden = False
        # Бонусная скорость
        self.hide_timer = pygame.time.get_ticks()
        self.bonus_speed = 0
        self.bonus_speed_time_start = 0
        self.bonus_speed_flag = False
        self.bonus_speed_time = 10000
        #
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        #
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.base_hp = 100
        self.current_hp = self.base_hp
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 60))
        self.rect = self.image.get_rect()
        self.radius = 25
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.radius = 25
        self.image.set_colorkey(BLACK)

    def to_base(self):
        self.bonus_speed = 0
        self.power = 1
        self.shoot_delay = 250
        self.current_hp = self.base_hp


    def gunup(self, poww):
        if self.power + poww <= 3:
            self.power += poww
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.power >= 3 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            draw_text(screen, "You're lost a 1 live", 25, WIDTH // 2, HEIGHT // 2)
            self.hidden = False
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 10

        if self.bonus_speed_flag == True:
            self.speed_chng = self.speed_chng_start + self.bonus_speed
        now = pygame.time.get_ticks()
        if now - self.bonus_speed_time_start > self.bonus_speed_time:
            self.bonus_speed_flag = False
            self.bonus_speed = 0
            self.speed_chng = self.speed_chng_start

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -self.speed_chng
        if keystate[pygame.K_RIGHT]:
            self.speedx = self.speed_chng
        if keystate[pygame.K_UP]:
            self.speedy = -self.speed_chng
        if keystate[pygame.K_DOWN]:
            self.speedy = self.speed_chng
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT and self.hidden == False:
            self.rect.bottom = HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                player_bullets.add(bullet)
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                player_bullets.add(bullet1)
                player_bullets.add(bullet2)
            if self.power == 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                player_bullets.add(bullet1)
                player_bullets.add(bullet2)
                player_bullets.add(bullet3)


    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH // 2, HEIGHT + 300)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        # вращение спрайтов


# Корабль получает урон
class ShipDamage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship_damage[2]
        self.image.set_colorkey(BLACK)
        self.delay = 150
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.start_time > self.delay:
            self.kill()


# Спрайты взрывов
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.delay = 50
        self.frame = 0
        self.size = size
        self.image = explosion_anim[size][0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_frame = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_frame > self.delay and self.frame < 8:
            self.last_frame = now
            self.frame += 1
            self.image = explosion_anim[self.size][self.frame]
        elif self.frame >= 8:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['hp', 'speedup', 'gunup'])
        our_pow = random.choice(power_up_img[self.type])
        self.lvl = our_pow[1]
        self.image = our_pow[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()




class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img_player, (2, 20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        shoot_sound.play()

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_dir = os.path.join(game_folder, 'sounds')

#Загрузка музычки
shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pew.ogg'))
expl_sounds = ['exp1.mp3', 'exp2.mp3', 'exp3.mp3']



# Загрузка картиночек
# Загрузка взрывов
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

    # Загрузка попаданий по игроку
ship_damage = []
damage_anim_list = ['playerShip1_damage1.png', 'playerShip1_damage2.png', 'playerShip1_damage3.png']
for i in damage_anim_list:
    img = pygame.image.load(os.path.join(img_folder, i)).convert()
    ship_damage.append(pygame.transform.scale(img, (60, 60)))
    # Загрузка улучшений/модификаторов
power_up_img = {}
power_up_img['hp'] = []
power_up_img['speedup'] = []
power_up_img['gunup'] = []
gunup_lst = ['things_silver.png', 'things_gold.png']
pills_lst = ['pill_blue.png', 'pill_green.png', 'pill_red.png', 'pill_yellow.png']
speed_lst = ['bolt_bronze.png', 'bold_silver.png', 'bolt_gold.png']
#shield_lst = ['shield_bronze.png', 'shield_silver.png', 'shield_gold.png']
for i, j in enumerate(pills_lst):
    img = pygame.image.load(os.path.join(img_folder, j)).convert()
    power_up_img['hp'].append((img, i))

#for i, j in enumerate(pills_lst):
 #   img = pygame.image.load(os.path.join(img_folder, j)).convert()
  #  power_up_img['shield'].append((img, i))

for i, j in enumerate(gunup_lst):
    img = pygame.image.load(os.path.join(img_folder, j)).convert()
    power_up_img['gunup'].append((img, i))

for i, j in enumerate(speed_lst):
    img = pygame.image.load(os.path.join(img_folder, j)).convert()
    power_up_img['speedup'].append((img, i))

meteor_images = []
meteor_list = ['meteorBrown_big3.png', 'meteorGrey_big1.png','meteorBrown_med1.png',
               'meteorGrey_med1.png', 'meteorGrey_med2.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png','meteorGrey_small1.png',
               'meteorBrown_tiny1.png']
for i in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, i)).convert())

player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_blue.png')).convert()
background = pygame.image.load(os.path.join(img_folder, 'darkPurple.png')).convert()
meteor_img = pygame.image.load(os.path.join(img_folder, 'meteorBrown_small1.png')).convert()
bullet_img_player = pygame.image.load(os.path.join(img_folder, 'laserBlue03.png')).convert()
bullet_img_enemy = pygame.image.load(os.path.join(img_folder, 'laserRed03.png')).convert()
player_img_mini = pygame.transform.scale(player_img, (25, 25))
player_img_mini.set_colorkey(BLACK)

background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

# Создание элементов игры
pygame.display.set_caption("THE DICK IN THE SPACE")
clock = pygame.time.Clock()

# Цикл игры
running = True
game_over = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        power_ups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        dif = 0
        score = 0
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)

    for hit in hits:
        new_explosion(hit.rect.x, hit.rect.y, 'lg')
        new_damage(hit.rect.x, hit.rect.y)
        player.current_hp -= hit.radius * 2
        newmob()
        if player.current_hp <= 0:
            deth_exp = Explosion(player.rect.x, player.rect.y, 'player')
            all_sprites.add(deth_exp)
            player.hide()
            player.to_base()
            player.lives -= 1

    if player.lives == 0 and not deth_exp.alive():
        game_over = True

    # Проверка, не ударила ли пуля моба
    hits = pygame.sprite.groupcollide(mobs, player_bullets, True, True)
    for hit in hits:
        if hit.radius < 10:
            score += 3
            new_explosion(hit.rect.x, hit.rect.y, 'sm')
        elif hit.radius < 25:
            score += 2
            new_explosion(hit.rect.x, hit.rect.y, 'sm')
        else:
            new_explosion(hit.rect.x, hit.rect.y, 'lg')
            score += 1
        dif = (score // 100)
        newmob(dif)
        if random.random() > 0.1:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            power_ups.add(pow)

        expl = random.choice(expl_sounds)
        pygame.mixer.music.load(os.path.join(snd_dir, expl))
        pygame.mixer_music.play()

    # Проверка, не поймали ли улучшение
    hits = pygame.sprite.spritecollide(player, power_ups, True)
    for hit in hits:
        if hit.type == 'hp':
            player.current_hp += (hit.lvl + 1) * 10
            if player.current_hp >= player.base_hp:
                player.current_hp = player.base_hp
        if hit.type == 'speedup' and player.bonus_speed <= (hit.lvl + 1):
            player.bonus_speed = hit.lvl + 1
            player.bonus_speed_time_start = pygame.time.get_ticks()
            player.bonus_speed_flag = True
        if hit.type == 'gunup':
            if hit.lvl == 0:
                player.gunup(1)
            if hit.lvl == 1:
                player.gunup(2)

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_text(screen, str(player.power), 25, 10, 30)
    draw_shield_bar(screen, 5, 5, player.current_hp)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_img_mini)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
