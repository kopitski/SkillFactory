M = [["-" for j in range(3)] for i in range(3)]

pobeda = False
cnt = 1 #Счетчик ходов

def check_X(M): # Проверка условий победы игрока Х
    if M[0][0] == "X" and M[0][1] == "X" and M[0][2] == "X" or M[1][0] == "X" and M[1][1] == "X" and M[1][2] == "X":
        return True
    elif M[2][0] == "X" and M[2][1] == "X" and M[2][2] == "X" or M[0][0] == "X" and M[1][1] == "X" and M[2][2] == "X":
        return True
    elif M[0][2] == "X" and M[1][1] == "X" and M[2][0] == "X":
        return True
    return False

def check_O(M): # Проверка условий победы игрока О
    if M[0][0] == "O" and M[0][1] == "O" and M[0][2] == "O" or M[1][0] == "O" and M[1][1] == "O" and M[1][2] == "O":
        return True
    elif M[2][0] == "O" and M[2][1] == "O" and M[2][2] == "O" or M[0][0] == "O" and M[1][1] == "O" and M[2][2] == "O":
        return True
    elif M[0][2] == "O" and M[1][1] == "O" and M[2][0] == "O":
        return True
    return False

while not pobeda:
    if cnt % 2 == 1:
        print("******************************\n")
        for i in M:
            print(' '.join(map(str, i)))
        print("Первый игрок (X)")
        i = int(input("Выберите ряд: "))
        j = int(input("Выберите столбец: "))

        test = False
        while test == False: #Проверяем i и j
            while i < 0 or i > 2:
                i = int(input("Заново выберите ряд: "))
            while j < 0 or j > 2:
                j = int(input("Заново выберите столбец: "))
            while M[i][j] != "-":  # Если место уже занято
                i = int(input("Заново выберите ряд: "))
                j = int(input("Заново выберите столбец: "))
            test = True

        M[i][j] = "X" #Вносим Х

        if check_X(M):
            print("Первый игрок выиграл")
            pobeda = True
            for i in M:
                print(' '.join(map(str, i)))
        else:
            cnt += 1

    elif cnt % 2 == 0:
        for i in M:
            print(' '.join(map(str, i)))
        print("Второй игрок (O)")
        i = int(input("Выберите ряд: "))
        j = int(input("Выберите столбец: "))
        test = False
        while test == False: #Проверяем i и j
            while i < 0 or i > 2:
                i = int(input("Заново выберите ряд: "))
            while j < 0 or j > 2:
                j = int(input("Заново выберите столбец: "))
            while M[i][j] != "-":  # Если место уже занято
                i = int(input("Заново выберите ряд: "))
                j = int(input("Заново выберите столбец: "))
            test = True

        M[i][j] = "O" #Вносим О

        if check_O(M):
            print("Второй игрок выиграл")
            pobeda = True
            for i in M:
                print(' '.join(map(str, i)))
        else:
            cnt += 1
    if cnt == 10: #Условие при котором никто не выиграл
        break
if cnt == 10:
    print("Никто не выиграл...")