import random
import os
import time


def words_from_file(filename):
# считывает слова с файла (создается строка), возвращает список слов
# если файл не найден, то возвращается пустой список, если список пуст, то при вызове функции game() игра будет выводиться "Слова на этот уровень сложности закончились, выберите другой уровень!"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = []
            for line in file:
                words.append(line.strip())
        # Убираем пробелы, поскольку в файле со словами могли быть пробелы, а ответы игроков записываются без пробелов
        return words
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return []

def shuffle_word(word):
# перемешивает буквы в слове (для метода shuffle необходим список), возвращает перемешанное слово
    word_mixed  = list(word)
    random.shuffle(word_mixed)
    shuffled = ''.join(word_mixed).replace(" ", "")
    if shuffled != word:
        return shuffled
    else:
        shuffle_word(word)

def load_ratings(filename):
# загружает рейтинг из файла
    ratings = {}
# создается словарь для хранения рейтинга, имена - ключи, вся остальная информация (в виде словарей) - значения
    if os.path.exists(filename):
# проверяется существование файла
        with open(filename, 'r', encoding='utf-8') as file:
            for each_line in file:
                inf_rating = each_line.strip().split(',')
                name, amount_guessed, lost_games, amount_games, total_time = inf_rating
# в словаре будет хранится имя - name, количество угаданных слов - amount_guessed, количество проигрышей - lost_games, общее количество игр - amount_games, общее время - total_time
                ratings[name] = {'amount_guessed':int(amount_guessed), 'lost_games':int(lost_games), 'amount_games':int(amount_games), 'total_time':float(total_time)}
# словарь-значение для каждого имени
    return ratings

def print_name(filename):
    ratings = load_ratings(filename)
    while True:
        new_player = input("Вы новый игрок или нет? (да/нет): ").lower().strip()
        if new_player == 'да':
            while True:
                name = input("Введите ваше имя: ").strip()
                if name in ratings:
                    print("Имя уже занято. Введите другое имя.")
                elif name:
                    return name
                else:
                    print("Имя не может быть пустым или состоять только из пробелов. Попробуйте снова.")
        elif  new_player == 'нет':
            while True:
                name = input("Введите ваше имя: ").strip()
                if name in ratings:
                    return name
                else:
                    print("Имени не существует:( Введите еще раз.")
        else:
            print("Некорректный ввод. Пожалуйста, введите 'да' или 'нет'.")


def update_rating(filename, name, amount_guessed, lost_games, total_time):
# обновляет рейтинг
    ratings = load_ratings(filename)
# вызов функции, которая возвращает словарь рейтинга
    if name in ratings:
        ratings[name]['amount_guessed'] += amount_guessed # увеличивает количество угаданных слов
        ratings[name]['lost_games'] += lost_games # увеличивает количество проигрышей
        ratings[name]['amount_games'] += 1  # увеличивает общее количество игр
        ratings[name]['total_time'] += total_time  # увеличивает общее время игр
    else:
        ratings[name] = {'amount_guessed': amount_guessed, 'lost_games': lost_games, 'amount_games': 1,
                                'total_time': total_time}
# добавляет информацию нового игрока, если его имя не было найдено в рейтинге (в словаре)

    with open(filename, 'w', encoding='utf-8') as file:
# записывает информацию по игроку в файл
        for name, inf in ratings.items():
            file.write(f"{name},{inf['amount_guessed']},{inf['lost_games']},{inf['amount_games']},{inf['total_time']}\n")

def count_win_rate(name, ratings):
# подсчитывает коэффициент побед
    if name in ratings:
        inf = ratings[name]
# вся информация об игроке - производительность
        if inf['amount_games'] > 0:
            return inf['amount_guessed'] / inf['amount_games'] # рассчитывается доля побед от общего количества игр
    return 0 # если имени нет в рейтинге

def choose_difficulty(players):
# с помощью этой функции выбирается уровень сложности игры
    ratings = load_ratings('rating.txt')
# загружается рейтинг игроков
    win_rates = []
# добавляется долю побед игрока(ов) в список
    games_played = []
# создается список для проверки количества сыгранных игр
    for player in players:
        win_rate = count_win_rate(player, ratings)
        win_rates.append(win_rate)
        if player in ratings:
            games_played.append(ratings[player]['amount_games'])
        else:
            games_played.append(0)
# проверяется возможность выбрать уровень
    low_rating = True
    for win_rate in win_rates:
        if win_rate > 0.5:
            low_rating = False
            break
    if low_rating:
        if len(players) == 1:
            print("Ваш рейтинг низкий, поэтому вы не можете выбрать более высокий уровень:(")
        else:
            print("Оба игрока имеют низкий рейтинг, поэтому вы не можете выбрать более высокий уровень:(")
        return 'easy_words.txt'
    while True:
        difficulty = input("Выберите уровень сложности (1 - легкий; 2 - средний; 3 - сложный): ")
        if difficulty == '1':
            return 'easy_words.txt'
        elif difficulty == '2':
            possible_medium = True
            for i in range(len(players)):
                if win_rates[i] <= 0.5 or games_played[i] < 20:
                    possible_medium = False
                    break
            if possible_medium:
                return 'medium_words.txt'
            else:
                print("Вы не может выбрать средний уровень из-за недостаточно высокого рейтинга:( Попробуйте легкий.")
        elif difficulty == '3':
            possible_hard = True
            for i in range(len(players)):
                if win_rates[i] <= 0.75 or games_played[i] < 30:
                    possible_hard = False
                    break
            if possible_hard:
                return 'hard_words.txt'
            else:
                print("Вы не может выбрать сложный уровень из-за недостаточно высокого рейтинга:( Попробуйте легкий или средний.")
        else:
            print("Некорректный ввод. Пожалуйста, выберите 1 - легкий, 2 - средний, 3 - сложный.")

def game():
    print("Добро пожаловать в игру!")
    players = []
    used_words = set()
# создаем множетство, чтобы слова не повторялись, в нем буду те слова, которые были уже использованы
    ratings = load_ratings('rating.txt')
    while not players:
        amount = input("Хотите играть один или с соперником? (1 - один; 2 - с соперником): ")
        if amount == '1':
            name = print_name('rating.txt')
            players.append(name)
        elif amount == '2':
            for i in range(2):
               name = print_name('rating.txt')
               players.append(name)
        else:
            print("Некорректный ввод. Пожалуйста, выберите 1 или 2")
    while True:
# цикл нужен для того, чтобы продолжить или завершить игру
        words_file = choose_difficulty(players)
        words = words_from_file(words_file)
        attempts = 3
        scores = {}
        for player in players:
            scores[player] = {'amount_guessed': 0, 'lost_games': 0}
# начало отсчета времени
        start_time = time.time()
        for i in range(len(players)):
            player = players[i]
# случайно выбирает слово из списка неиспользованных слов, чтобы для игроков они не повторялись
            filtered_words = []
            for word in words: # из первого списка (первая функция)
                if word not in used_words:
                    filtered_words.append(word)
            if not filtered_words:
                print("\nСлова на этот уровень сложности закончились, выберите другой уровень!")
                break

            word_to_guess = random.choice(filtered_words)
            used_words.add(word_to_guess)
            shuffled_word = shuffle_word(word_to_guess)
            print(f"\nПеремешанное слово для {player}: {shuffled_word}")
            attempts = 3
            player_attempts = attempts
            first_hint_given = False
            while player_attempts > 0:
                guess = input(f"{player}, введите ответ: ").strip()
                if guess == word_to_guess:
                    print("\nПоздравляем! Вы угадали слово!")
                    scores[player]['amount_guessed'] = 1
                    break
                else:
                    player_attempts -= 1
                    if player_attempts == 2:
                        print("У вас осталось 2 попытки.")
                        if not first_hint_given:
                            hint = input("Хотите подсказку (да/нет)? ")
                            if hint.lower() == 'да':
                                print(f"Подсказка: первая буква слова - {word_to_guess[0]}")
                                first_hint_given = True
                    elif player_attempts == 1:
                        print("У вас осталась 1 попытка.")
                        if not first_hint_given:
                            hint = input("Хотите подсказку (да/нет)? ")
                            if hint.lower() == 'да':
                                print(f"Подсказка: первая буква слова - {word_to_guess[0]}")
                                first_hint_given = True
                        else:
                            hint = input("Хотите подсказку (да/нет)? ")
                            if hint.lower() == 'да':
                                print(f"Подсказка: последняя буква слова - {word_to_guess[-1]}")
            if scores[player]['amount_guessed'] == 0:
                print(f"\nВы проиграли:( В следующий раз точно повезет! Загаданное слово: {word_to_guess}")
                scores[player]['lost_games'] += 1
        end_time = time.time()
        total_time = end_time - start_time
        for player in players:
            update_rating('rating.txt', player, scores[player]['amount_guessed'], scores[player]['lost_games'], total_time)
# определение победителя если играли двое
        if len(players) == 2:
            if scores[players[0]]['amount_guessed'] > scores[players[1]]['amount_guessed']:
                print(f"\nИтог игры")
                print(f"Победитель - {players[0]}")
                print(f"Проигравший - {players[1]}")
            elif scores[players[0]]['amount_guessed'] < scores[players[1]]['amount_guessed']:
                print(f"\nИтог игры")
                print(f"Победитель - {players[1]}")
                print(f"Проигравший - {players[0]}")
            else:
                print(f"\nИтог игры")
                print("Ничья!")
        play_again = input("\nХотите сыграть еще раз (да/нет)? ").strip().lower()
        if play_again != 'да':
            print("\nСпасибо за игру! До свидания!")
            break

game()
