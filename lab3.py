import tkinter as tk
from tkinter import filedialog, messagebox


# Алгоритм Гронсфельда
# Алгоритм Гронсфельда
def gronsfeld_cipher(text, key, mode="encrypt"):
    key = [int(digit) for digit in key]  # Перетворення ключа в список чисел
    alphabet = alphabet_entry.get().strip()  # Отримуємо алфавіт із GUI
    result = []

    # Обробка кожного символу
    for i, char in enumerate(text.strip()):
        if char.isalpha():  # Обробляємо тільки літери
            # Перевіряємо чи це велика буква
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

                # Якщо буква була великою то зберігаємо великий регістр в іншому випадку малий
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


# Створення GUI
root = tk.Tk()
root.title("Gronsfeld Cipher")

# Поле алфавіту
tk.Label(root, text="Алфавіт:").grid(row=0, column=0, padx=5, pady=5)
alphabet_entry = tk.Entry(root, width=50)
alphabet_entry.insert(0, "АБВГҐДЕЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ")
alphabet_entry.grid(row=0, column=1, padx=5, pady=5)

# Поле для вибору типу шифрування
tk.Label(root, text="Ключ (мін. 6 цифр):").grid(row=1, column=0, padx=5, pady=5)
key_input = tk.Entry(root)
key_input.grid(row=1, column=1, padx=5, pady=5)

# Поле введення тексту
tk.Label(root, text="Вхідний текст:").grid(row=2, column=0, padx=5, pady=5)
input_text = tk.Text(root, height=10, width=50)
input_text.grid(row=2, column=1, padx=5, pady=5)

# Поле результатів
tk.Label(root, text="Результат:").grid(row=3, column=0, padx=5, pady=5)
output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=3, column=1, padx=5, pady=5)

# Кнопки
encrypt_button = tk.Button(root, text="Зашифрувати", command=encrypt_text)
encrypt_button.grid(row=4, column=0, padx=5, pady=5)

decrypt_button = tk.Button(root, text="Розшифрувати", command=decrypt_text)
decrypt_button.grid(row=4, column=1, padx=5, pady=5)

load_button = tk.Button(root, text="Завантажити текст з файлу", command=load_text_from_file)
load_button.grid(row=5, column=0, columnspan=2, pady=10)

# Запуск головного циклу Tkinter
root.mainloop()
