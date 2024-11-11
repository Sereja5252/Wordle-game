"""
Модуль для графического интерфейса игры Wordle.
Реализует класс WordleGUI с использованием Tkinter.
"""

import tkinter as tk
from tkinter import messagebox
from game import WordleGame

class WordleGUI:
    """
    Класс для создания графического интерфейса игры Wordle.
    """
    
    def __init__(self):
        """
        Инициализация графического интерфейса пользователя.
        """
        self.root = tk.Tk()
        self.root.title("Wordle")
        self.game = None
        self.cells = []
        self.current_row = 0
        self.word_length = 5
        self.max_attempts = self.word_length + 1

        self.setup_frames()
        self.show_length_selection()

    def setup_frames(self):
        """
        Создаёт фреймы для выбора длины слова.
        """
        self.length_frame = tk.Frame(self.root)
        self.length_frame.pack(padx=20, pady=20)

        self.game_frame = tk.Frame(self.root)

    def show_length_selection(self):
        """
        Отображает фрейм выбора длины слова.
        """
        self.game_frame.pack_forget()

        tk.Label(self.length_frame, text="Добро пожаловать в Wordle на русском языке!", font=('Helvetica', 16)).pack(pady=10)
        tk.Label(self.length_frame, text="Выберите длину слова (4, 5, 6 или 7):", font=('Helvetica', 14)).pack(pady=5)

        self.length_var = tk.IntVar(value=5)

        lengths = [4, 5, 6, 7]
        for length in lengths:
            tk.Radiobutton(self.length_frame, text=str(length), variable=self.length_var, value=length, font=('Helvetica', 12)).pack(anchor=tk.W)

        tk.Button(self.length_frame, text="Начать игру", command=self.start_game, font=('Helvetica', 12)).pack(pady=10)

    def start_game(self):
        """
        Инициализирует игру с выбранной длиной слова и отображает фрейм игры.
        """
        self.word_length = self.length_var.get()
        self.game = WordleGame(self.word_length)
        self.game.start_game()
        if self.game.game_over:
            messagebox.showerror("Ошибка", "Не удалось загрузить слово.")
            self.root.destroy()
            return

        self.max_attempts = self.game.max_attempts

        self.length_frame.pack_forget()

        self.game_frame.pack(padx=20, pady=20)

        self.create_grid()

        self.create_input_area()

    def create_grid(self):
        """
        Создаёт сетку клеток игры.
        """
        self.cells = []
        for i in range(self.max_attempts):
            row = []
            for j in range(self.word_length):
                cell = tk.Label(self.game_frame, text='', width=4, height=2, borderwidth=1, relief='solid', font=('Helvetica', 24))
                cell.grid(row=i, column=j, padx=2, pady=2)
                row.append(cell)
            self.cells.append(row)

    def create_input_area(self):
        """
        Создаёт область ввода догадок с полем ввода и кнопкой отправки.
        """
        self.input_var = tk.StringVar()
        input_frame = tk.Frame(self.game_frame)
        input_frame.grid(row=self.max_attempts, column=0, columnspan=self.word_length, pady=10)
        tk.Label(input_frame, text="Введите слово: ", font=('Helvetica', 14)).pack(side=tk.LEFT)
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var, font=('Helvetica', 14))
        self.input_entry.pack(side=tk.LEFT)
        self.input_entry.focus()
        tk.Button(input_frame, text="Отправить", command=self.submit_guess, font=('Helvetica', 12)).pack(side=tk.LEFT, padx=5)
        self.root.bind('<Return>', lambda event: self.submit_guess())

    def submit_guess(self):
        """
        Обрабатывает догадку пользователя: проверяет её, обновляет сетку и определяет окончание игры.
        """
        if self.game.is_game_over():
            return

        guess = self.input_var.get().lower()
        self.input_var.set('')

        if len(guess) != self.word_length:
            messagebox.showwarning("Некорректная длина", f"Слово должно быть длиной {self.word_length} букв.")
            return

        if not self.game.word_list.is_valid_word(guess):
            messagebox.showwarning("Слово не найдено", "Слово не найдено в словаре. Попробуйте другое слово.")
            return

        feedback = self.game.check_guess(guess)
        self.update_grid(feedback, guess)

        if self.game.is_game_over():
            if guess == self.game.target_word:
                messagebox.showinfo("Победа!", f"Поздравляем! Вы угадали слово '{self.game.target_word}'.")
            else:
                messagebox.showinfo("Проигрыш", f"Вы проиграли. Загаданное слово было: '{self.game.target_word}'.")
            self.disable_input()

    def update_grid(self, feedback, guess):
        """
        Обновляет сетку клеток на основе результатов проверки догадки.
        """
        for idx, (status, letter) in enumerate(zip(feedback, guess)):
            cell = self.cells[self.current_row][idx]
            cell.config(text=letter.upper())
            if status == 'correct':
                cell.config(bg='green', fg='white')
            elif status == 'present':
                cell.config(bg='yellow', fg='black')
            else:
                cell.config(bg='grey', fg='white')
        self.current_row += 1

    def disable_input(self):
        """
        Отключает поле ввода после завершения игры.
        """
        self.input_entry.config(state='disabled')

    def run(self):
        """
        Запускает главный цикл приложения.
        """
        self.root.mainloop()
