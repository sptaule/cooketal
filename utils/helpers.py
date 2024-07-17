import os
import datetime
import tkinter as tk
import customtkinter as ctk
import ctypes
import screeninfo
from CTkMessagebox import CTkMessagebox
from PIL import Image


def get_scaling_factor():
    # Load the user32.dll
    user32 = ctypes.windll.user32

    # Get the screen DPI
    hdc = user32.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 is the index for LOGPIXELSX
    user32.ReleaseDC(0, hdc)

    # Calculate the scaling factor
    scaling_factor = dpi / 96  # 96 DPI is the default DPI for 100% scaling

    return scaling_factor


def center_geometry(width: int, height: int):
    # Utiliser les dimensions de l'écran
    screen_width, screen_height = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
    scaling_factor = get_scaling_factor()
    x = int(((screen_width / 2) - (width / 2)) * scaling_factor)
    y = int(((screen_height / 2) - (height / 2)) * scaling_factor)

    return f"{width}x{height}+{x}+{y}"


def get_icon(name: str, ext: str = "png", return_path: bool = False):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if return_path:
        return os.path.abspath(os.path.join(root_dir, 'assets', 'images', f"{name}.{ext}"))

    icon = ctk.CTkImage(
        light_image=Image.open(os.path.abspath(os.path.join(root_dir, 'assets', 'images', f"{name}.{ext}"))),
        dark_image=Image.open(os.path.abspath(os.path.join(root_dir, 'assets', 'images', f"{name}.{ext}")))
    )
    return icon


def convert_float_to_int_if_zero(float_num):
    if float(float_num).as_integer_ratio()[1] == 1:
        return int(float_num)
    else:
        return float_num


def alert(message: str):
    """Display an alert popup"""
    return CTkMessagebox(
        title="Erreur",
        message=message,
        icon="",
        button_width=375,
        option_focus=1,
        fade_in_duration=200
    )


def success(message: str):
    """Display a success popup"""
    return CTkMessagebox(
        title="Succès",
        message=message,
        icon="check",
        button_width=375,
        option_focus=1,
        fade_in_duration=200
    )


def confirm_deletion_popup(message: str):
    return CTkMessagebox(
        title="Suppression",
        message=message,
        icon="",
        button_width=375,
        option_1="Non",
        option_2="Oui",
        fade_in_duration=200
    )


def data_list(master):
    return tk.Listbox(
            master=master,
            width=50,
            height=20,
            font=ctk.CTkFont(size=14),
            bg="#313131",
            fg="#EBEBEB",
            bd=0,
            relief="flat",
            selectbackground="#313131",
            selectforeground="#51A3A3",
            highlightcolor="#313131",
            borderwidth=0,
            highlightthickness=16,
            highlightbackground="#313131",
            activestyle="none"
    )


def format_date_fr(date):
    weekdays = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"}
    months = {
        1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
        7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
    }
    return weekdays[date.weekday()] + ", " + date.strftime("%d ") + months[date.month] + " " + date.strftime("%Y")


def format_date_str(date_str):
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    weekdays = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"}
    return f"{weekdays[date_obj.weekday()]} {date_obj.strftime('%d/%m/%Y')}"


def calculate_days_between_dates(date1_str, date2_str):
    date1 = datetime.datetime.strptime(date1_str, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2_str, "%Y-%m-%d")
    days_difference = (date2 - date1).days + 1
    if days_difference == 1:
        return "1 jour"
    else:
        return f"{days_difference} jours"


def is_time_of_day(date_str, time_of_day):
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    current_time = datetime.datetime.now().time()
    if date_obj.date() != datetime.datetime.now().date():
        return False
    if time_of_day == "Midi":
        return datetime.time(0, 0, 0) <= current_time < datetime.time(13, 0, 0)
    elif time_of_day == "Soir":
        return datetime.time(13, 0, 1) <= current_time <= datetime.time(23, 59, 59)
    else:
        return False


def get_date(delta=0):
    today = datetime.date.today()
    date_with_delta = today + datetime.timedelta(days=delta)
    day = date_with_delta.day
    month = date_with_delta.month
    year = date_with_delta.year
    return day, month, year


def check_widget_type(widget):
    if isinstance(widget, tk.Label):
        return tk.Label
    elif isinstance(widget, ctk.CTkCanvas):
        return ctk.CTkCanvas
    else:
        return None
