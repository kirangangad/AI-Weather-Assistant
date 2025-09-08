import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading

API_KEY = "fae3d36b57300befb4071f452f94e64c"  # Your API key 
PROGRESS_DELAY = 40
WEATHER_STEPS = [
    "Searching Location...",
    "Analyzing Cloud Patterns...",
    "Measuring Wind Speed...",
    "Gathering Satellite Data...",
    "Checking Temperature Trends...",
    "Finalizing Forecast..."
]

def center_window(window, width, height, parent):
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def fetch_weather(city):
    """Fetch weather data from OpenWeatherMap API."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("cod") != 200:
            return None, data.get("message", "Unknown error")

        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return f"Weather in {city}:\n{weather}\n🌡 Temp: {temp}°C\n💧 Humidity: {humidity}%\n💨 Wind Speed: {wind_speed} m/s", None
    except Exception as e:
        return None, str(e)

def start_weather_forecast():
    city = entry.get().strip()
    if not city or city.lower() == "type city name here...":
        messagebox.showerror("Missing Input", "Please enter a city name.", parent=root)
        return

    progress_win = tk.Toplevel(root)
    progress_win.title("AI Weather Forecasting")
    center_window(progress_win, 400, 130, root)
    progress_win.transient(root)
    progress_win.grab_set()

    progress_label = tk.Label(progress_win, text="Initializing...", font=("Arial", 11))
    progress_label.pack(pady=10)

    progress = ttk.Progressbar(progress_win, orient=tk.HORIZONTAL, length=350, mode='determinate')
    progress.pack(pady=10)

    def run_progress(i=0):
        if i < 100:
            progress["value"] = i + 1
            step_index = (i * len(WEATHER_STEPS)) // 100
            if step_index < len(WEATHER_STEPS):
                progress_label.config(text=WEATHER_STEPS[step_index])
            root.after(PROGRESS_DELAY, lambda: run_progress(i + 1))
        else:
            # Fetch weather in a new thread to avoid UI freeze
            def get_weather():
                weather_data, error = fetch_weather(city)
                progress_win.destroy()
                if error:
                    messagebox.showerror("Error", f"Could not fetch weather: {error}", parent=root)
                else:
                    messagebox.showinfo("Forecast Ready", weather_data, parent=root)
            threading.Thread(target=get_weather, daemon=True).start()

    run_progress()

# GUI setup
root = tk.Tk()
root.title("AI Weather Forecasting")
root.geometry("400x200")

heading = tk.Label(root, text="Enter your city name:", font=("Arial", 14))
heading.pack(pady=20)

entry = tk.Entry(root, font=("Arial", 12), justify="center")
entry.pack(pady=5)
entry.insert(0, "Type city name here...")
entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END))
entry.bind("<Return>", lambda e: start_weather_forecast())

forecast_button = tk.Button(root, text="Get Forecast", font=("Arial", 12), command=start_weather_forecast)
forecast_button.pack(pady=20)

root.mainloop()

