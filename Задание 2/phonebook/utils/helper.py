import os

from services import print_service
from utils import errors


def check_file_exists(filepath):
    """Проверка существования файла"""
    if not os.path.exists(filepath):
        print_service.show_message(errors.FILE_NOT_FOUND_ERROR)
        return False

    return True


def prompt(prompt_text, default=""):
    """Обработка ввода пользователя"""
    while True:
        try:
            text = input(prompt_text).strip()

            if text == "" and default == "":
                print(errors.FIELD_NOT_TO_BE_EMPTY_ERROR)
                continue

            return text if text != "" else default
        except EOFError as e:
            print(errors.BASE_ERROR, e)
