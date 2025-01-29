import tkinter as tk
import random
import threading

vowels = ['a', 'e', 'i', 'o', 'u']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Списки для зберігання результатів
vowel_result = []
consonant_result = []
digit_result = []

# Функція для генерації голосних
def generate_vowels():
    vowel_result.clear()
    while len(vowel_result) < 6:  # Оскільки чергування 1 голосна, 2 приголосні
        vowel_result.append(random.choice(vowels))

# Функція для генерації приголосних
def generate_consonants():
    consonant_result.clear()
    while len(consonant_result) < 12:  # Для 2 приголосних на кожну групу
        consonant_result.append(random.choice(consonants))

# Функція для генерації цифр
def generate_digits():
    digit_result.clear()
    while len(digit_result) < 6:  # Для 1 цифри на кожну групу
        digit_result.append(random.choice(digits))

# Основна функція генерації пароля, що комбінує символи з усіх трьох потоків
def generate_password():
    # Створення потоків для кожної групи символів
    vowel_thread = threading.Thread(target=generate_vowels)
    consonant_thread = threading.Thread(target=generate_consonants)
    digit_thread = threading.Thread(target=generate_digits)

    # Запуск потоків
    vowel_thread.start()
    consonant_thread.start()
    digit_thread.start()

    # Очікуємо завершення всіх потоків
    vowel_thread.join()
    consonant_thread.join()
    digit_thread.join()

    # Формування пароля: чергування 1 голосної, 2 приголосних, 1 цифри
    password = []
    i = 0
    while len(password) < 12:
        if i < len(vowel_result) and len(password) < 12:
            password.append(vowel_result[i])
        if i < len(consonant_result) and len(password) < 12:
            password.append(consonant_result[i])
        if i + 1 < len(consonant_result) and len(password) < 12:
            password.append(consonant_result[i + 1])
        if i < len(digit_result) and len(password) < 12:
            password.append(digit_result[i])
        i += 1

    return ''.join(password)

# Функція для запуску генерації в окремому потоці
def thread_generate_password(entry, label):
    password = generate_password()
    entry.delete(0, tk.END)
    entry.insert(0, password)
    check_length(entry, label)

# Функція для перевірки довжини пароля
def check_length(entry, label):
    password = entry.get()
    if len(password) >= 12:
        label.config(text="Пароль достатньої довжини.", fg="green")
    else:
        label.config(text="Пароль занадто короткий.", fg="red")

# Створення основного вікна
window = tk.Tk()
window.title("Генератор паролів")

password_entry = tk.Entry(window, width=25, font=("Arial", 14))
password_entry.grid(row=0, column=0, padx=10, pady=10)

generate_button = tk.Button(window, text="Генерувати пароль", width=20, font=("Arial", 12),
                            command=lambda: threading.Thread(target=thread_generate_password, args=(password_entry, length_label)).start())
generate_button.grid(row=1, column=0, padx=10, pady=10)

length_label = tk.Label(window, text="Перевірка довжини пароля", font=("Arial", 12))
length_label.grid(row=2, column=0, padx=10, pady=10)

check_button = tk.Button(window, text="Перевірити довжину", width=20, font=("Arial", 12), command=lambda: check_length(password_entry, length_label))
check_button.grid(row=3, column=0, padx=10, pady=10)

window.mainloop()
