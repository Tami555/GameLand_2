import os
import random
import sys
import pygame
from work_database_fail import checking_the_record


column_in_DataBase = 'Geese'
path = r'..\ALL_GAMES\Geese_Game\\imges'


def load_image(name, colorkey=None):
    fullname = f'{path}\\{name}'
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

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


class Gus(pygame.sprite.Sprite):
    def __init__(self, x, speed, points):
        super().__init__()
        self.points = points
        self.image = self.create_text()
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed

    def create_text(self):
        if self.points >= 0:
            img = load_image('gus.png')
            color = 'red'
        else:
            img = load_image('angry_gus.jpg')
            color = 'black'

        f = pygame.font.SysFont(None, 35)
        text = f.render(str(self.points), 1, color)
        image = pygame.transform.scale(img, (80, 100))

        if self.points < 0:
            image.set_colorkey((255, 255, 255))

        new_image = pygame.Surface((80, 100), pygame.SRCALPHA)  # pygame.SRCALPHA для прозрачности
        new_image.blit(image, (0, 0))  # отрисовываем изображение гуся
        new_image.blit(text, (30, 55))  # отрисовываем текст с очками

        return new_image

    def update(self, *args, **kwargs):
        if self.rect.y < args[0]:  # height
            self.rect.y += self.speed  # speed
        else:
            self.kill()


def main():
    try:
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        size = w, h = 1100, 800
        sc = pygame.display.set_mode(size)
        pygame.display.set_caption('Ловите Гусей')
        running = True
        clock = pygame.time.Clock()
        fps = 70

        # Музыка
        pygame.mixer.music.load(f'{path}\\music_fon.mp3')
        pygame.mixer.music.play(-1)
        duck_music = pygame.mixer.Sound(f'{path}\\duck_sound.ogg')

        pygame.time.set_timer(pygame.USEREVENT, 500)
        # Определяем пользовательские события
        CREATE_GUS = pygame.USEREVENT + 1
        QUIT_GAME = pygame.USEREVENT + 2
        TIMER = pygame.USEREVENT + 3

        pygame.time.set_timer(CREATE_GUS, 400)  # Таймер для генерации новых гусей
        pygame.time.set_timer(TIMER, 1000)  # Основной таймер на 30 сек
        timer = 30

        # ВСЕ ИЗОБРАЖЕНИЯ
        trava = pygame.image.load(f'{path}\\trava.jpg')  # Задний фон травы

        c = pygame.transform.scale(load_image('cart.jpg', -1), (200, 100))  # Тележка
        right, left = c, pygame.transform.flip(c, 1, 0)
        cart = right
        cart_rect = cart.get_rect(centerx=w // 2, bottom=h - 5)

        speed = 10  # Скорость тележки
        game_points = 0  # Всего очков за пойманных гусей
        img_f = load_image('end_fon.jpg')

        def start_screen():
            fon = pygame.transform.scale(pygame.image.load(f'{path}\\fon_guess_game.jpg'), (w, h))
            sc.blit(fon, (0, 0))

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN or \
                            event.type == pygame.MOUSEBUTTONDOWN:
                        return  # начинаем игру
                pygame.display.flip()
                clock.tick(fps)

        def create_text(count, timer):
            f = pygame.font.SysFont(None, 60)

            count_text = f.render(f'Count: {count}', 1, 'black', 'yellow')
            count_rect = count_text.get_rect()

            text_timer = f.render(f'Time: {timer}', 1, 'black', 'green')
            timer_rect = text_timer.get_rect(topright=(450, 0))

            sc.blit(count_text, count_rect)
            sc.blit(text_timer, timer_rect)

        def create_Gus():
            x = random.randint(50, w - 50)
            speed = random.randint(1, 10)
            point = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            return Gus(x, speed, point)

        guss = pygame.sprite.Group()
        gus = create_Gus()
        win = None

        def collider_Gus():
            """Метод для проверки столкновений (гусей с тележкой)"""
            nonlocal game_points
            for g in guss:
                if cart_rect.collidepoint(g.rect.center):
                    game_points += g.points
                    duck_music.play()
                    g.kill()

        def win_close(count):
            nonlocal img_f
            """Создание поверхности для выйгрыша"""
            img_f = pygame.transform.scale(img_f, (1100, 800))
            checking_the_record(column_in_DataBase, count, 'max')
            w = pygame.Surface((1100, 800))
            w.fill('red')
            w.blit(img_f, (0, 0))
            return w

        start_screen()
        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    print('EXIT', os.getcwd())
                    pygame.quit()

                if event.type == CREATE_GUS:
                    if win is None:
                        gus = create_Gus()
                        guss.add(gus)

                if event.type == TIMER:
                    if timer > 0:
                        timer -= 1
                    else:
                        if win is None:
                            win = win_close(game_points)
                            pygame.time.set_timer(QUIT_GAME, 2000)  # Запускаем таймер для закрытия

                if event.type == QUIT_GAME:
                    running = False
                    pygame.quit()

            lst_keys = pygame.key.get_pressed()
            if lst_keys[pygame.K_LEFT]:
                cart = left
                cart_rect.x -= speed
                if cart_rect.x < 0:
                    cart_rect.x = 0

            elif lst_keys[pygame.K_RIGHT]:
                cart = right
                cart_rect.x += speed

                if cart_rect.topright[0] > w:
                    cart_rect.topright = (w, cart_rect.topright[1])

            collider_Gus()
            sc.blit(trava, (0, 0))
            create_text(game_points, timer)
            guss.update(h)
            guss.draw(sc)
            sc.blit(cart, cart_rect)

            if win is not None:
                win = win_close(game_points)
                sc.blit(win, (0, 0))
                print('EXIT', os.getcwd())

            pygame.display.update()
            clock.tick(fps)
    except Exception as e:
        print('ОШИБКА ОТ ГУСЕЙ', e)