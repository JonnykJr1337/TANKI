import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((512, 512))
FPS = 100
clock = pygame.time.Clock()
shot_direction_rus = 0
shot_direction_hoh = 0
bullet_owner = "rus"
tank_1_live = True
tank_2_live = True
cooldown = 2500
last_rus_shot = 0
last_ucr_shot = 0
shotscounter = 0
pygame.display.set_caption('TankITank')
pygame.display.set_icon(pygame.image.load('data/Dota2.png'))

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('data/Startscreen.png'), (512, 512))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def redwin_screen():
    global running
    fon = pygame.transform.scale(load_image('data/RedWinScreen.png'), (512, 512))
    text = 'Всего выстрелов:' + str(shotscounter)
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render(text, True,
                      (180, 0, 0))
    screen.blit(fon, (0, 0))
    screen.blit(text1, (0, 400))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def bluwin_screen():
    global running
    fon = pygame.transform.scale(load_image('data/BlueWinScreen.png'), (512, 512))
    text = 'Всего выстрелов:' + str(shotscounter)
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render(text, True,
                      (180, 0, 0))
    screen.blit(fon, (0, 0))
    screen.blit(text1, (0, 400))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name):
    image = pygame.image.load(name)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('data/UnbreakableBlock.png'),
    'grass': load_image('data/Grass.png'),
    "flag_floor": load_image('data/FlagFloor.png'),
    'red_flag': load_image('data/RedFlag.png'),
    "blue_flag": load_image('data/BlueFlag.png'),
}

number_images = {
    0: load_image('data/0.png'),
    1: load_image('data/1.png'),
    2: load_image('data/2.png'),
    3: load_image('data/3.png')
}
wall_image = load_image('data/UnbreakableBlock.png')
tank_1_image = load_image('data/RusTankSpritesheet.png')
tank_1_destroyed_image = load_image('data/BurnTankSpritesheet.png')
tank_2_image = load_image('data/UcrTankSpritesheet.png')
tank_2_destroyed_image = load_image('data/BurnTankSpritesheet.png')
bullet_image = load_image('data/Bullet.png')
red_image = load_image('data/RedFlag.png')
blue_image = load_image('data/BlueFlag.png')
tile_width = tile_height = 32


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tank_1(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tank_1_image, 1, 2, pos_x * 32, pos_y * 32)
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        bluwin_screen()

    def update(self):
        if tank_1_live:
            super().update()
            self.image = pygame.transform.rotate(self.image, shot_direction_rus)
            if pygame.sprite.pygame.sprite.spritecollideany(self, walls_group):
                if shot_direction_rus == 270:
                    self.rect = self.rect.move(-velocity, 0)
                elif shot_direction_rus == 90:
                    self.rect = self.rect.move(velocity, 0)
                elif shot_direction_rus == 180:
                    self.rect = self.rect.move(0, -velocity)
                elif shot_direction_rus == 0:
                    self.rect = self.rect.move(0, velocity)


class Dead_man(AnimatedSprite):
    def __init__(self, pos_x, pos_y, rotate):
        super().__init__(tank_1_destroyed_image, 1, 6, pos_x, pos_y)
        self.rotate = rotate

    def update(self):
        dead_man = Dead_man(tank_2.rect.x, tank_2.rect.y, shot_direction_hoh)
        super().update()
        self.image = pygame.transform.rotate(self.image, self.rotate)


class Tank_2(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tank_2_image, 1, 2, pos_x * 32, pos_y * 32)
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        dead_man = Dead_man(tank_2.rect.x, tank_2.rect.y, shot_direction_rus)
        redwin_screen()

    def update(self):
        if tank_2_live:
            super().update()
            self.image = pygame.transform.rotate(self.image, shot_direction_hoh)
            if pygame.sprite.pygame.sprite.spritecollideany(self, walls_group):
                if shot_direction_hoh == 270:
                    self.rect = self.rect.move(-velocity, 0)
                elif shot_direction_hoh == 90:
                    self.rect = self.rect.move(velocity, 0)
                elif shot_direction_hoh == 180:
                    self.rect = self.rect.move(0, -velocity)
                elif shot_direction_hoh == 0:
                    self.rect = self.rect.move(0, velocity)


class Counter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(numbers_group, all_sprites)
        self.count = 0
        self.image = number_images[self.count]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)

    def update(self):
        self.image = number_images[self.count]


class Flag(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, color):
        super().__init__(flags_group, all_sprites)
        self.color = color
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 32
        self.rect.y = pos_y * 32
        self.basex = pos_x * 32
        self.basey = pos_y * 32
        self.onbase = True
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.collide_mask(self,
                                      tank_1) and self.color == 'blue' and tank_1_live:  # забираем флаг за красного
            self.rect = self.image.get_rect().move(tank_1.rect.x, tank_1.rect.y)
            self.onbase = False
        if pygame.sprite.collide_mask(self, tank_2) and self.color == 'red' and tank_2_live:  # забираем флаг за синего
            self.onbase = False
            self.rect = self.image.get_rect().move(tank_2.rect.x, tank_2.rect.y)
        if (pygame.sprite.collide_mask(self, tank_1) and self.color == 'red' and not tank_2_live) or (  # подбираем флаг
                pygame.sprite.collide_mask(self, tank_2) and self.color == 'blue' and not tank_1_live):
            self.rect = self.image.get_rect().move(self.basex, self.basey)
            self.onbase = True
        if self.color == 'red' and pygame.sprite.collide_mask(tank_2,
                                                              blue_flag) and not self.onbase and blue_flag.onbase:  # захват флага красным
            ucrcounter.count += 1
            self.rect = self.image.get_rect().move(self.basex, self.basey)
            self.onbase = True
        if self.color == 'blue' and pygame.sprite.collide_mask(tank_1,
                                                               red_flag) and not self.onbase and red_flag.onbase:  # захват флага синим
            self.rect = self.image.get_rect().move(self.basex, self.basey)
            self.onbase = True
            ruscounter.count += 1
        if ucrcounter.count == 3:
            bluwin_screen()
        if ruscounter.count == 3:
            redwin_screen()


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = wall_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bullet_group, all_sprites)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.owner = bullet_owner
        if self.owner == "rus":
            self.direction = shot_direction_rus
        if self.owner == "bandera":
            self.direction = shot_direction_hoh

    def update(self):
        if self.direction == 270:
            self.rect.x += 4
        elif self.direction == 90:
            self.rect.x -= 4
        elif self.direction == 180:
            self.rect.y += 4
        elif self.direction == 0:
            self.rect.y -= 4

        if pygame.sprite.collide_mask(self, tank_1) and self.owner != "rus":
            tank_1.destroy()
        if pygame.sprite.collide_mask(self, tank_2) and self.owner != "bandera":
            tank_2.destroy()


tank_1 = None
tank_2 = None
# группы спрайтов

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
flags_group = pygame.sprite.Group()
numbers_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()


def generate_level(level):
    new_tank_1, new_tank_2, wall, x, y = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                new_wall = Wall(x, y)
            elif level[y][x] == 'R':
                Tile('flag_floor', x, y)
                red_flag = Flag(x, y, red_image, 'red')
                new_tank_1 = Tank_1(x, y)
            elif level[y][x] == 'B':
                Tile('flag_floor', x, y)
                blue_flag = Flag(x, y, blue_image, 'blue')
                new_tank_2 = Tank_2(x, y)
            elif level[y][x] == '_':
                Tile('flag_floor', x, y)
    ruscounter = Counter(480, 480)
    ucrcounter = Counter(0, 0)

    # вернем игрока, а также размер поля в клетках
    return new_wall, new_tank_1, new_tank_2, red_flag, blue_flag, ruscounter, ucrcounter


start_screen()
wall, tank_1, tank_2, red_flag, blue_flag, ruscounter, ucrcounter = generate_level(load_level('map.txt'))
running = True
velocity = 1
movement_timer = pygame.USEREVENT + 1
pygame.time.set_timer(movement_timer, 22)
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if tank_1_live:
            if event.type == movement_timer:
                if keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                    tank_1.rect.x -= velocity
                    shot_direction_rus = 90
                if keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                    tank_1.rect.x += velocity
                    shot_direction_rus = 270
                if keys[pygame.K_UP]:
                    tank_1.rect.y -= velocity
                    shot_direction_rus = 0
                if keys[pygame.K_DOWN]:
                    tank_1.rect.y += velocity
                    shot_direction_rus = 180
            if keys[pygame.K_RCTRL]:
                now = pygame.time.get_ticks()
                if now - last_rus_shot > cooldown:
                    shotscounter += 1
                    bullet_owner = "rus"
                    last_rus_shot = pygame.time.get_ticks()
                    bullet = Bullet(tank_1.rect.x, tank_1.rect.y)
        # движ 2 ----------------------------
        if tank_2_live:
            if event.type == movement_timer:
                if keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]:
                    tank_2.rect.x -= velocity
                    shot_direction_hoh = 90
                if keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
                    tank_2.rect.x += velocity
                    shot_direction_hoh = 270
                if keys[pygame.K_w]:
                    tank_2.rect.y -= velocity
                    shot_direction_hoh = 0
                if keys[pygame.K_s]:
                    tank_2.rect.y += velocity
                    shot_direction_hoh = 180
            if keys[pygame.K_f]:
                now = pygame.time.get_ticks()
                if now - last_ucr_shot > cooldown:
                    shotscounter += 1
                    bullet_owner = "bandera"
                    last_ucr_shot = pygame.time.get_ticks()
                    bullet = Bullet(tank_2.rect.x, tank_2.rect.y)

    tiles_group.draw(screen)
    player_group.update()
    player_group.draw(screen)
    flags_group.update()
    flags_group.draw(screen)
    bullet_group.update()
    bullet_group.draw(screen)
    numbers_group.update()
    numbers_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
