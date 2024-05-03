# Создаем игровое поле
board = [' ' for _ in range(9)]
# Функция для отображения игрового поля
def print_board():
    print("-------------")
    for i in range(3):
        print("|", board[i * 3], "|", board[i * 3 + 1], "|", board[i * 3 + 2], "|")
        print("-------------")
# Функция для хода игрока
def player_move():
    valid_move = False
    while not valid_move:
        move = input("Выберите пустую ячейку для вашего хода (1-9): ")
        move = int(move) - 1
        if move >= 0 and move < 9 and board[move] == ' ':
            board[move] = 'X'
            valid_move = True
        else:
            print("Некорректный ход. Попробуйте еще раз.")
# Функция для хода бота
def bot_move():
    valid_move = False
    while not valid_move:
        import random
        move = random.randint(0, 8)
        if board[move] == 'X':
            board[move] = 'O'
            valid_move = True
# Функция для проверки победителя
def check_winner():
    winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != ' ':
            return board[combination[0]]
    if 'X' not in board:
        return "Ничья"
    return None
# Основной игровой цикл
def play_game():
    print("Игра началась! Используйте цифры от 1 до 9 для выбора пустой ячейки.")
    print_board()
    winner = None
    while not winner:
        player_move()
        print_board()
        winner = check_winner()
        if winner:
            break
        bot_move()
        print_board()
        winner = check_winner()
    print("Игра окончена.")
    if winner == "Ничья":
        print("Ничья")
    else:
        print("Победитель:", winner)
# Запускаем игру
play_game()

