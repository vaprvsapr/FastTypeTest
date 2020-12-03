
from tkinter import *
from tkinter import scrolledtext
import random
import time

number_of_small_texts = 1
number_of_medium_texts = 1
number_of_big_texts = 1


class Project:  # Этот класс отвечает за визуализацию

    def __init__(self, master):
        self.master = master  # Передаю в класс окно, в которое этот класс отрисовывается
        self.coordinates = [550, 100]  # Передаю отладочные координаты

        # Описываю все ништяки, которые встречаются в этом классе
        self.file_name = ""
        self.timer = 0
        self.symbols_words = ['', '']

        self.prepare_label = Label(self.master, text="Пальцы на клавиатуру.",
                                   font=("Arial Black", 20))  # Это окошко предупредит, когда печатать
        # Это наш текст, который надо напечатать
        self.main_text_label = Label(self.master, text="text", font=("Times New Roman", 20))
        # Это окно ввода
        self.main_scrolled_text = scrolledtext.ScrolledText(self.master, width=60, height=12,
                                                            font=("Times New Roman", 20))
        # Кнопка "Сохранить"
        self.save_button = Button(self.master, text="Сохранить", font=15, width=10, command=self.command_save_button)

        # Кнопка "Пройти тест ещё раз"
        self.restart_button = Button(self.master, text="Пройти тест ещё раз",
                                     font=15, width=20, command=self.command_restart)

        self.calculations = Label(self.master, text='Тут что-то должно быть', font=("Arial Black", 20))

        # Замечательное приветственное лобби
        self.greeting_label = Label(self.master, text='Правила: вам предлагается выбрать объём текста для набора. '
                                                      '\nПосле выбора на экране появится текст.'
                                                      '\nКогда вы закончите набор текста нажмите кнопку "Готово"',
                                    font=("Arial black", 20), justify="left")

        # Три кнопки: Большой, Средний, Маленький
        self.btn_small = Button(self.master, text="Маленький", font=15, width=10,
                                command=lambda: self.chose_text_type("small"))
        self.btn_medium = Button(self.master, text="Средний", font=15, width=10,
                                 command=lambda: self.chose_text_type("med"))
        self.btn_big = Button(self.master, text="Большой", font=15, width=10,
                              command=lambda: self.chose_text_type("big"))
        self.draw_greeting_lobby()

    def draw_greeting_lobby(self):  # Эта функция отрисовывает начальное лобби.
        # Отрисовка вынесена в функциию, чтобы можно было отрисовать ещё раз и начать всё сначала.
        self.greeting_label.place(x=self.coordinates[0], y=self.coordinates[1])
        self.btn_small.place(x=self.coordinates[0] + 350, y=self.coordinates[1] + 150)
        self.btn_medium.place(x=self.coordinates[0] + 350, y=self.coordinates[1] + 200)
        self.btn_big.place(x=self.coordinates[0] + 350, y=self.coordinates[1] + 250)

    def chose_text_type(self, text):

        if text == "small":
            n = random.randint(1, number_of_small_texts)
            self.file_name = "small" + str(n) + ".txt"
        elif text == "med":
            n = random.randint(1, number_of_medium_texts)
            self.file_name = "med" + str(n) + ".txt"
        elif text == "big":
            n = random.randint(1, number_of_big_texts)
            self.file_name = "big" + str(n) + ".txt"

        self.greeting_label.place_forget()  # Этим блоком кода уничтожается приветственное лобби
        self.btn_small.place_forget()
        self.btn_medium.place_forget()
        self.btn_big.place_forget()

        self.create_waiting_lobby()  # Запускаю следующий блок кода

    def create_waiting_lobby(self):

        self.prepare_label.pack()  # Тут я орисовываю "Пальцы на клавиатуру"
        self.prepare_label.place(x=800, y=200)

        time.sleep(0.1)  # Даём подготовиться к набору
        self.master.update()

        self.create_main_text_lobby()  # У меня код связан в цепочку.
        # Поэтому после окончания выполнения одной функции, она вызывает другую.

    def create_main_text_lobby(self):

        time.sleep(1)
        self.prepare_label.place_forget()  # Перестаю отрисовывать "Пальцы на клавиатуру"

        with open(self.file_name) as f:  # Читаю из нужного файла текст

            coord = [int(x) for x in f.readline().split()]
            text = f.read()

        self.main_text_label.configure(text=text)  # Вностим текст
        self.main_text_label.place(x=coord[0], y=coord[1])  # Устанавливаю текст, в зависимости от его размера

        self.main_scrolled_text.place(x=570, y=coord[1] + 250)  # Отрисовка окошка ввода

        self.save_button.place(x=900, y=coord[1] + 650)  # Отрисовка кнопки "Сохранить"
        self.timer = time.time()

    def command_save_button(self):

        with open("entered_text.txt", "w") as f:
            f.write(self.main_scrolled_text.get("1.0", END))

        # Вызов следующего участка кода
        self.create_final_lobby()

    def create_final_lobby(self):
        # Удалим main_lobby
        self.main_text_label.place_forget()
        self.main_scrolled_text.place_forget()
        self.save_button.place_forget()

        # Осталось нарисовать результат обработки проверяющей программой.

        mistakes = self.calculate_mistakes()
        dt = time.time() - self.timer

        self.calculations.config(text="Проверка: размеры текстов совпадают? -> {}\n"
                                      "Проверка: количество ошибок в посимвольном сравнении -> {}\n"
                                      "Проверка: количество ошибок при сравнении по словам -> {}\n"
                                      "Проверка орфографии: (если нет ошибки, возвращает True, иначе, False\n"
                                      "Знак: ',', результат -> {}\n"
                                      "Знак: '.', результат -> {}\n"
                                      "Знак: '!', результат -> {}\n"
                                      "Знак: '?', результат -> {}\n"
                                      "Знак: ':', результат -> {}\n"
                                      "Знак: ';', результат -> {}\n"
                                      "Знак: '-', результат -> {}\n\n"
                                      "Время набора: {}с\n\n"
                                      "Скорость набора:\n"
                                      "{} символов в минуту\n"
                                      "{} слов в минуту".format(mistakes[0],
                                                                mistakes[1],
                                                                mistakes[2],
                                                                mistakes[3][0],
                                                                mistakes[3][1],
                                                                mistakes[3][2],
                                                                mistakes[3][3],
                                                                mistakes[3][4],
                                                                mistakes[3][5],
                                                                mistakes[3][6],
                                                                round(dt),
                                                                round(float(self.symbols_words[0]) / dt * 60),
                                                                round(float(self.symbols_words[1]) / dt * 60)
                                                                ))
        print(self.symbols_words[0])
        self.calculations.place(x=440, y=40)

        # Добавим кнопку "Пройти тест ещё раз"
        self.restart_button.place(x=850, y=600)

    def command_restart(self):
        self.restart_button.place_forget()  # Удаляю финальное окно
        self.calculations.place_forget()  # Удаляю расчет ошибок
        self.draw_greeting_lobby()  # Начинаю всё сначала

        self.main_scrolled_text.delete("1.0", END)  # Очищаю для повторного использования

    def calculate_mistakes(self):
        with open('entered_text.txt') as f:
            entered_text = f.read()

        with open("{}".format(self.file_name)) as f:
            f.readline()
            real_text = f.read()

        self.symbols_words = len(entered_text.strip()), len(entered_text.strip().split()),

        # Опишем алгоритм проверки текста
        # 1. Мы не проверяем ENTER-ы. Можно написать всё в одну строчку. (Хотя, может, стишки и проверяем).
        # 2. Мы будем сплитать полученный текст методом "split()".
        # 3. Проверка пунктуаыии. Сплитать мы будем по пробелам. Поэтому нужно правильно расставлять пробелы.
        # 4. Если в слове есть хотябы одна ошибка, то будем считать, что слово написано с ошибкой.
        # 5. Все ошибки считаем одного типа: ОШИБКА. (Орфография, пунктуация, пропуск буквы, добавление буквы).

        mistakes = []
        # mistakes[0] - Совпадают ли длины текстов.
        # mistakes[1] - Количество несовпадений в посимвольном сравнении.
        # mistakes[2] - Количество несовпадений в пословном сравнении.

        #  1. Проверка: совпадают ли тексты. Результат проверки - Да / Нет.
        mistakes.append(len(real_text.strip()) == len(entered_text.strip()))

        #  2. Проверка: посимвольная проверка текста. Результат проверки - количество ошибок.
        mistakes.append(0)
        for i in range(min(len(real_text) - 1, len(entered_text) - 1)):
            if real_text[i] != entered_text[i]:
                print(real_text[i], entered_text[i])
                mistakes[1] += 1

        #  3. Проверка: проверка по словам. Результат проверки - количество ошибок.
        mistakes.append(0)
        array_real_text = real_text.split(' ')
        array_entered_text = entered_text.split(' ')

        for i in range(min(len(array_real_text) - 1, len(array_entered_text) - 1)):
            if array_entered_text[i] != array_real_text[i]:
                mistakes[2] += 1

        #  4. Проверка: проверка пунктуации. Результат проверки - количество ошибок.
        punctuation_mistakes = [real_text.count(",") == entered_text.count(","),
                                real_text.count(".") == entered_text.count("."),
                                real_text.count("!") == entered_text.count("!"),
                                real_text.count("?") == entered_text.count("?"),
                                real_text.count(":") == entered_text.count(":"),
                                real_text.count(";") == entered_text.count(";"),
                                real_text.count('-') == entered_text.count('-')]

        mistakes.append(punctuation_mistakes)

        print(mistakes)

        return mistakes


window = Tk()  # Создаём окно
window.title("Тест скорости набора текста.")  # Обзовём необычно наше окно
window.geometry("1920x1080")  # Устанавливаем размер окна
project = Project(window)  # Создаём экземпляр класса "Project"
window.mainloop()  # Цикл отрисовки окна
