import pygame
import sys
import os

FPS = 50
pygame.init()
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None
    
    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, 
                                       tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(mario_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
                tile_width * pos_x + 15,
                tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)
    
    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
                tile_width * self.pos[0] + 15,
                tile_height * self.pos[1] + 5)

player = None
running = True
clock = pygame.time.Clock()
sprite_group = pygame.sprite.Group()
mario_group =pygame.sprite.Group()
def terminate():
    pygame.quit()
    sys.exit()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
# вернем игрока, а также размер поля в клетках
    return new_player, x, y

def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (tile_width,
tile_height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1,
pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord += 10
    intro_rect.top = text_coord
    intro_rect.x = 10
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

def move(mario, movement):
    x, y = mario.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            mario.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            mario.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            mario.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            mario.move(x + 1, y)

start_screen()
level_map = load_level('map.map')
mario, max_x, max_y = generate_level(level_map)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(mario, 'up')
            elif event.key == pygame.K_DOWN:
                move(mario, 'down')
            elif event.key == pygame.K_LEFT:
                move(mario, 'left')
            elif event.key == pygame.K_RIGHT:
                move(mario, 'right')
    screen.fill(pygame.Color('black'))
    sprite_group.draw(screen)
    mario_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()