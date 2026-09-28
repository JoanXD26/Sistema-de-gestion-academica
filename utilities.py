import os

# Funciones para cambiar color de texto
def reset_color():
    return "\033[0m"  # Resetea el color

def green_color():
    return "\033[92m"  # Color verde claro

def blue_color():
    return "\033[94m"  # Color azul claro

def red_color():
    return "\033[91m"  # Color rojo claro

def purple_color():
    return "\033[95m"  # Color púrpura

def cyan_color():
    return "\033[96m"  # Color cian

def borrarPantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def gotoxy(x, y):
    print(f"\033[{y};{x}H", end='')  # Mueve el cursor a la posición (x, y)
