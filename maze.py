
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < win_width - 60:
            self.rect.x += self.speed

        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < win_height - 60:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(
            player_image,
            player_x,
            player_y,
            player_speed
        )
        self.side = "up"
    
    def update(self):
        if self.rect.y <= 220:
            self.side = "down"

        if self.rect.y >= 350:
            self.side = "up"

        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Enemy2(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(
            player_image,
            player_x,
            player_y,
            player_speed
        )
        self.side = "left"
    
    def update(self):
        if self.rect.x <= 220:
            self.side = "right"

        if self.rect.x >= 500:
            self.side = "left"

        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(
            self,
            color_1,
            color_2,
            color_3,
            wall_x,
            wall_y,
            wall_width,
            wall_height,
    ):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill((color_1, color_2, color_3))

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

player = Player(
    "hero.png",
    20,
    420,
    4
)

monster = Enemy(
    "cyborg.png",
    350,
    250,
    2
)

monster2 = Enemy2(
    "sawit.png",
    350,
    250,
    2
)

final = GameSprite(
    "treasure.png",
    600,
    420,
    0
)

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)

w4 = Wall(154, 205, 50, 200, 130, 250, 10)
w5 = Wall(154, 205, 50, 200, 130, 10, 350)
w6 = Wall(154, 205, 50, 550, 20, 10, 380)
w7 = Wall(154, 205, 50, 310, 390, 250, 10)

walls = [w1, w2, w3, w4, w5, w6, w7]

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()

font1 = font.SysFont('Arial', 70)
win_text = font1.render(
    "YOU LOSE!",
    True,
    (255, 0, 0)
)
lose_text = font1.render(
    "YOU WIN",
    True,
    (255, 215, 0)
)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monster.update()
        monster2.update()

        player.reset()
        monster.reset()
        monster2.reset()
        final.reset()

        for wall in walls:
            wall.draw_wall()

        lose_game = sprite.collide_rect(
            player,
            monster
        )

        for wall in walls:
            if sprite.collide_rect(player, wall):
                lose_game = False

        if lose_game:
            finish = True
            window.blit(
                lose_text,
                (180, 220)
            )

        if sprite.collide_rect(
            player,
            final
        ):
            
            finish = True
            window.blit(
                win_text,
                (180, 220)
            )

    display.update()
    clock.tick(FPS)