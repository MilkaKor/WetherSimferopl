import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите название города.")
        return

    try:
        url = f"http://localhost:3000?city={city}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            update_weather_display(data)
        else:
            messagebox.showerror("Ошибка", "Не удалось получить данные о погоде.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Ошибка сети: {e}")

def update_weather_display(data):
    # Очистка предыдущих данных
    for row in weather_tree.get_children():
        weather_tree.delete(row)
    
    # Добавление новых данных
    try:
        weather_tree.insert("", "end", values=(
            data["city"],
            data["temperature"],
            data["humidity"],
            data["pressure"],
            data["wind"]
        ))

        # Отображение иконки погоды
        icon_url = data.get("icon")
        if icon_url:
            response = requests.get(icon_url)
            if response.status_code == 200:
                img_data = Image.open(BytesIO(response.content))
                img_data = img_data.resize((80, 80), Image.ANTIALIAS)
                weather_icon = ImageTk.PhotoImage(img_data)
                icon_label.config(image=weather_icon)
                icon_label.image = weather_icon
            else:
                icon_label.config(image="", text="Нет иконки")
    except KeyError:
        messagebox.showerror("Ошибка", "Неверный формат данных с сервера.")

# Создание окна
root = tk.Tk()
root.title("Прогноз погоды")
root.geometry("500x400")
root.resizable(False, False)

# Поле ввода города
frame_top = ttk.Frame(root)
frame_top.pack(pady=10)

city_label = ttk.Label(frame_top, text="Введите город:", font=("Arial", 12))
city_label.pack(side="left", padx=5)

city_entry = ttk.Entry(frame_top, width=20, font=("Arial", 12))
city_entry.pack(side="left", padx=5)

get_weather_button = ttk.Button(frame_top, text="Получить погоду", command=get_weather)
get_weather_button.pack(side="left")

# Таблица для данных о погоде
columns = ("Город", "Температура (°C)", "Влажность (%)", "Давление (hPa)", "Ветер (м/с)")
weather_tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    weather_tree.heading(col, text=col, anchor="center")
    weather_tree.column(col, anchor="center", width=90)

weather_tree.pack(pady=20, fill="both", expand=True)

# Отображение иконки погоды
icon_label = ttk.Label(root, text="Иконка погоды")
icon_label.pack(pady=10)

# Подвал
footer_label = ttk.Label(root, text="Данные предоставлены OpenWeather", font=("Arial", 8), foreground="gray")
footer_label.pack(side="bottom", pady=5)

root.mainloop()
