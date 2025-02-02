import sqlite3
file_user = "C:\\Users\\Tami\\Desktop\\New_Game\\now_user.txt"
database = sqlite3.connect('C:\\Users\\Tami\\Desktop\\New_Game\\GameLand_db.sql')
cur = database.cursor()


def user():
    """ Для чтения текущего пользователя"""
    with open(file_user, 'r', encoding='utf-8') as file:
        line = file.readline()
        if line != '':
            return line.split(';')[1]
        return None


def create_now_user(data=''):
    """Для записи на компьютер (в файл) текущего пользователя. (Без повторной регистрации)"""
    with open(file_user, 'w', encoding='utf-8') as file:
        if isinstance(data, (list, tuple)):
            file.write(';'.join(map(str, data)))
        else:
            pass


def get_infa(password=None):
    """Проверяет наличие пользователя в БД по паролю"""
    if password is None:
        password = user()
    req = """SELECT * FROM users WHERE Password = ?"""
    result = cur.execute(req, (password,)).fetchone()
    return [str(x) for x in result] if result is not None else None


def update_result_DB(column, value, password=None):
    """Обновляет данные в БД (о пользователе, рекордах и т.д) по паролю"""
    if password is None:
        password = user()
    query = f"""UPDATE users SET {column} = ? WHERE Password = ?"""
    cur.execute(query, (value, password))
    database.commit()


def current_record(game):
    """Получаем текущий рекорд по игре(game)"""
    password_user = user()
    query = f"""SELECT {game} FROM users WHERE Password = ?"""
    result = cur.execute(query, (password_user,)).fetchone()
    print('Получил текущий рекорд!!!')
    return result[0]


def checking_the_record(game_sql, record_game, value):
    """ Проверка на побивание рекорда, value может быть:
    1) max - рекорд должен быть как можно Больше
    2) min -рекорд должен быть как можно Меньше
    """
    cur_record = current_record(game_sql)  # Текущий рекорд

    print(game_sql, record_game, cur_record)
    if value == 'min':
        if cur_record == 0 or cur_record > record_game:
            update_result_DB(game_sql, record_game)
            print('ОТРАБОТАЛ 1, Записал, min')
    else:
        if cur_record < record_game:
            update_result_DB(game_sql, record_game)
            print('ОТРАБОТАЛ 2, Записал, max')