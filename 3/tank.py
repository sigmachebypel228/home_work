

from hitbox import Hitbox
from tkinter import *
from random import randint
import world

# 5 теперь изображения танков будут грузиться из модуля texture
import texture as skin


# 6 внесем изменния в инициализатор
class Tank:
    __count = 0

    def __init__(self, canvas, x, y,model = 'Т-14 Армата',
                 ammo = 100, speed = 10,
                 # file_up = '../img/tankT34_up.png',
                 # file_down = '../img/tankT34_down.png',
                 # file_left = '../img/tankT34_left.png',
                 # file_right = '../img/tankT34_right.png',

                 bot = True):
        self.__bot = bot
        self.__target = None
        # self.__skin_up = PhotoImage(file = file_up)
        # self.__skin_down = PhotoImage(file = file_down)
        # self.__skin_left = PhotoImage(file = file_left)
        # self.__skin_right = PhotoImage(file = file_right)
        Tank.__count += 1
        self.__hitbox = Hitbox(x, y, self.get_size(), self.get_size(), padding=1)
        self.__canvas = canvas
        self.__model = model
        self.__hp = 100
        self.__xp = 0
        self.__ammo = ammo
        self.__fuel = 10000
        self.__speed = speed
        self.__x = x
        self.__y = y
        self.__vx = 0
        self.__vy = 0
        self.__dx = 0
        self.__dy = 0
        if self.__x < 0:
            self.__x = 0
        if self.__y < 0:
            self.__y = 0

        self.__create()
        self.right()

        print(self)
    def __check_map_collision(self):
        result = self.__hitbox.check_map_collision()
        if result:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()

    def set_target(self, target):
        self.__target = target

    def __AI_goto_target(self):
        if randint(1,2) == 1:
            if self.__target.get_x() < self.get_x():
                self.left()
            else:
                self.right()
        else:
            if self.__target.get_y() < self.get_y():
                self.forvard()
            else:
                self.backward()

    def __AI(self):
        if randint(1,30) == 1:
            if randint(1,10) < 9 and self.__target is not None:
                self.__AI_goto_target()
            else:
                self.__AI_change_orientation()

    def __AI_change_orientation(self):
        rand = randint(0, 3)
        if rand == 0:
            self.left()
        if rand == 1:
            self.forvard()
        if rand == 2:
            self.right()
        if rand == 3:
            self.backward()

    def fire(self):
        if self.__ammo > 0:
            self.__ammo -= 1
            print('стреляю')


# 7 Установить текстуры при смене напрвлений
    def forvard(self):
        self.__vx = 0
        self.__vy = -1
        self.__canvas.itemconfig(self.__id,
                                 image = skin.get('tank_up'))

    def backward(self):
        self.__vx = 0
        self.__vy = 1
        self.__canvas.itemconfig(self.__id,
                                 image = skin.get('tank_down'))

    def left(self):
        self.__vx = -1
        self.__vy = 0
        self.__canvas.itemconfig(self.__id,
                                 image = skin.get('tank_left'))

    def right(self):
        self.__vx = 1
        self.__vy = 0
        self.__canvas.itemconfig(self.__id,
                                 image = skin.get('tank_right'))

    def stop(self):
        self.__vx = 0
        self.__vy = 0
        self.__undo_move()

    def update(self):
        if self.__fuel > self.__speed:
            if self.__bot:
                self.__AI()

            self.__dx = self.__vx * self.__speed
            self.__dy = self.__vy * self.__speed
            self.__x += self.__dx
            self.__y += self.__dy
            self.__fuel -=self.__speed

            self.__update_hitbox()
            self.__chek_out_of_world()
            self.__check_map_collision()
            self.__repaint()


    def __undo_move(self):
        if self.__dx == 0 and self.__dy == 0:
            return
        self.__x -= self.__dx
        self.__y -= self.__dy
        self.__update_hitbox()
        self.__repaint()
        self.__dx = 0
        self.__dy = 0

# 8 Изменим код создания изображения на холсте
    def __create(self):
        self.__id = self.__canvas.create_image(self.__x, self.__y,
                                               image = skin.get('tank_up'), anchor ='nw')

    def __repaint(self):
        self.__canvas.moveto(self.__id,
                             x = world.get_screen_x(self.__x),
                             y = world.get_screen_y(self.__y))

    def __update_hitbox(self):
        self.__hitbox.moveto(self.__x, self.__y)

    def intersects(self, other_tank):
        value = self.__hitbox.intersects(other_tank.__hitbox)
        if value:
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()
        return value

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_ammo(self):
        return self.__ammo

    def get_model(self):
        return self.__model

    def get_hp(self):
        return self.__hp

    def get_xp(self):
        return self.__xp

    def get_fuel(self):
        return self.__fuel

    def get_speed(self):
        return self.__speed

    @staticmethod
    def grt_quantity():
        return Tank.__count

# 9 Получить размеры изображения через skin
    def get_size(self):
        # return self.__skin_up.width()
        return skin.get('tank_up').width()

    def __chek_out_of_world(self):
        if self.__hitbox.left < 0 or \
                self.__hitbox.top < 0 or \
                self.__hitbox.right >= world.get_width() or \
                self.__hitbox.bottom >= world.get_height():
            self.__undo_move()
            if self.__bot:
                self.__AI_change_orientation()


    def __del__(self):
        print(f'удален танк')
        try:
            self.__canvas.delete(self.__id)
        except Exception:
            pass

    def __str__(self):
        return (f'координаты: x = {self.__x}, y = {self.__y}, модель: {self.__model}, '
                f'здоровье: {self.__hp}, опыт: {self.__xp}, боеприпасы: {self.__ammo}')
