import pygame
import json
import os
from random import randint


FPS = 60
B_SIZE = 40
WIN_SIZE = 25


class Snake:
    def __init__(self, body, direction):
        self.body = [(j[0] * B_SIZE, j[1] * B_SIZE) for j in body]
        self.direction = direction
        self.length = len(body)

    def move(self):
        self.body.append((self.body[-1][0] + self.direction[0] * B_SIZE, self.body[-1][1] + self.direction[1] * B_SIZE))
        self.body = self.body[-self.length:]


def create_apple(snake_coordinates):
    apple_coordinates = randint(0, WIN_SIZE - 1) * B_SIZE, randint(0, WIN_SIZE - 1) * B_SIZE
    if apple_coordinates in snake_coordinates:
        create_apple(snake_coordinates)
    return randint(0, WIN_SIZE - 1) * B_SIZE, randint(0, WIN_SIZE - 1) * B_SIZE


def get_level_settings(level):
    with open('levels.json', 'r') as json_file:
        settings = json.load(json_file)
    result = {}
    for k, v in settings[level].items():
        if k == 'amount_of_food':
            result[k] = v
        else:
            for address, dirs, files in os.walk(v):
                res_files = []
                for file in files:
                    res_files.append(address + '/' + file)
                result[k] = res_files
    return result


def get_image_objects(settings):
    for k, v in settings.items():
        if k != 'amount_of_food':
            images = {}
            for file in v:
                images[file.split('/')[-1].split('.')[0]] = pygame.image.load(file)
            settings[k] = images
    return settings


def get_foods_images(objects_dict):
    result = []
    for _, v in objects_dict.items():
        result.append(v)
    return result


def main(level):

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_SIZE * B_SIZE, WIN_SIZE * B_SIZE))
    pygame.display.update()
    pygame.display.set_caption('Snake')

    settings = get_level_settings(level)
    images = get_image_objects(settings)

    font_arial_26 = pygame.font.SysFont('Arial', 26, bold=True)
    font_arial_60 = pygame.font.SysFont('Arial', 60, bold=True)

    snake = Snake([(3, 13), (4, 13), (5, 13)], [1, 0])
    keys = {'up': True, 'right': False, 'down': True, 'left': True}
    score = 0
    speed = 1

    food_images = get_foods_images(images['food'])
    amount_of_food = settings['amount_of_food']
    fruits_spawn = []
    for _ in range(amount_of_food):
        ind = randint(0, len(food_images) - 1)
        fruits_spawn.append([food_images[ind], create_apple(snake.body)])

    scr = 0
    scr_k = 12

    screen_coords_1 = [-1000, -1000]
    screen_coords_2 = [-1000, -1000]
    screen_coords_3 = [-1000, -1000]

    game_started = False
    quit_game = False
    while not quit_game:
        screen.fill(pygame.Color('black'))
        screen.blit(images['background']['bkg_1'], screen_coords_1)
        screen.blit(images['background']['bkg_2'], screen_coords_2)
        screen.blit(images['background']['bkg_3'], screen_coords_3)

        sprites = []
        snake_coords = snake.body[::-1]
        for coords in snake_coords:
            if coords == snake_coords[0] and len(snake_coords) > 1:
                if coords[0] == snake_coords[1][0] and coords[1] + 1 * B_SIZE == snake_coords[1][1]:
                    if snake.direction == [0, -1]:
                        sprites.append((images['skin']['head_up'], coords))
                    elif snake.direction == [-1, 0]:
                        sprites.append((images['skin']['head_up_left'], coords))
                    elif snake.direction == [1, 0]:
                        sprites.append((images['skin']['head_up_right'], coords))
                elif coords[0] - 1 * B_SIZE == snake_coords[1][0] and coords[1] == snake_coords[1][1]:
                    if snake.direction == [1, 0]:
                        sprites.append((images['skin']['head_right'], coords))
                    elif snake.direction == [0, -1]:
                        sprites.append((images['skin']['head_right_left'], coords))
                    elif snake.direction == [0, 1]:
                        sprites.append((images['skin']['head_right_right'], coords))
                elif coords[0] == snake_coords[1][0] and coords[1] - 1 * B_SIZE == snake_coords[1][1]:
                    if snake.direction == [0, 1]:
                        sprites.append((images['skin']['head_down'], coords))
                    elif snake.direction == [-1, 0]:
                        sprites.append((images['skin']['head_down_right'], coords))
                    elif snake.direction == [1, 0]:
                        sprites.append((images['skin']['head_down_left'], coords))
                elif coords[0] + 1 * B_SIZE == snake_coords[1][0] and coords[1] == snake_coords[1][1]:
                    if snake.direction == [-1, 0]:
                        sprites.append((images['skin']['head_left'], coords))
                    elif snake.direction == [0, 1]:
                        sprites.append((images['skin']['head_left_left'], coords))
                    elif snake.direction == [0, -1]:
                        sprites.append((images['skin']['head_left_right'], coords))
            if coords == snake_coords[0] and len(snake_coords) == 1:
                if snake.direction == [0, -1]:
                    sprites.append((images['skin']['single_up'], coords))
                elif snake.direction == [1, 0]:
                    sprites.append((images['skin']['single_right'], coords))
                elif snake.direction == [0, 1]:
                    sprites.append((images['skin']['single_down'], coords))
                elif snake.direction == [-1, 0]:
                    sprites.append((images['skin']['single_left'], coords))
            if len(snake_coords) > 2 and coords != snake_coords[-1] and coords != snake_coords[0]:
                cur_index = snake_coords.index(coords)
                if snake_coords[cur_index + 1][0] == coords[0] and snake_coords[cur_index - 1][0] == coords[0]:
                    sprites.append((images['skin']['body_vertical'], coords))
                elif snake_coords[cur_index + 1][1] == coords[1] and snake_coords[cur_index - 1][1] == coords[1]:
                    sprites.append((images['skin']['body_horizontal'], coords))
                if coords[0] + 1 * B_SIZE == snake_coords[cur_index + 1][0] and coords[1] + 1 * B_SIZE == \
                        snake_coords[cur_index - 1][1] \
                        or coords[1] + 1 * B_SIZE == snake_coords[cur_index + 1][1] and coords[0] + 1 * B_SIZE == \
                        snake_coords[cur_index - 1][0]:
                    sprites.append((images['skin']['body_left_top'], coords))
                elif coords[1] + 1 * B_SIZE == snake_coords[cur_index + 1][1] and coords[0] - 1 * B_SIZE == \
                        snake_coords[cur_index - 1][0] \
                        or coords[0] - 1 * B_SIZE == snake_coords[cur_index + 1][0] and coords[1] + 1 * B_SIZE == \
                        snake_coords[cur_index - 1][1]:
                    sprites.append((images['skin']['body_right_top'], coords))
                elif coords[0] + 1 * B_SIZE == snake_coords[cur_index + 1][0] and coords[1] - 1 * B_SIZE == \
                        snake_coords[cur_index - 1][1] \
                        or coords[1] - 1 * B_SIZE == snake_coords[cur_index + 1][1] and coords[0] + 1 * B_SIZE == \
                        snake_coords[cur_index - 1][0]:
                    sprites.append((images['skin']['body_left_bot'], coords))
                elif coords[1] - 1 * B_SIZE == snake_coords[cur_index + 1][1] and coords[0] - 1 * B_SIZE == \
                        snake_coords[cur_index - 1][0] \
                        or coords[0] - 1 * B_SIZE == snake_coords[cur_index + 1][0] and coords[1] - 1 * B_SIZE == \
                        snake_coords[cur_index - 1][1]:
                    sprites.append((images['skin']['body_right_bot'], coords))
            if coords == snake_coords[-1] and len(snake_coords) != 1:
                if snake_coords[-2][0] + 1 * B_SIZE == coords[0] and snake_coords[-2][1] == coords[1]:
                    sprites.append((images['skin']['tail_right'], coords))
                elif snake_coords[-2][0] == coords[0] and snake_coords[-2][1] - 1 * B_SIZE == coords[1]:
                    sprites.append((images['skin']['tail_up'], coords))
                elif snake_coords[-2][0] - 1 * B_SIZE == coords[0] and snake_coords[-2][1] == coords[1]:
                    sprites.append((images['skin']['tail_left'], coords))
                elif snake_coords[-2][0] == coords[0] and snake_coords[-2][1] + 1 * B_SIZE == coords[1]:
                    sprites.append((images['skin']['tail_down'], coords))

        for sprite in sprites:
            sprite, coordinates = sprite
            screen.blit(sprite, coordinates)

        for fruit in fruits_spawn:
            img, coords = fruit
            screen.blit(img, coords)

        render_score = font_arial_26.render(f'SCORE: {score}', 1, pygame.Color('orange'))
        render_speed = font_arial_26.render(f'SPEED: {speed}', 1, pygame.Color('orange'))
        screen.blit(render_score, (5, 5))
        screen.blit(render_speed, (5, 50))

        if scr % scr_k == 0:
            snake.move()

        if snake.direction == [0, -1]:
            screen_coords_1[1] += 1
            screen_coords_2[1] += 2
            screen_coords_3[1] += 3
        elif snake.direction == [1, 0]:
            screen_coords_1[0] -= 1
            screen_coords_2[0] -= 2
            screen_coords_3[0] -= 3
        elif snake.direction == [0, 1]:
            screen_coords_1[1] -= 1
            screen_coords_2[1] -= 2
            screen_coords_3[1] -= 3
        elif snake.direction == [-1, 0]:
            screen_coords_1[0] += 1
            screen_coords_2[0] += 2
            screen_coords_3[0] += 3

        for fruit in fruits_spawn:
            if snake.body[-1] == fruit[1]:
                ind = fruits_spawn.index(fruit)
                fruits_spawn.pop(ind)
                new_fruit = randint(0, len(food_images) - 1)
                fruits_spawn.append([food_images[new_fruit], create_apple(snake.body)])
                snake.length += 1
                score += 1
                if score % 10 == 0:
                    if scr_k != 3:
                        scr_k -= 1
                        speed += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and keys['up']:
                    snake.direction = [0, -1]
                    keys = {'up': True, 'right': True, 'down': False, 'left': True}
                elif event.key == pygame.K_RIGHT and keys['right']:
                    snake.direction = [1, 0]
                    keys = {'up': True, 'right': True, 'down': True, 'left': False}
                elif event.key == pygame.K_DOWN and keys['down']:
                    snake.direction = [0, 1]
                    keys = {'up': False, 'right': True, 'down': True, 'left': True}
                elif event.key == pygame.K_LEFT and keys['left']:
                    snake.direction = [-1, 0]
                    keys = {'up': True, 'right': False, 'down': True, 'left': True}
                elif event.key == pygame.K_SPACE:
                    game_started = False

        pygame.display.flip()

        while game_started + quit_game == 0:

            b_ground = pygame.Surface((WIN_SIZE * B_SIZE, WIN_SIZE * B_SIZE))
            b_ground.set_alpha(5)
            b_ground.fill((160, 160, 160))
            screen.blit(b_ground, (0, 0))

            render_start = font_arial_26.render('-- press SPASE to START --', 1, pygame.Color('orange'))
            screen.blit(render_start, (WIN_SIZE * B_SIZE // 3, WIN_SIZE * B_SIZE // 2))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_started = True
                elif event.type == pygame.QUIT:
                    quit_game = True

        clock.tick(FPS)
        scr += 1

        if snake.body[-1][0] < 0 or snake.body[-1][0] > (WIN_SIZE - 1) * B_SIZE or snake.body[-1][1] < 0 \
                or snake.body[-1][1] > (WIN_SIZE - 1) * B_SIZE or len(snake.body) != len(set(snake.body)):
            while not quit_game:
                render_game_over = font_arial_60.render('GAME OVER', 1, pygame.Color('orange'))
                screen.blit(render_game_over, (WIN_SIZE * B_SIZE // 3, WIN_SIZE * B_SIZE // 3))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_game = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.quit()
                            main(level)

    pygame.quit()


if __name__ == '__main__':
    main('space')
