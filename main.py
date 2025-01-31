import secrets
import string
import msvcrt
import os
import sys

SPECIAL_CHARS = "~!@#$%_"


def get_wordlist_path():
    if getattr(sys, 'frozen', False):
        # Если скрипт запущен из исполняемого файла PyInstaller
        basedir = sys._MEIPASS
    else:
        # Если скрипт запущен обычным образом из .py файла
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, 'share', 'eff_large.wordlist')


WORDLIST_PATH = get_wordlist_path()


def generate_random_password(length):
    characters = string.ascii_letters + string.digits + SPECIAL_CHARS
    return ''.join(secrets.choice(characters) for _ in range(length))


def enhance_character(char, transformed, password):
    enhancements = {
        'a': '@', 'A': '4', 'e': '3', 'E': '3', 'i': '1', 'I': '!',
        'o': '0', 'O': '0', 's': '5', 'S': '$',
        't': '7', 'T': '7', 'b': '8', 'B': '8', 'g': '9', 'G': '6',
        ' ': '', 'l': '|'
    }
    if char in string.punctuation and char not in enhancements:
        available_chars = [c for c in SPECIAL_CHARS if c not in password]
        if not available_chars:
            return secrets.choice([char] + list(SPECIAL_CHARS))
        return secrets.choice(available_chars)
    if char not in transformed and char in enhancements:
        transformed.add(char)
        return enhancements[char]
    return char


def ensure_password_requirements(password):
    if not any(char.islower() for char in password):
        idx = secrets.choice([i for i, c in enumerate(password) if c.isupper()])
        password[idx] = password[idx].lower()
    if not any(char.isupper() for char in password):
        idx = secrets.choice([i for i, c in enumerate(password) if c.islower()])
        password[idx] = password[idx].upper()
    if not any(char.isdigit() for char in password):
        password.append(secrets.choice(string.digits))
    if not any(char in SPECIAL_CHARS for char in password):
        password.append(secrets.choice(SPECIAL_CHARS))
    return "".join(password)


def convert_phrase_to_password(phrase):
    transformed = set()
    phrase = "".join(phrase.split())
    enhanced_chars = []
    for char in phrase:
        enhanced_chars.append(enhance_character(char, transformed, enhanced_chars))
    secure_password = ensure_password_requirements(enhanced_chars)
    return secure_password


def load_wordlist(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]


def generate_passphrase(num_words=1, case='camel', separator=''):
    wordlist = load_wordlist(WORDLIST_PATH)
    words = [secrets.choice(wordlist) for _ in range(num_words)]
    if case == 'upper':
        words = [word.upper() for word in words]
    elif case == 'camel':
        words = [word.capitalize() for word in words]
    elif case == 'inverted':
        words = [word[0].lower() + word[1:].upper() for word in words]
    return separator.join(words)


def main():
    mode = input(
        "Выберите режим работы программы (1 - рандомная генерация, 2 - преобразование строки, 3 - генерация парольной фразы): ")
    if mode == '1':
        length = int(input("Введите желаемую длину пароля: "))
        password = generate_random_password(length)
    elif mode == '2':
        phrase = input("Введите строку для преобразования в пароль: ")
        password = convert_phrase_to_password(phrase)
    elif mode == '3':
        num_words = int(input("Введите количество слов в парольной фразе: "))
        print("Выберите регистр для слов (по-умолчанию каждое слово с заглавной буквы):")
        print("1 - только нижний регистр")
        print("2 - только верхний регистр")
        print("3 - каждое слово с заглавной буквы")
        print("4 - первая буква слова строчная, остальное слово в верхнем регистре")
        case_choice = input("Ваш выбор (1-4): ")
        case_options = {'1': 'lower', '2': 'upper', '3': 'camel', '4': 'inverted'}
        case = case_options.get(case_choice, 'camel')
        separator = input("Введите символ для разделения слов (по-умолчанию без пробелов): ")
        password = generate_passphrase(num_words, case, separator)
    else:
        raise ValueError("Неверно указан режим работы программы.")
    print("Сгенерированный пароль:", password)
    print("Нажмите любую клавишу для выхода...")
    msvcrt.getch()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("Нажмите любую клавишу для выхода...")
        msvcrt.getch()
