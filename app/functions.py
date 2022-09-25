import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


def get_hash(password):
    """
    Создаёт хэш пароля пользователя
    :param password: Пароль пользователя
    :return: Хэш пароля пользователя в виде строки
    """
    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),  # Convert the password to bytes
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )
    return base64.b64encode(hash_digest)


def compare_passwords(password_hash, other_password):
    """
    Сравнивает переданный и сохранённый пароли пользователя
    :param password_hash: Сохранённый пароль пользователя
    :param other_password: Переданный пароль пользователя
    :return: Булево значение
    """
    return hmac.compare_digest(
        base64.b64decode(password_hash), get_hash(other_password)
    )
