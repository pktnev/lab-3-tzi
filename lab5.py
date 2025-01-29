import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Алгоритм Гронсфельда
def gronsfeld_cipher(text, key, mode="encrypt"):
    key = [int(digit) for digit in key]  # Перетворення ключа в список чисел
    alphabet = alphabet_entry.get().strip()  # Отримуємо алфавіт із GUI
    result = []

    # Обробка кожного символу
    for i, char in enumerate(text.strip()):
        if char.isalpha():  # Обробляємо тільки літери
            is_upper = char.isupper()
            char_upper = char.upper()

            # Перевіряємо чи є символ в алфавіті
            if char_upper in alphabet:
                idx = alphabet.index(char_upper)
                shift = key[i % len(key)]  # Використовуємо зсув по циклу ключа

                if mode == "encrypt":
                    new_idx = (idx + shift) % len(alphabet)
                elif mode == "decrypt":
                    new_idx = (idx - shift) % len(alphabet)

                # Якщо буква була великою, то зберігаємо великий регістр в іншому випадку малий
                result_char = alphabet[new_idx]
                result.append(result_char.upper() if is_upper else result_char.lower())
            else:
                result.append(char)  # Якщо символ не буква, додаємо як є
        else:
            # Якщо символ не літера, зберігаємо його без змін
            result.append(char)

    return "".join(result)

# Функції для шифрування/дешифрування
def encrypt_text():
    key = key_input.get()
    if len(key) < 6 or not key.isdigit():  # Перевірка на правильність ключа
        messagebox.showerror("Помилка", "Ключ має містити мінімум 6 цифр")
        return
    text = input_text.get("1.0", tk.END).strip()
    encrypted_text = gronsfeld_cipher(text, key, mode="encrypt")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, encrypted_text)
    # Зберігаємо зашифрований текст для подальшого розшифрування
    global encrypted_result
    encrypted_result = encrypted_text

def decrypt_text():
    key = key_input.get()
    if len(key) < 6 or not key.isdigit():  # Перевірка на правильність ключа
        messagebox.showerror("Помилка", "Ключ має містити мінімум 6 цифр")
        return

    if not encrypted_result:
        messagebox.showerror("Помилка", "Шифр ще не зашифрований, неможливо розшифрувати.")
        return

    result = gronsfeld_cipher(encrypted_result, key, mode="decrypt")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

# Завантаження тексту з файлу
def load_text_from_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file.read())

# Функція для перевірки пароля
def check_password():
    correct_password = "123456"
    password = password_input.get()

    if password == correct_password:
        messagebox.showinfo("Успіх", "Пароль правильний, доступ дозволено.")
        password_frame.pack_forget()  # Сховати поля пароля
        encryption_frame.pack(padx=10, pady=10)  # Показати поля для шифрування
    else:
        messagebox.showerror("Помилка", "Невірний пароль! Комп'ютер буде перезавантажено.")
        close_and_reset()

# Видалення файлу
def delete_file():
    try:
        file_path = "C:/Users/Administrator/PycharmProjects/TZII/dist/lab5.exe"
        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("Повідомлення", f"Файл {file_path} видалено.")
        else:
            messagebox.showinfo("Повідомлення", f"Файл {file_path} не знайдено.")
    except PermissionError:
        messagebox.showerror("Помилка доступу", "Не вдалося отримати доступ до файлу для видалення. Запустіть програму з правами адміністратора.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося видалити файл: {e}")

# Функція для перезавантаження компютера
def close_and_reset():
    delete_file()

    messagebox.showinfo("Перезавантаження", "Систему буде перезавантажено.")
    os.system("shutdown /r /t 1")  # Перезавантаження через команду в Windows

# Створення GUI
root = tk.Tk()
root.title("Захист системи від НСД")

# Рамка для паролю
password_frame = tk.Frame(root)
tk.Label(password_frame, text="Введіть пароль:").grid(row=0, column=0, padx=5, pady=5)
password_input = tk.Entry(password_frame, show="*")
password_input.grid(row=0, column=1, padx=5, pady=5)

password_button = tk.Button(password_frame, text="Перевірити пароль", command=check_password)
password_button.grid(row=1, column=0, columnspan=2, pady=10)

password_frame.pack(padx=10, pady=10)

# Рамка для шифрування після перевірки пароля
encryption_frame = tk.Frame(root)

# Поле алфавіту
tk.Label(encryption_frame, text="Алфавіт:").grid(row=0, column=0, padx=5, pady=5)
alphabet_entry = tk.Entry(encryption_frame, width=50)
alphabet_entry.insert(0, "АБВГҐДЕЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ")
alphabet_entry.grid(row=0, column=1, padx=5, pady=5)

# Поле для введення ключа
tk.Label(encryption_frame, text="Ключ (мін. 6 цифр):").grid(row=1, column=0, padx=5, pady=5)
key_input = tk.Entry(encryption_frame)
key_input.grid(row=1, column=1, padx=5, pady=5)

# Поле введення тексту
tk.Label(encryption_frame, text="Вхідний текст:").grid(row=2, column=0, padx=5, pady=5)
input_text = tk.Text(encryption_frame, height=10, width=50)
input_text.grid(row=2, column=1, padx=5, pady=5)

# Поле результатів
tk.Label(encryption_frame, text="Результат:").grid(row=3, column=0, padx=5, pady=5)
output_text = tk.Text(encryption_frame, height=10, width=50)
output_text.grid(row=3, column=1, padx=5, pady=5)

# Кнопки
encrypt_button = tk.Button(encryption_frame, text="Зашифрувати", command=encrypt_text)
encrypt_button.grid(row=4, column=0, padx=5, pady=5)

decrypt_button = tk.Button(encryption_frame, text="Розшифрувати", command=decrypt_text)
decrypt_button.grid(row=4, column=1, padx=5, pady=5)

load_button = tk.Button(encryption_frame, text="Завантажити текст з файлу", command=load_text_from_file)
load_button.grid(row=5, column=0, columnspan=2, pady=10)

# Запуск головного циклу Tkinter
root.mainloop()
