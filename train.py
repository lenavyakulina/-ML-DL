import argparse
import sys
import re
from collections import defaultdict
import os
import pickle

r_alphabet = re.compile(u'[а-яА-Яa-zA-Z]+')

# Реализация консольного интерфейса:


def deal_with_console():
    """
    Считывание аргументов из консоли
    :return: доступ к ним
    """
    parser = argparse.ArgumentParser(description='Создание модели текста.',
                                     prog='train', fromfile_prefix_chars='@')
    parser.add_argument('--input', '--input-dir', action='store',
                        help='Путь к директории, в которой лежит'
                        'коллекция документов. '
                        'Если данный аргумент не задан, считается, '
                        'что тексты вводятся из stdin.',
                        default=False)
    parser.add_argument('--model', action='store',
                        help='Путь к файлу, в который сохраняется модель.',
                        default=False)

    return parser.parse_args()

# Введение строк из stdin:


def gen_lines_from_stdin(args):
    """
    Получение строк из текста, введённого из stdin(консоли).
    Приведение к lowercase.
    :param args: то, что ввели в консоли
    :return: строки
    """
    for line in sys.stdin:
        yield line.lower()

# Получение строк из файлов в директории:


def gen_lines_from_directory(args):
    """
    Получение строк из файлов, которые находятся
    в указанной пользователем директории.
    Приведение к lowercase.
    :param args: то, что ввели в консоли
    :return: строки
    """
    directory = os.listdir(args.input)
    for file in directory:
        f = open(os.path.join(args.input, file), 'r')
        for line in f:
            yield line.lower()

# Очистить текст: выкинуть неалфавитные символы. Токенизация:


def gen_tokens(lines):
    """
    :rtype: gen_tokens
    Возвращает очищенные от неалфавитных символов слова из строк
    """
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

# Сгенерировать биграммы:


def gen_bigrams(tokens):
    """
    :param tokens:
    Генератор пар слов (предыдущее-последующее)
    :return: пара
    """
    t1 = '$'
    for t2 in tokens:
        if t1 != '$':
            yield t1, t2
        t1 = t2

# Создание модели:


def train_itself():
    """
    Функция, создающая словарь (model),
    где ключ - слово,
    а значение - пара (следующее слово + частота встречаемости пары)
    :return:
    """
    args = deal_with_console()
    if not args.model:
        print('Пожалуйста, запустите программу ещё раз '
              'и укажите название файла, в который '
              'нужно сохранить модель')
        sys.exit()

    g = open(args.model, 'wb')
    if args.input:
        lines = gen_lines_from_directory(args)
    else:
        lines = gen_lines_from_stdin(args)

    tokens = gen_tokens(lines)
    b_grams = gen_bigrams(tokens)
    bi = defaultdict(int)

    for word0, word1 in b_grams:
        bi[word0, word1] += 1

    model = defaultdict(set)
    for word0, word1 in bi.keys():
        model[word0].add((word1, bi[word0, word1]))

    pickle.dump(model, g)

# Вызов функций:


if __name__ == '__main__':
    train_itself()
