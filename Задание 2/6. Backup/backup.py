import logging
import os
import zipfile
from datetime import datetime

# Настройка логирования.
logging.basicConfig(
    filename="backup.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log(message, error=False):
    """Одновременное логирование в файл и консоль"""
    if not error:
        logging.info(message)
    else:
        logging.error(message)
    print(message)


def create_backup(src_folder: str, dest_folder: str):
    """Создание ZIP-архива с резервной копией"""
    if not os.path.exists(src_folder):
        log(f"Исходная папка не найдена: {src_folder}", True)
        raise FileNotFoundError(f"Исходная папка не найдена: {src_folder}")

    if not os.path.exists(dest_folder):
        try:
            os.makedirs(dest_folder, exist_ok=True)
            log(f"Создана папка назначения: {dest_folder}")
        except Exception as e:
            log(f"Ошибка при создании папки назначения: {e}", True)
            raise

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{timestamp}.zip"
    archive_path = os.path.join(dest_folder, archive_name)

    try:
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(src_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, src_folder)

                    try:
                        zipf.write(file_path, rel_path)
                        log(f"Добавлен файл: {file_path} → {rel_path}")
                    except Exception as e:
                        log(f"Ошибка при добавлении файла {file_path}: {e}", True)

        log(f"Резервная копия создана: {archive_path}")
    except Exception as e:
        log(f"Ошибка при создании архива: {e}", True)


def main():
    print("======== Утилита резервного копирования директории ========")
    src_dir = input("Введите путь к исходной директории: ").strip()
    dest_dir = input("Введите путь для сохранения архива: ").strip()

    try:
        create_backup(src_dir, dest_dir)
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
