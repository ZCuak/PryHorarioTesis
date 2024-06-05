import pywhatkit
from datetime import datetime
import time
import pyautogui
import pygetwindow as gw

def send_whatsapp_message(phone_number, message):
    # Obtener todas las ventanas abiertas
    windows = gw.getAllTitles()

    # Verificar si la ventana de WhatsApp Web ya está abierta
    whatsapp_window = None
    for window in windows:
        print(window)
        if 'WhatsApp' in window:
            whatsapp_window = window
            break

    # Si no hay una ventana de WhatsApp Web abierta, usar pywhatkit para abrir una
    if not whatsapp_window:
        seconds = time.time() + 40
        date = datetime.fromtimestamp(seconds)
        pywhatkit.sendwhatmsg(phone_number, message, date.hour, date.minute)
        time.sleep(15)  # Tiempo para abrir la ventana de WhatsApp Web
        pyautogui.press("enter")  # Pulsar "Enter" para abrir el chat
    else:
        # Seleccionar la ventana de WhatsApp Web existente
        gw.getWindowsWithTitle(whatsapp_window)[0].activate()
        print("activate")
        # Simular la selección del chat
        time.sleep(2)  # Esperar para asegurar que el chat se seleccione
        pyautogui.typewrite(message)
        pyautogui.press("enter")

        # Uso de la función
send_whatsapp_message("+51916702954", "kbro4")
print("funciono")

