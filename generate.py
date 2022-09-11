import argparse
import sys
import random
import pickle

# Реализация консольного интерфейса:


def deal_with_console():
    """
    Считывание аргументов из консоли
    :return: доступ к ним
    """
    parser = argparse.ArgumentParser(description='Генерация текста',
                                     prog='generate',
                                     fromfile_prefix_chars='@')
    parser.add_argument('--length', action='store',
                        help='Длина генерируемой последовательности',
                        default=False)
    parser.add_argument('--model', action='store',
                        help='Путь к файлу, из которого загружается модель',
                        default=False)
    parser.add_argument('--prefix', action='store', default=False,
                        help='Начало предложения (одно слово). '
                        'Если не указано, выбираем '
                             'случайно из всех слов')
    parser.add_argument('--output', action='store', default=False,
                        help='Файл, в который будет записан результат. '
                             'Если аргумент отсутствует, выводить в stdout.')

    return parser.parse_args()

# Проверка введённых данных:


def check_console(args):
    """
    Функция проверяет, указали ли в консоли модель для генерации
    текста и длину генерируемого текста
    :param args: то, что ввели в консоли
    :return: если проверка пройдена, вернет пару (модель - первое слово текста)
    """
    if not args.model:
        print('Пожалуйста, укажите файл, из которого нужно загрузить модель!')
        sys.exit()

    if not args.length:
        print('Пожалуйста, укажите длину последовательности!')
        sys.exit()

    f = open(args.model, 'rb')
    model = pickle.load(f)
    f.close()

    startword = ""
    if args.prefix:
        startword = args.prefix
    else:
        startword = random.choice([k for k in model.keys()])
    return model, startword

# Генерация текста:


def generation_itself():
    """
    Функция, генерирующая текст по его длине и модели для него
    """
    args = deal_with_console()
    model, word = check_console(args)

    if args.output:
        g = open(args.output, 'w')

    ans = ''
    for j in range(int(args.length)):
        if args.output:
            g.write(word + ' ')
        else:
            ans += word + ' '
        loc = []
        for elem in model[word]:
            for num in range(elem[1]):
                loc.append(elem[0])
        word = random.choice(loc)

    if args.output:
        g.close()
    else:
        print(ans)

# Вызов функций:

if __name__ == "__main__":
    generation_itself()
