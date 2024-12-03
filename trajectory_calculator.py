import tkinter as tk
from tkinter import messagebox
import math
import bcrypt # type: ignore
import json
from tkinter import Tk, Label, Entry, Button, messagebox
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

# Функція для перевірки коректності email
def is_valid_email(email):
    return "@" in email and "." in email

# Функція для хешування пароля
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Симуляція бази даних
users_db = {}

# Функція для реєстрації користувача
def register_user():
    email = email_entry.get() # type: ignore
    password = password_entry.get() # type: ignore
    confirm_password = confirm_password_entry.get() # type: ignore

    print("Розпочато реєстрацію...")

    # Перевірка email
    if not is_valid_email(email):
        print("Некоректний email.")
        messagebox.showerror("Помилка", "Некоректний email!")
        return
    print("Email успішно перевірено.")

    # Перевірка, чи існує email
    if email in users_db:
        print("Email вже зареєстрований.")
        messagebox.showerror("Помилка", "Користувач із таким email вже зареєстрований!")
        return
    print("Перевірка наявності email успішна.")

    # Перевірка пароля
    if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
        print("Пароль не відповідає вимогам.")
        messagebox.showerror("Помилка", "Пароль має бути не менше 8 символів з великою літерою та цифрою!")
        return
    print("Пароль успішно перевірено.")

    # Підтвердження пароля
    if password != confirm_password:
        print("Паролі не співпадають.")
        messagebox.showerror("Помилка", "Паролі не співпадають!")
        return
    print("Підтвердження пароля успішне.")

    # Хешування пароля
    hashed_password = hash_password(password).decode('utf-8')  # Декодуємо bytes у str
    users_db[email] = hashed_password
    print("Пароль хешовано та збережено у базі даних.")

    # Збереження у файл
    try:
        with open("users_db.json", "w") as file:
            json.dump(users_db, file)
        print("Дані успішно збережені у файл.")
    except Exception as e:
        print(f"Помилка під час збереження даних: {e}")
        messagebox.showerror("Помилка", "Не вдалося зберегти дані у файл!")
        return

    # Повідомлення про успіх
    print("Реєстрація завершена. Виводимо повідомлення про успіх.")
    messagebox.showinfo("Успіх", "Реєстрація успішна!")

    # Закриття вікна реєстрації
    try:
        registration_window.destroy() # type: ignore
        print("Вікно реєстрації закрито.")
    except Exception as e:
        print(f"Помилка під час закриття вікна: {e}")
    
    calc_button.config(state="normal")  # Активуємо кнопку розрахунків

# Функція для розрахунку траєкторії
def calculate_trajectory(mass, angle, height):
    g = 9.81
    angle_rad = math.radians(angle)

    # Початкова швидкість
    initial_velocity = math.sqrt(2 * g * height)

    # Час польоту
    time_of_flight = (2 * initial_velocity * math.sin(angle_rad)) / g

    # Горизонтальна відстань
    horizontal_distance = initial_velocity * math.cos(angle_rad) * time_of_flight

    # Збереження результатів у JSON
    results = {
        "initial_velocity": initial_velocity,
        "time_of_flight": time_of_flight,
        "horizontal_distance": horizontal_distance
    }
    with open("trajectory_results.json", "w") as file:
        json.dump(results, file, indent=4)

    return results

# Функція для візуалізації траєкторії
def plot_trajectory():
    with open("trajectory_results.json", "r") as file:
        data = json.load(file)

    g = 9.81
    v = data["initial_velocity"]
    angle = 45  # Приклад кута
    angle_rad = np.radians(angle) # type: ignore

    # Час та координати
    t = np.linspace(0, data["time_of_flight"], num=500) # type: ignore
    x = v * np.cos(angle_rad) * t # type: ignore
    y = x * np.tan(angle_rad) - (g * x**2) / (2 * v**2 * np.cos(angle_rad)**2) # type: ignore

    # Побудова графіка
    plt.plot(x, y) # type: ignore
    plt.title("Траєкторія польоту") # type: ignore
    plt.xlabel("Горизонтальна відстань (м)") # type: ignore
    plt.ylabel("Висота (м)") # type: ignore
    plt.grid() # type: ignore
    plt.show() # type: ignore

# Інтерфейс
def open_calculation_window():
    calc_window = tk.Toplevel(root)
    calc_window.title("Розрахунок траєкторії")

    tk.Label(calc_window, text="Маса апарату (кг):").grid(row=0, column=0, padx=5, pady=5)
    mass_entry = tk.Entry(calc_window)
    mass_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(calc_window, text="Кут спуску (°):").grid(row=1, column=0, padx=5, pady=5)
    angle_entry = tk.Entry(calc_window)
    angle_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(calc_window, text="Висота (м):").grid(row=2, column=0, padx=5, pady=5)
    height_entry = tk.Entry(calc_window)
    height_entry.grid(row=2, column=1, padx=5, pady=5)

    def calculate():
        try:
            mass = float(mass_entry.get())
            angle = float(angle_entry.get())
            height = float(height_entry.get())
            results = calculate_trajectory(mass, angle, height)
            messagebox.showinfo("Результати", f"Швидкість: {results['initial_velocity']:.2f} м/с\n"
                                              f"Час польоту: {results['time_of_flight']:.2f} с\n"
                                              f"Дальність: {results['horizontal_distance']:.2f} м")
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні значення!")

    tk.Button(calc_window, text="Розрахувати", command=calculate).grid(row=3, column=0, padx=5, pady=5)
    tk.Button(calc_window, text="Побудувати графік", command=plot_trajectory).grid(row=3, column=1, padx=5, pady=5)

def open_registration_window():
    # Створення модального вікна реєстрації
    registration_window = tk.Toplevel(root)
    registration_window.title("Реєстрація")
    registration_window.geometry("300x200")  # Розмір вікна

    # Заборона взаємодії з головним вікном
    registration_window.grab_set()  # Робимо вікно модальним
    registration_window.transient(root)  # Робимо вікно залежним від головного

    # Поля для введення email та пароля
    tk.Label(registration_window, text="Email:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    email_entry = tk.Entry(registration_window, width=25)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(registration_window, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_entry = tk.Entry(registration_window, width=25, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(registration_window, text="Confirm Password:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    confirm_password_entry = tk.Entry(registration_window, width=25, show="*")
    confirm_password_entry.grid(row=2, column=1, padx=10, pady=10)

    # Обробник реєстрації
    def register_user():
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not is_valid_email(email):
            messagebox.showerror("Помилка", "Некоректний email!")
            return

        if email in users_db:
            messagebox.showerror("Помилка", "Користувач із таким email вже зареєстрований!")
            return

        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
            messagebox.showerror("Помилка", "Пароль має бути не менше 8 символів з великою літерою та цифрою!")
            return

        if password != confirm_password:
            messagebox.showerror("Помилка", "Паролі не співпадають!")
            return

        hashed_password = hash_password(password).decode('utf-8')
        users_db[email] = hashed_password

    try:
        with open("users_db.json", "w") as file:
            json.dump(users_db, file)
        messagebox.showinfo("Успіх", "Реєстрація успішна!")
        registration_window.destroy()  # Закриваємо вікно після реєстрації
        calc_button.config(state="normal")  # Активуємо кнопку розрахунків
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти дані: {e}")

    # Кнопки
    tk.Button(registration_window, text="Register", command=register_user).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(registration_window, text="Cancel", command=registration_window.destroy).grid(row=4, column=0, columnspan=2, pady=5)

    # Центрування вікна на екрані
    registration_window.update_idletasks()
    x = (registration_window.winfo_screenwidth() - registration_window.winfo_reqwidth()) // 2
    y = (registration_window.winfo_screenheight() - registration_window.winfo_reqheight()) // 2
    registration_window.geometry(f"+{x}+{y}")

# Основне вікно
root = tk.Tk()
root.title("Система моделювання")

# Кнопка відкриття реєстрації
tk.Button(root, text="Реєстрація", command=open_registration_window).pack(pady=10)

# Кнопка для розрахунків (спочатку неактивна)
calc_button = tk.Button(root, text="Розрахунок траєкторії", command=open_calculation_window, state="disabled")
calc_button.pack(pady=10)

root.mainloop()

