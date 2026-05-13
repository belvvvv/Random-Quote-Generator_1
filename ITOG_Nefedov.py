import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# ---------------------- Файл ---------------------- #

HISTORY_FILE = "quotes_history.json"

# ---------------------- Предопределённые цитаты ---------------------- #

quotes = [
    {
        "text": "Знание — сила.",
        "author": "Фрэнсис Бэкон",
        "topic": "Мотивация"
    },
    {
        "text": "Не откладывай на завтра то, что можно сделать сегодня.",
        "author": "Бенджамин Франклин",
        "topic": "Продуктивность"
    },
    {
        "text": "Успех — это движение от неудачи к неудаче без потери энтузиазма.",
        "author": "Уинстон Черчилль",
        "topic": "Успех"
    },
    {
        "text": "Будь собой. Остальные роли уже заняты.",
        "author": "Оскар Уайльд",
        "topic": "Жизнь"
    }
]

history = []

# ---------------------- Функции ---------------------- #

def generate_quote():
    author_filter = author_filter_entry.get().strip().lower()
    topic_filter = topic_filter_entry.get().strip().lower()

    filtered_quotes = quotes

    # Фильтр по автору
    if author_filter:
        filtered_quotes = [
            quote for quote in filtered_quotes
            if author_filter in quote["author"].lower()
        ]

    # Фильтр по теме
    if topic_filter:
        filtered_quotes = [
            quote for quote in filtered_quotes
            if topic_filter in quote["topic"].lower()
        ]

    if not filtered_quotes:
        messagebox.showwarning(
            "Нет данных",
            "Цитаты не найдены!"
        )
        return

    selected_quote = random.choice(filtered_quotes)

    result_label.config(
        text=f'“{selected_quote["text"]}”\n— {selected_quote["author"]} ({selected_quote["topic"]})'
    )

    history.append(selected_quote)

    update_history()
    save_history()


def update_history():
    history_listbox.delete(0, tk.END)

    for quote in history:
        history_listbox.insert(
            tk.END,
            f'{quote["author"]}: {quote["text"]}'
        )


def add_quote():
    text = quote_entry.get("1.0", tk.END).strip()
    author = author_entry.get().strip()
    topic = topic_entry.get().strip()

    # Проверка пустых строк
    if not text or not author or not topic:
        messagebox.showerror(
            "Ошибка",
            "Все поля должны быть заполнены!"
        )
        return

    quotes.append({
        "text": text,
        "author": author,
        "topic": topic
    })

    quote_entry.delete("1.0", tk.END)
    author_entry.delete(0, tk.END)
    topic_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Успех",
        "Цитата добавлена!"
    )


def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


def load_history():
    global history

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

        update_history()

# ---------------------- GUI ---------------------- #

root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("700x650")
root.resizable(False, False)

# ---------------------- Заголовок ---------------------- #

title_label = tk.Label(
    root,
    text="Генератор случайных цитат",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=10)

# ---------------------- Фильтры ---------------------- #

filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Автор").grid(row=0, column=0, padx=5)

author_filter_entry = tk.Entry(filter_frame, width=20)
author_filter_entry.grid(row=0, column=1)

tk.Label(filter_frame, text="Тема").grid(row=0, column=2, padx=5)

topic_filter_entry = tk.Entry(filter_frame, width=20)
topic_filter_entry.grid(row=0, column=3)

# ---------------------- Генерация ---------------------- #

generate_button = tk.Button(
    root,
    text="Сгенерировать цитату",
    font=("Arial", 12),
    command=generate_quote
)
generate_button.pack(pady=10)

# ---------------------- Результат ---------------------- #

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 14),
    wraplength=600,
    justify="center",
    fg="blue"
)
result_label.pack(pady=15)

# ---------------------- История ---------------------- #

tk.Label(
    root,
    text="История цитат:",
    font=("Arial", 12, "bold")
).pack()

history_listbox = tk.Listbox(
    root,
    width=80,
    height=10
)
history_listbox.pack(pady=10)

# ---------------------- Добавление цитаты ---------------------- #

add_frame = tk.Frame(root)
add_frame.pack(pady=15)

tk.Label(add_frame, text="Текст цитаты").grid(row=0, column=0)

quote_entry = tk.Text(add_frame, width=40, height=4)
quote_entry.grid(row=1, column=0, columnspan=2, pady=5)

tk.Label(add_frame, text="Автор").grid(row=2, column=0)

author_entry = tk.Entry(add_frame, width=30)
author_entry.grid(row=2, column=1)

tk.Label(add_frame, text="Тема").grid(row=3, column=0)

topic_entry = tk.Entry(add_frame, width=30)
topic_entry.grid(row=3, column=1)

add_button = tk.Button(
    root,
    text="Добавить цитату",
    command=add_quote
)
add_button.pack(pady=10)

# ---------------------- Загрузка истории ---------------------- #

load_history()

# ---------------------- Запуск ---------------------- #

root.mainloop()
