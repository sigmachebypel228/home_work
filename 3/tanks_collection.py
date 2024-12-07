# Спавним больше танков
from random import randint
from tank import Tank
import world

_tanks = []
_canvas = None


def initialize(canv):
    global _canvas
    _canvas = canv
    player = Tank(canvas = canv, x = world.BLOCK_SIZE*2, y = world.BLOCK_SIZE*4, ammo = 100, speed=5, bot = False)
    enemy = Tank(canvas = canv, x = world.BLOCK_SIZE*4, y = world.BLOCK_SIZE*6, ammo = 100, speed=5, bot = True)
    enemy.set_target(player)

    _tanks.append(player)
    _tanks.append(enemy)


def get_player():
    return _tanks[0]

def update():
    for tank in _tanks:
        tank.update()
        check_collision(tank)


def check_collision(tank):
    for other_tank in _tanks:
        if tank == other_tank:
            continue
        if tank.intersects(other_tank):
            return True
    return False

# 1 добавим больше танков вызывать будем по нажатию на пробел в основном модуле
def spawn_enemy():
    pos_x = randint(200, world.WIDTH - 200)
    pos_y = randint(200, world.HEIGHT - 200)

    # для тестирования зададим видимые координаты и добавим в модуль tank в момень создания такнка print(self)
    # pos_x = randint(200, 800)
    # pos_y = randint(200, 600)

    t = Tank(_canvas, x=pos_x, y=pos_y, speed=10)


    t.set_target(get_player())
    _tanks.append(t)

# 2 перепишем функцию spawn_enemy() так чтобы танк спавнился только если не пересекается с другим танком
def spawn_enemy():
    while True:
        pos_x = randint(200, 800)
        pos_y = randint(200, 600)

        t = Tank(_canvas, x=pos_x, y=pos_y, speed=1)
        if not check_collision(t):
            t.set_target(get_player())
            _tanks.append(t)
            return True






