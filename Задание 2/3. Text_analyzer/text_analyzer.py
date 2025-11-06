import re
from collections import Counter
from datetime import datetime

import chardet

DEFAULT_CHARSET = "utf-8"
TOP_WORDS = 10


def detect_encoding(filepath):
    """Определение кодировки файла"""
    with open(filepath, "rb") as f:
        raw_data = f.read(100_000)

    result = chardet.detect(raw_data)
    return result["encoding"] or DEFAULT_CHARSET


def load_text(filepath):
    """Загрузка текста с правильной кодировкой"""
    encoding = detect_encoding(filepath)
    try:
        with open(filepath, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла: {e}")


def analyze_text(text):
    """Анализ текста"""
    cleaned_text = text.strip()

    total_chars = len(cleaned_text)
    total_chars_no_spaces = len(cleaned_text.replace(" ", ""))

    words = re.findall(r"\b\w+\b", cleaned_text.lower())
    total_words = len(words)

    unique_words = len(set(words))

    sentences = re.split(r"[.!?]+", cleaned_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    total_sentences = len(sentences)

    counter = Counter(words)
    top_words = counter.most_common(TOP_WORDS)

    return {
        "total_words": total_words,
        "total_chars": total_chars,
        "total_chars_no_spaces": total_chars_no_spaces,
        "total_sentences": total_sentences,
        "unique_words": unique_words,
        "top_words": top_words,
    }


def save_report(report_path, stats):
    """Сохранение отчёта в файл"""
    with open(report_path, "w", encoding=DEFAULT_CHARSET) as file:
        print_text(file, "Отчёт по анализу текста\n")
        print_text(file, "=" * 40 + "\n")
        print_text(file, f"Всего слов: {stats['total_words']}\n")
        print_text(file, f"Всего символов (с пробелами): {stats['total_chars']}\n")
        print_text(file, f"Всего символов (без пробелов): {stats['total_chars_no_spaces']}\n")
        print_text(file, f"Количество предложений: {stats['total_sentences']}\n")
        print_text(file, f"Уникальных слов: {stats['unique_words']}\n\n")
        print_text(file, "Топ-10 слов:\n")

        for word, count in stats["top_words"]:
            print_text(file, f" - {word}: {count}\n")

        print_text(file, "=" * 40 + "\n")
        print_text(file, f"Отчёт сохранён в {report_path}\n")


def print_text(file, text):
    """Вывод текста в консоль и запись в файл"""
    file.write(text)
    print(text, end="")


def get_report_file_name(text_file_name):
    return f'report-for-{text_file_name.removesuffix(".txt")}-{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.txt'


def main():
    try:
        file_name = input("Введите путь к текстовому файлу (директория texts): ").strip()
        file_path = 'texts/' + file_name
        text = load_text(file_path)
        stats = analyze_text(text)
        final_path = f'reports/{get_report_file_name(file_name)}'
        save_report(final_path, stats)
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
