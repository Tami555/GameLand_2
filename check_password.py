"""Функции для создания качественного пароля"""
from string import ascii_uppercase, ascii_lowercase


class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


def long_and_num(parol):
    if len(parol) < 9:
        raise LengthError()
    if not any([x in list('1234567890') for x in parol]):
        raise DigitError()
    return True


def minus(lst):
    a, b, c = lst
    return abs(a - b) == 1 and abs(b - c) == 1


def letters(parol):
    lst_e_b = ascii_uppercase
    lst_e_l = ascii_lowercase

    lst_r_l = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    lst_r_b = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    if (any(x in parol for x in lst_e_b) or any(x in parol for x in lst_r_b)) and \
            (any(x in parol for x in tuple(lst_e_l)) or any(x in parol for x in tuple(lst_r_l))):
        return True
    raise LetterError()


def check_password(password):
    try:
        long_and_num(password)
        letters(password)

        return True
    except LengthError:
        return 'The password must be at least 9 characters long.'
    except DigitError:
        return 'The password must contain numbers.'
    except LetterError:
        return "The password contains all characters of the same case."