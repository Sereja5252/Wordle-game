"""
Модуль для управления списком слов, используемых в игре Wordle.
Содержит класс WordList для загрузки и проверки слов.
"""

import os
import random
from typing import List

class WordList:
    """
    Класс для работы со списком слов заданной длины.
    """

    def __init__(self, word_length: int):
        """
        Инициализация класса WordList.
        """
        self.word_length = word_length
        self.words = self.load_words()

    def load_words(self) -> List[str]:
        """
        Загрузка списка слов из файла.
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            assets_dir = os.path.join(script_dir, '..', 'assets')
            file_path = os.path.join(assets_dir, f'words_{self.word_length}.txt')

            with open(file_path, 'r', encoding='utf-8') as file:
                words = [line.strip().lower() for line in file if len(line.strip()) == self.word_length]
            return words
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return []

    def get_random_word(self) -> str:
        """
        Получение случайного слова из списка.
        """
        return random.choice(self.words) if self.words else ''

    def is_valid_word(self, word: str) -> bool:
        """
        Проверяет, существует ли слово в словаре.
        """
        return word.lower() in self.words

