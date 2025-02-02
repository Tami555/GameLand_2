import time
import pygame
import os
import random
from work_database_fail import checking_the_record

# pygame.mixer.pre_init(44100, -16, 1, 512) # для хорошего звука

column_in_DataBase = 'Cow'
path = r'..\ALL_GAMES\Cow_game\\data'
# Уровни, раpмер экрана под них, цвет поля
levels_value = {1: ['level.txt', (800, 550), '#08bd92'],
                2: ['level_2.txt', (900, 550), '#007004'],
                3:  ['level_3.txt', (900, 700), '#7f0303'],
                4: ['level_4.txt', (900, 800), '#020070'],
                5: ['level_5.txt', (1200, 800), '#8f034d']
                }

level = key_level = tile_width = tile_height = lifes = count_milk = all_milk = speed_monster = running = None


def upload_level():
    """Получение уровня"""
    global key_level
    l = [key_level, *levels_value[key_level]]
    return l


def update_level(l, r):
    """Обновление уровня и рекорда """
    global key_level
    key_level = l
    checking_the_record(column_in_DataBase, r, 'max')


def load_image(name, colorkey=None):
    """Для загрузки изображений """
    fullname = f'{path}\\{name}'
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        return
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)
        image.set_colorkey(color)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    """Загрузка определенного уровня"""
    try:
        filename = f'{path}\\{filename}'
        with open(filename, 'r') as mapFile:
            level_map = [list(line.strip()) for line in mapFile]
            return level_map

    except FileNotFoundError:
        print('Такого файла не существует !!!!!')
        return


def start_screen(scr, w, h):
    """Заставка"""
    global key_level
    fon = pygame.transform.scale(pygame.image.load(f'{path}\\start_screen_2.JPEG'), (w, h))
    scr.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                key_level = 1
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(50)


def random_monster():
    """Выбор случайного монстра"""
    lst = ['enemy.png', 'enemy_2.png', 'enemy_3.png', 'enemy_4.png']
    i = random.choice(lst)
    return load_image(i, -1)


def random_angry_block():
    """Выбор случайного опасного блока (огонь, кислота, острый куб)"""
    lst = [load_image('knife.JPEG', 2),
           load_image('cislota.JPEG', -1),
           load_image('fire.PNG')]
    return random.choice(lst)


def create_text(count, lifes, scr):
    """Добавление текста: кол молока, жизни, уровень"""
    f = pygame.font.SysFont(None, 60)
    color_point = '#17039c'
    img_points = pygame.transform.scale(load_image('milk.jpg', -2), (50, 50))

    if count >= ((all_milk * 90) // 100) * 10:
        color_point = 'yellow'

    count_text = f.render(f'Count: {count}', 1, color_point)

    img_heart = pygame.transform.scale(load_image('heart.jpg', -1), (50, 50))
    text_life = f.render(f'Life: {round(lifes)}', 1, 'red')

    text_level = f.render(f'Level: {level[0]}', 1, 'white')

    scr.blit(img_points, (10, 0))
    scr.blit(img_heart, (330, 0))
    scr.blit(count_text, (70, 0))
    scr.blit(text_life, (400, 0))
    scr.blit(text_level, (600, 0))


def final_screen(scr, music_lst=(), final=False, w=0, h=0):
    """Финальная заставка, после окончания уровня"""
    global key_level
    # Проверка на проигрыш
    photo = None
    long = 4
    next_level = False
    gameover, win_all, win_sound = music_lst

    if lifes <= 0 or (final and count_milk < ((all_milk * 90) // 100) * 10):
        photo = 'fin_end.jpg'
        pygame.mixer.music.stop()
        key_level = 1
        gameover.play()

    elif final:
        # Проверка на выйгрыш
        photo = 'fin_win.jpg'

        if level[0] == len(levels_value):
            # Если последний уровень
            photo = 'final_fon.jpeg'
            long = 12
            win_all.play(-1)

        # Проверка на побитие рекорда
        # elif record < count_milk:
        #     photo = 'fin_win_record.jpg'
        #     update_level(level[0] + 1, count_milk)
        #     win_sound.play()
        #     next_level = True

        else:
            update_level(key_level + 1, count_milk)
            win_sound.play()
            next_level = True
        pygame.mixer.music.stop()

    if photo is not None:
        # Показ заставки
        photo = pygame.transform.scale(load_image(photo), (w, h))
        scr.blit(photo, (0, 0))
        pygame.display.flip()
        time.sleep(long)
        if not next_level:
            pygame.quit()

    return next_level


class Player(pygame.sprite.Sprite):
    """Класс Главного Героя (Корова)"""
    def __init__(self, pos_x, pos_y, img):
        super().__init__()
        self.image = pygame.transform.scale(img, (45, 45))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Point(pygame.sprite.Sprite):
    """Класс очков. Молока или доп жизни"""
    def __init__(self, pos_x, pos_y, img, hear=False):
        super().__init__()
        self.hear = hear
        self.image = pygame.transform.scale(img, (25, 25))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))


class Wall(pygame.sprite.Sprite):
    """Стены, свободные блоки, блоки с очками"""
    def __init__(self, pos_x, pos_y, img, point_grop, milk=False, h=False, milk_img=None):
        super().__init__()
        if img != '':
            # Для стены
            self.image = pygame.transform.scale(img, (50, 50))
        else:
            # Для свободного блока
            self.image = pygame.Surface((50, 50))
            self.image.fill(level[-1])

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        if milk or h:
            # если есть метка молока или доп жизни
            center_x = self.rect.x + tile_width // 2
            center_y = self.rect.y + tile_height // 2
            if milk:
                p = Point(center_x, center_y, milk_img)
            else:
                p = Point(center_x, center_y, load_image('heart.jpg', -1), True)
            point_grop.add(p)
            self.image.blit(p.image, p.rect)


class Enemy(pygame.sprite.Sprite):
    """Класс Врага (Инопланетян)"""
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(random_monster(), (45, 45))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, player_rect, enem_grop):
        # Преследование коровы
        dx = player_rect.center[0] - self.rect.center[0]
        dy = player_rect.center[1] - self.rect.center[1]

        if abs(dx) > 1 or abs(dy) > 1:  # чтоб не "залипали" на герое
            max_step = max(abs(dx // speed_monster), abs(dy // speed_monster))
            if max_step > 0:  # проверка, что бы не делить на ноль
                # Проверка столкновений с другими врагами
                for other_enemy in enem_grop:
                    if other_enemy != self and self.rect.colliderect(other_enemy.rect):
                        # Отталкиваем врага от другого врага
                        overlap_x = (self.rect.center[0] - other_enemy.rect.center[0]) / 2
                        overlap_y = (self.rect.center[1] - other_enemy.rect.center[1]) / 2
                        self.rect.center = (self.rect.center[0] + overlap_x, self.rect.center[1] + overlap_y)

                self.rect.center = (self.rect.center[0] + dx / max_step, self.rect.center[1] + dy / max_step)


class AngryBlock(pygame.sprite.Sprite):
    """Класс Опасных блоков"""
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(random_angry_block(), (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Exit(pygame.sprite.Sprite):
    """Класс Выхода (завершения игры) """
    def __init__(self, pos_x, pos_y, img):
        super().__init__()
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(lev, lst_group):
    """Заполнение поля по символам из уровня"""
    global all_milk
    new_player, x, y, exit_game = None, None, None, None
    for x in lst_group:
        x.empty()

    wall, free, enemy, points, angry = lst_group

    # Изображения
    cow_stop = load_image('cow_1.png', -1)
    wall_img = load_image('stone_wall.jpg')
    m_img = load_image('milk.jpg', -2)
    exit_img = load_image('exit.png', -1)

    for y in range(len(lev)):
        for x in range(len(lev[y])):
            if lev[y][x] == '.':
                # Проходимый блок, без всего
                f = Wall(x, y, '', points)
                free.add(f)

            elif lev[y][x] == '$':
                # Проходимый блок с молоком
                f = Wall(x, y, '', points, True, milk_img=m_img)
                free.add(f)
                all_milk += 1

            elif lev[y][x] == '#':
                # Стена
                w = Wall(x, y, wall_img, points)
                wall.add(w)

            elif lev[y][x] == '@':
                # Главный герой (корова)
                f = Wall(x, y, '', points)
                free.add(f)
                new_player = Player(x, y, cow_stop)

            elif lev[y][x] == '&':
                # Враг (Инопланетянин)
                e = Enemy(x, y)
                enemy.add(e)

            elif lev[y][x] == ']':
                # Опасный блок
                a = AngryBlock(x, y)
                angry.add(a)

            elif lev[y][x] == '%':
                # Выход
                exit_game = Exit(x, y, exit_img)

            elif lev[y][x] == '!':
                # Проходимый блок с доп жизнью (сердце)
                f = Wall(x, y, '', points, h=True)
                free.add(f)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, exit_game


def music_load():
    # Музыка и звуки
    pygame.mixer.music.load(f'{path}\\cow_music_fon.mp3')
    pygame.mixer.music.play(-1)
    pain = pygame.mixer.Sound(f'{path}\\Ай.ogg')
    gameover = pygame.mixer.Sound(f'{path}\\gameover.ogg')
    win_all = pygame.mixer.Sound(f'{path}\\all_win_sound.ogg')
    win_sound = pygame.mixer.Sound(f'{path}\\win_music.wav')
    nam = pygame.mixer.Sound(f'{path}\\nam_nam.ogg')
    return gameover, win_all, win_sound, pain, nam


def escape():
    global key_level, running
    key_level = 1
    running = True


def game_main():
    """ Главная функция ИГРЫ"""
    try:
        global count_milk, lifes, key_level, level, running,\
        level, key_level, tile_width, tile_height, lifes, count_milk, all_milk,  speed_monster

        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        # Данные
        key_level = 1
        tile_width = tile_height = 50  # размер клетки
        lifes = 3  # Количество жизней
        count_milk = 0  # Количество собранного молока
        all_milk = 0  # Всего молока на поле
        speed_monster = 1  # Скорость врагов
        running = True

        # Само Поле
        clock = pygame.time.Clock()
        fps = 50
        running = True
        level = upload_level()
        size = w, h = level[2]
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Cowscape')
        pygame.display.set_icon(pygame.image.load(f'{path}\\cow_icon.jpg'))

        # Музыка
        music_list = music_load()
        pain, nam = music_list[-2:]

        # ВСЕ ГРУППЫ СПАРАЙТОВ
        wall_group, free_group, enemy_group, points_group, angry_group = [pygame.sprite.Group() for _ in range(5)]
        player, level_x, level_y, exit_game = generate_level(load_level(level[1]),
                                [wall_group, free_group, enemy_group, points_group, angry_group])
        start_screen(screen, w, h)
        print('Поехалиии')
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    key_level = 1
                    pygame.quit()

            keys = pygame.key.get_pressed()
            x = 0
            y = 0

            # Движение влево, вправо, вверх и вниз
            if keys[pygame.K_LEFT]:
                x -= 10
            elif keys[pygame.K_RIGHT]:
                x += 10
            elif keys[pygame.K_DOWN]:
                y += 10
            elif keys[pygame.K_UP]:
                y -= 10
            # Проверка на коллизию по X
            if x != 0:
                player.rect.move_ip(x, 0)
                if any(pygame.sprite.collide_mask(player, l) for l in wall_group):
                    player.rect.move_ip(-x, 0)

            elif y != 0:
                player.rect.move_ip(0, y)
                if any(pygame.sprite.collide_mask(player, l) for l in wall_group):
                    player.rect.move_ip(0, -y)

            screen.fill(level[-1])

            # Отрисовка групп блоков
            free_group.draw(screen)
            wall_group.draw(screen)
            enemy_group.draw(screen)
            points_group.draw(screen)
            angry_group.draw(screen)
            # Отрисовка блоков
            screen.blit(exit_game.image, exit_game.rect)
            screen.blit(player.image, player.rect)
            # Обновление блоков

            # Проверка столкновений
            for p in points_group:
                # Проверка на столкновение с молоком или доп жизнями
                if player.rect.collidepoint(p.rect.center):
                    if p.hear:
                        if lifes < 3:
                            lifes += 1
                            nam.play()
                    else:
                        count_milk += 10
                    p.kill()

            for e in enemy_group:
                # Проверка на столкновение с врагами
                if player.rect.collidepoint(e.rect.center):
                    lifes -= 0.1
                    pain.play()

            for a in angry_group:
                # Проверка на столкновение с опасными блоками
                if player.rect.collidepoint(a.rect.center):
                    lifes -= 0.1
                    pain.play()

            # Обновление координат игрока для преследований
            enemy_group.update(player.rect, enemy_group)

            create_text(count_milk, lifes, screen)  # Текст
            final_screen(screen, music_list[:-2], w=w, h=h)  # Проверка на наличие жизни

            if player.rect.colliderect(exit_game.rect):
                # Касание Выхода: запуск нового уровня или сразу завершение игры
                if final_screen(screen, music_list[:-2], True, w, h):
                    level = upload_level()
                    size = w, h = level[2]
                    screen = pygame.display.set_mode(size)
                    screen.fill('black')
                    create_text(count_milk, 3, screen)
                    lifes = 3
                    player, level_x, level_y, exit_game = generate_level(load_level(level[1]),
                                                                         [wall_group, free_group, enemy_group,
                                                                          points_group, angry_group])
                    start_screen(screen, w, h)
                    pygame.mixer.music.play(-1)

                else:
                    running = False
                    key_level = 1
                    pygame.quit()

            pygame.display.flip()
            clock.tick(fps)
    except Exception as e:
        print(e)
