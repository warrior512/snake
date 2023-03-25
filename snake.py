import pygame
from random import randint


B_SIZE = 40
WIN_SIZE = 25
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def create_snake():
    return [(randint(0, WIN_SIZE - 1)*B_SIZE, randint(0, WIN_SIZE - 1)*B_SIZE)]


def create_apple(snake_coordinates):
    apple_coordinates = randint(0, WIN_SIZE - 1) * B_SIZE, randint(0, WIN_SIZE - 1) * B_SIZE
    if apple_coordinates in snake_coordinates:
        create_apple(snake_coordinates)
    return randint(0, WIN_SIZE - 1) * B_SIZE, randint(0, WIN_SIZE - 1) * B_SIZE


def game_over():
    print('game over')


def main():
    pygame.init()
    fps = 6
    score = 0
    speed = 1
    font_info = pygame.font.SysFont('Arial', 26, bold=True)
    font_game_over = pygame.font.SysFont('Arial', 60, bold=True)

    snake = create_snake()
    apple = create_apple(snake)
    snake_length = 1
    dx, dy = 1, 0
    keys = {'up': True, 'right': False, 'down': True, 'left': True}

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_SIZE * B_SIZE, WIN_SIZE * B_SIZE))
    pygame.display.update()
    pygame.display.set_caption('Snake')
    apple_image = pygame.image.load('apple.png')
    fon_image = pygame.image.load('fon.jpg')

    img_body_horizontal = pygame.image.load('body_horizontal.png')
    img_body_vertical = pygame.image.load('body_vertical.png')
    img_body_left_top = pygame.image.load('body_left_top.png')
    img_body_right_top = pygame.image.load('body_right_top.png')
    img_body_left_bot = pygame.image.load('body_left_bot.png')
    img_body_right_bot = pygame.image.load('body_right_bot.png')
    img_head_up = pygame.image.load('head_up.png')
    img_head_right = pygame.image.load('head_right.png')
    img_head_down = pygame.image.load('head_down.png')
    img_head_left = pygame.image.load('head_left.png')
    img_tail_up = pygame.image.load('tail_up.png')
    img_tail_right = pygame.image.load('tail_right.png')
    img_tail_down = pygame.image.load('tail_down.png')
    img_tail_left = pygame.image.load('tail_left.png')

    quit_game = False
    while not quit_game:
        screen.fill(pygame.Color('black'))
        screen.blit(fon_image, (0, 0))

        sprites = []
        snake_coords = snake[::-1]
        for coords in snake_coords:
            if coords == snake_coords[0]:
                if dx == 0 and dy == -1:
                    sprites.append((img_head_up, coords))
                elif dx == 1 and dy == 0:
                    sprites.append((img_head_right, coords))
                elif dx == 0 and dy == 1:
                    sprites.append((img_head_down, coords))
                elif dx == -1 and dy == 0:
                    sprites.append((img_head_left, coords))
            if len(snake_coords) > 2 and coords != snake_coords[-1] and coords != snake_coords[0]:
                cur_index = snake_coords.index(coords)
                if snake_coords[cur_index + 1][0] == coords[0] and snake_coords[cur_index - 1][0] == coords[0]:
                    sprites.append((img_body_vertical, coords))
                elif snake_coords[cur_index + 1][1] == coords[1] and snake_coords[cur_index - 1][1] == coords[1]:
                    sprites.append((img_body_horizontal, coords))
                if coords[0] + 1 * B_SIZE == snake_coords[cur_index + 1][0] and coords[1] + 1 * B_SIZE == snake_coords[cur_index - 1][1] \
                        or coords[1] + 1 * B_SIZE == snake_coords[cur_index + 1][1] and coords[0] + 1 * B_SIZE == snake_coords[cur_index - 1][0]:
                    sprites.append((img_body_left_top, coords))
                elif coords[1] + 1 * B_SIZE == snake_coords[cur_index + 1][1] and coords[0] - 1 * B_SIZE == snake_coords[cur_index - 1][0] \
                        or coords[0] - 1 * B_SIZE == snake_coords[cur_index + 1][0] and coords[1] + 1 * B_SIZE == snake_coords[cur_index - 1][1]:
                    sprites.append((img_body_right_top, coords))
                elif coords[0] + 1 * B_SIZE == snake_coords[cur_index + 1][0] and coords[1] - 1 * B_SIZE == snake_coords[cur_index - 1][1] \
                        or coords[1] - 1 * B_SIZE == snake_coords[cur_index + 1][1] and coords[0] + 1 * B_SIZE == snake_coords[cur_index - 1][0]:
                    sprites.append((img_body_left_bot, coords))
                elif coords[1] - 1 * B_SIZE == snake_coords[cur_index + 1][1] and coords[0] - 1 * B_SIZE == snake_coords[cur_index - 1][0] \
                        or coords[0] - 1 * B_SIZE == snake_coords[cur_index + 1][0] and coords[1] - 1 * B_SIZE == snake_coords[cur_index - 1][1]:
                    sprites.append((img_body_right_bot, coords))
            if coords == snake_coords[-1] and len(snake_coords) != 1:
                if snake_coords[-2][0] + 1 * B_SIZE == coords[0] and snake_coords[-2][1] == coords[1]:
                    sprites.append((img_tail_right, coords))
                elif snake_coords[-2][0] == coords[0] and snake_coords[-2][1] - 1 * B_SIZE == coords[1]:
                    sprites.append((img_tail_up, coords))
                elif snake_coords[-2][0] - 1 * B_SIZE == coords[0] and snake_coords[-2][1] == coords[1]:
                    sprites.append((img_tail_left, coords))
                elif snake_coords[-2][0] == coords[0] and snake_coords[-2][1] + 1 * B_SIZE == coords[1]:
                    sprites.append((img_tail_down, coords))

        for sprite in sprites:
            sprite, coordinates = sprite
            screen.blit(sprite, coordinates)

        screen.blit(apple_image, apple)
        render_score = font_info.render(f'SCORE: {score}', 1, pygame.Color('orange'))
        render_speed = font_info.render(f'SPEED: {speed}', 1, pygame.Color('orange'))
        screen.blit(render_score, (5, 5))
        screen.blit(render_speed, (5, 50))

        snake.append((snake[-1][0] + dx * B_SIZE, snake[-1][1] + dy * B_SIZE))
        snake = snake[-snake_length:]

        if snake[-1] == apple:
            apple = create_apple(snake)
            snake_length += 1
            score += 1
            if score % 5 == 0:
                fps += 1
                speed += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and keys['down']:
                    dx, dy = 0, -1
                    keys = {'up': False, 'right': True, 'down': True, 'left': True}
                elif event.key == pygame.K_RIGHT and keys['left']:
                    dx, dy = 1, 0
                    keys = {'up': True, 'right': False, 'down': True, 'left': True}
                elif event.key == pygame.K_DOWN and keys['up']:
                    dx, dy = 0, 1
                    keys = {'up': True, 'right': True, 'down': False, 'left': True}
                elif event.key == pygame.K_LEFT and keys['right']:
                    dx, dy = -1, 0
                    keys = {'up': True, 'right': True, 'down': True, 'left': False}
        pygame.display.flip()
        clock.tick(fps)

        if snake[-1][0] < 0 or snake[-1][0] > (WIN_SIZE - 1) * B_SIZE or snake[-1][1] < 0 \
                or snake[-1][1] > (WIN_SIZE - 1) * B_SIZE or len(snake) != len(set(snake)):
            while not quit_game:
                render_game_over = font_game_over.render('GAME OVER', 1, pygame.Color('orange'))
                screen.blit(render_game_over, (WIN_SIZE * B_SIZE // 3, WIN_SIZE * B_SIZE // 3))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_game = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.quit()
                            main()
    pygame.quit()


if __name__ == '__main__':
    main()
