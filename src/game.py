"""
Модуль, содержащий класс WordleGame.
Обрабатывает основную логику игры, включая выбор слова и проверку догадок.
"""

from typing import List
from wordlist import WordList

class WordleGame:
    """
    Класс, управляющий логикой игры Wordle.
    """

    def __init__(self, word_length: int):
        """
        Инициализация игры с заданной длиной слова.
        """
        self.word_length = word_length
        self.word_list = WordList(word_length)
        self.target_word = ''
        self.max_attempts = word_length + 1
        self.attempts = 0
        self.game_over = False

    def start_game(self):
        """
        Запуск новой игры.
        """
        self.attempts = 0
        self.game_over = False
        self.target_word = self.word_list.get_random_word()
        if not self.target_word:
            print("Невозможно загрузить слово.")
            self.game_over = True

    def check_guess(self, guess: str) -> List[str]:
        """
        Проверка догадки пользователя и предоставление обратной связи.
        """
        if not self.word_list.is_valid_word(guess):
            return ['invalid']
        result = []
        for i, char in enumerate(guess):
            if char == self.target_word[i]:
                result.append('correct')
            elif char in self.target_word:
                result.append('present')
            else:
                result.append('absent')
        self.attempts += 1
        if guess == self.target_word or self.attempts >= self.max_attempts:
            self.game_over = True
        return result

    def is_game_over(self) -> bool:
        """
        Проверка, закончилась ли игра.
        """
        return self.game_over

