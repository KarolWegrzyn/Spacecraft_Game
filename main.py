import pygame
import sys
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Kosmiczna Przygoda')

# Załaduj obrazki
player = pygame.image.load('Sprites/ship.png')
player_up = pygame.image.load('Sprites/ship_up.png')
player_image = player
enemy_image = pygame.image.load('Sprites/enemy.png')
bullet_image = pygame.image.load('Sprites/bullet.png')
enemy_bullet_image = pygame.image.load('Sprites/enemy_bullet.png')
background = pygame.image.load('Sprites/background.png')
counter = pygame.image.load('Sprites/Counter/counter.png')
background_image = pygame.transform.scale(background, (screen_width, screen_height))

coins_images = {
    9: pygame.image.load('Sprites/Counter/9.png'),
    8: pygame.image.load('Sprites/Counter/8.png'),
    7: pygame.image.load('Sprites/Counter/7.png'),
    6: pygame.image.load('Sprites/Counter/6.png'),
    5: pygame.image.load('Sprites/Counter/5.png'),
    4: pygame.image.load('Sprites/Counter/4.png'),
    3: pygame.image.load('Sprites/Counter/3.png'),
    2: pygame.image.load('Sprites/Counter/2.png'),
    1: pygame.image.load('Sprites/Counter/1.png'),
    0: pygame.image.load('Sprites/Counter/0.png')
}

health_images = {
    5: pygame.image.load('Sprites/Hearth/hearth_5.png'),
    4: pygame.image.load('Sprites/Hearth/hearth_4.png'),
    3: pygame.image.load('Sprites/Hearth/hearth_3.png'),
    2: pygame.image.load('Sprites/Hearth/hearth_2.png'),
    1: pygame.image.load('Sprites/Hearth/hearth_1.png'),
    0: pygame.image.load('Sprites/Hearth/hearth_0.png')
}

# Ustawienia gracza
player_x = 265
player_y = 700
player_speed = 0.4
player_health = 5
coins = 0
cooldown = 0
cooldown_extra = 500
bullets = []

class Enemy:
    def __init__(self, x, y, speed, image):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = image
        self.direction = 1  # Kierunek ruchu (1 = prawo, -1 = lewo)
        self.cooldown = 0  # Cooldown na strzelanie przeciwnika

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= screen_width - self.image.get_width():
            self.direction *= -1  # Zmiana kierunku

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def shoot(self, bullets):
        current_time = pygame.time.get_ticks()
        if current_time > self.cooldown:
            new_bullet = Bullet(self.x + self.image.get_width() // 2, self.y + self.image.get_height(), "enemy_bullet")
            bullets.append(new_bullet)
            self.cooldown = current_time + random.randint(1000, 3000)  # Losowy cooldown na strzał przeciwnika

# Utworzenie listy przeciwników
enemies = [
    Enemy(100, 55, 0.3, enemy_image),
    Enemy(200, 120, 0.3, enemy_image),
    Enemy(300, 185, 0.3, enemy_image),
]

class Bullet:
    def __init__(self, x, y, whose_bullet):
        self.x = x
        self.y = y
        self.speed = 0.5  # Prędkość pocisku
        self.whose_bullet = whose_bullet

        if whose_bullet == "player_bullet":
            self.image = bullet_image  # Obrazek pocisku
        elif whose_bullet == "enemy_bullet":
            self.image = enemy_bullet_image

    def move(self):
        if self.whose_bullet == "player_bullet":
            self.y -= self.speed  # Pociski poruszają się w górę
        elif self.whose_bullet == "enemy_bullet":
            self.y += self.speed  # Pociski poruszają się w dół

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def check_collision(bullet, enemy):
    bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.image.get_width(), bullet.image.get_height())
    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
    return bullet_rect.colliderect(enemy_rect)

def check_collision_player(bullet):
    bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.image.get_width(), bullet.image.get_height())
    player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
    return bullet_rect.colliderect(player_rect)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))
    screen.blit(player_image, (player_x, player_y))
    screen.blit(health_images[player_health],(5,5))
    screen.blit(counter, (430,5))

    screen.blit(coins_images[0], (550,11))
    screen.blit(coins_images[0], (565,11))
    screen.blit(coins_images[coins], (580,11))

    keys = pygame.key.get_pressed()

    # Ruch gracza
    if keys[pygame.K_LEFT] and player_x > -screen_width + screen_width + 5:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - 72:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 5:
        player_y -= player_speed
        player_image = player_up
    else:
        player_image = player
    if keys[pygame.K_DOWN] and player_y < screen_height - 78:
        player_y += player_speed

    current_time = pygame.time.get_ticks()  # Pobranie aktualnego czasu

    # Strzelanie Gracza
    if keys[pygame.K_SPACE] and current_time > cooldown:
        new_bullet = Bullet(player_x + 25, player_y - 50, "player_bullet")
        bullets.append(new_bullet)
        cooldown = current_time + cooldown_extra

    for bullet in bullets:
        bullet.move()

    for enemy in enemies:
        enemy.move()
        enemy.shoot(bullets)  # Przeciwnik strzela

    # Usuwanie pocisków poza ekranem
    bullets = [bullet for bullet in bullets if bullet.y > 0 and bullet.y < screen_height]

    # Sprawdzanie kolizji między pociskami a przeciwnikami
    for bullet in bullets:
        if bullet.whose_bullet == "player_bullet":
            for enemy in enemies:
                if check_collision(bullet, enemy):
                    coins += 1
                    print(coins)
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

    # Sprawdzanie kolizji między pociskami przeciwników a graczem
    for bullet in bullets:
        if bullet.whose_bullet == "enemy_bullet":
            if check_collision_player(bullet):
                print("Gracz trafiony!")
                bullets.remove(bullet)
                player_health -= 1

                if player_health == 0:
                    running = False

    for bullet in bullets:
        bullet.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    # Aktualizacja ekranu
    pygame.display.flip()

# Zakończenie działania Pygame
pygame.quit()
sys.exit()