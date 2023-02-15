from random import randint

# класс точки поля, сравнения двух точек
# и метод для отображения точек
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

# Исключения
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы выстрелилили за пределы игрового поля! " \
               "Попробуйте ещё раз!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "В эту клетку уже стреляли!" \
               "Попробуйте ещё раз!"

class BoardWrongShipException(BoardException):
    pass

# класс Корабль, длина, нос корабля, ориентация на игровом поле
# количество жизней = длина корабля

class Ship:
    def __init__(self, bow_ship, length, orient):
        self.bow_ship = bow_ship
        self.length = length
        self.orient = orient
        self.lives = length

# Создаем метод-свойство, который будет в списке хранить точки корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            current_x = self.bow_ship.x
            current_y = self.bow_ship.y

            if self.orient == 0:
                current_x += i

            elif self.orient == 1:
                current_y += i

            ship_dots.append(Dot(current_x, current_y))

        return ship_dots

# Игровое поле
class Board:
    def __init__(self, hidden = False, size = 6):
        self.size = size
        self.hidden = hidden

        self.count = 0  # кол-во пораженных кораблей

        self.field =[['O'] * size for _ in range(size)]  # сетка 0

        self.busy = []  # список занятых точек
        self.ships = []  # список кораблей доски

# Расстановка корабля. Проверяем точки корабля, не выходят ли за границы игрового поля и не заняти ли уже
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

# Контур корабля, чтобы точки кораблей не пересекались
    def contour(self, ship, verb = False):
        # список всех точек вокруг корабля
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)
                ]
        # Все соседние точки (вверх/вниз/по диагонали)
        for d in ship.dots:
            for dx, dy in near:
                current = Dot(d.x + dx, d.y + dy)
                if not(self.out(current)) and current not in self.busy:
                    if verb:
                        self.field[current.x][current.y] = "."
                    self.busy.append(current)

# Игровое поле
    def __str__(self):
        res = ''
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        # Используем ф-ю enumerate и начинаем отсчет с 1
        for i, row in enumerate(self.field, 1):
            res += f"\n{i} | " + " | ".join(row) + " |"

        if self.hidden:
            res = res.replace('■', 'O')
        return res

# Проверка по координатам, корабль находится в игровом поле
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

# Стрельба, попадает ли точка в поле и не занята ли она
# если не занята,  добавляем в занятые и проверяем не попала ли она в корабль
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True

        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []  # обнуляем список

# Игрок
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class Ai(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d

# Вносим координаты и проверяем, внесли ли 2 координаты длиной 1 символ
class User(Player):
    def ask(self):
        while True:
            coordinates = input('Введите координаты: ').split()

            if len(coordinates) != 2:
                print('Введите x и y координаты через пробел')
                continue

            x, y = coordinates

            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите целые числа')
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

# Игра
class Game:
    # Устанавливаем размер поля
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        comp = self.random_board()
        comp.hidden = True

        self.ai = Ai(comp, pl)
        self.us = User(pl, comp)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
# Размещаем корабли
    def random_place(self):
        all_ships = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for length in all_ships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board


    def greet(self):
        print('      Добро пожаловать   ')
        print('           в игру      ')
        print('        МОРСКОЙ БОЙ   ')
        print('-'*27)
        print('формат ввода – целые числа ')
        print('     через пробел    ')
        print(' x – по горизонтали')
        print(' у – по вертикали  ')
        print('-'*27)

    def loop(self):
        num = 0
        while True:
            print('~'*27)
            print('Игровое поле игрока: ')
            print(self.us.board)
            print('~'*27)
            print('Игровое поле компьютера: ')
            print(self.ai.board)
            print('~'*27)
            if num % 2 == 0:
                print('Ваш ход!')
                repeat = self.us.move()
            else:
                print('Ход компьютера')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print('~'*27)
                print('ВЫ ПОБЕДИЛИ!')
                break

            if self.us.board.count == 7:
                print('~'*27)
                print('ВЫ ПРОИГРАЛИ!')
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()