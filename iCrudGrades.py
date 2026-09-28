import os
import json
from datetime import date
from clsJson import JsonFile
from components import Valida, Menu
from utilities import borrarPantalla, gotoxy, reset_color, green_color, blue_color, red_color
import time

class Nivel:
    def __init__(self, id, nivel, fecha_creacion=None, active=True):
        self.id = id
        self.nivel = nivel
        self.fecha_creacion = fecha_creacion if fecha_creacion else date.today().strftime("%Y-%m-%d")
        self.active = active

class CrudLevels:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archivos')
        self.filepath = os.path.join(self.path, 'levels.json')
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as file:
                json.dump([], file, indent=4)

    def create(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Registro de Nivel Educativo" + reset_color())

        semestre_options = [
            "1) Primer Semestre",
            "2) Segundo Semestre",
            "3) Tercer Semestre",
            "4) Cuarto Semestre",
            "5) Quinto Semestre",
            "6) Sexto Semestre",
            "7) Séptimo Semestre",
            "8) Octavo Semestre"
        ]
        
        while True:
            semestre_menu = Menu("Seleccione el Semestre al que va a ingresar", semestre_options, 50, 4)
            semestre_opc = semestre_menu.show()

            semestre_mapping = {
                '1': 'Primer Semestre',
                '2': 'Segundo Semestre',
                '3': 'Tercer Semestre',
                '4': 'Cuarto Semestre',
                '5': 'Quinto Semestre',
                '6': 'Sexto Semestre',
                '7': 'Séptimo Semestre',
                '8': 'Octavo Semestre'
            }

            semestre = semestre_mapping.get(semestre_opc)

            if semestre:
                json_file = JsonFile(self.filepath)
                levels = json_file.read()

                new_id = str(len(levels) + 1)
                new_level = {
                    "id": new_id,
                    "nivel": semestre,
                    "fecha_creacion": date.today().strftime("%Y-%m-%d"),
                    "active": "Activo"
                }
                
                levels.append(new_level)
                json_file.save(levels)
                gotoxy(30, 16); print(green_color() + "Nivel educativo registrado con éxito." + reset_color())
                time.sleep(2)
                break
            else:
                print("Error: Opción no válida. Debe ingresar un número del 1 al 8.")
                input("Presione Enter para intentar de nuevo...")
                
                
    def consult(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Consulta de Nivel Educativo" + reset_color())

        gotoxy(5, 4); print("Ingrese ID del nivel educativo a consultar: ")
        level_id = input().strip()

        json_file = JsonFile(self.filepath)
        levels = json_file.read()
        level = next((l for l in levels if l["id"] == level_id), None)
        if level:
            gotoxy(5, 6); print(f"Id: {level['id']}")
            gotoxy(5, 7); print(f"Nombre: {level['nivel']}")
            gotoxy(5, 8); print(f"Fecha de Creación: {level['fecha_creacion']}")
            gotoxy(5, 9); print(f"Estado: {level['active']}")
        else:
            gotoxy(5, 6); print("No se encontró el nivel educativo.")
        input("Presione Enter para continuar...")


    def update(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Actualizar Nivel Educativo" + reset_color())

        while True:
            gotoxy(5, 4); print("Ingrese el ID del nivel educativo: ")
            level_id = input().strip()

            json_file = JsonFile(self.filepath)
            levels = json_file.read()
            level = next((l for l in levels if l["id"] == level_id), None)

            if level:
                gotoxy(5, 6); print(f"Nombre: {level['nivel']}")
                gotoxy(5, 7); print(f"Fecha de Creación: {level['fecha_creacion']}")
                gotoxy(5, 8); print(f"Estado actual: {level['active']}")
                break
            else:
                gotoxy(5, 6); print("No se encontró el nivel educativo.")
                input("Presione Enter para intentar de nuevo...")
        
        while True:
            gotoxy(5, 10); print("¿Qué desea modificar?")
            gotoxy(5, 11); print("1. Nombre")
            gotoxy(5, 12); print("2. Estado")
            
            option = input("Seleccione una opción o (3. Para cancelar): ").strip()


            if option == '1':
                while True:
                    semestre_options = [
                        "1) Primer Semestre",
                        "2) Segundo Semestre",
                        "3) Tercer Semestre",
                        "4) Cuarto Semestre",
                        "5) Quinto Semestre",
                        "6) Sexto Semestre",  
                        "7) Séptimo Semestre",
                        "8) Octavo Semestre"
                    ]
                    
                    semestre_menu = Menu("Seleccione el Nuevo Nombre", semestre_options, 30, 4)
                    new_semestre_opc = semestre_menu.show()

                    semestre_mapping = {
                        '1': 'Primer Semestre',
                        '2': 'Segundo Semestre',
                        '3': 'Tercer Semestre',
                        '4': 'Cuarto Semestre',
                        '5': 'Quinto Semestre',
                        '6': 'Sexto Semestre',
                        '7': 'Séptimo Semestre',
                        '8': 'Octavo Semestre'
                    }

                    new_semestre = semestre_mapping.get(new_semestre_opc, None)
                    if new_semestre:
                        for l in levels:
                            if l["id"] == level_id:
                                l["nivel"] = new_semestre
                                break
                        json_file.save(levels)
                        gotoxy(5, 16); print(green_color() + "Nombre actualizado con éxito." + reset_color())
                        time.sleep(2)
                        break
                    else:
                        gotoxy(5, 16); print("Error: Opción no válida.")
                        input("Presione Enter para intentar de nuevo...")
                return

            elif option == '2':
                while True:
                    gotoxy(5, 16); print("Ingrese el nuevo estado (1 = Activo, 0 = Inactivo): ")
                    new_status = input().strip()
                    
                    if new_status in ['0', '1']:
                        new_status = "Activo" if new_status == '1' else "Inactivo"
                        for l in levels:
                            if l["id"] == level_id:
                                l["active"] = new_status
                                break
                        json_file.save(levels)
                        gotoxy(5, 18); print(green_color() + "Estado actualizado con éxito." + reset_color())
                        time.sleep(2)
                        break
                    else:
                        gotoxy(5, 16); print("Error: Ingrese 1 para Activo o 0 para Inactivo.")
                        input("Presione Enter para intentar de nuevo...")
                return

            
            elif option == '3':
                return

            else:
                gotoxy(5, 16); print("Error: Opción no válida.")
                input("Presione Enter para intentar de nuevo...")

    def delete(self):
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Eliminar Nivel Educativo" + reset_color())

        while True:
            gotoxy(5, 4); print("Ingrese ID del nivel educativo a eliminar: ")
            level_id = input().strip()

            json_file = JsonFile(self.filepath)
            levels = json_file.read()
            level = next((l for l in levels if l["id"] == level_id), None)

            if level:
                gotoxy(5, 6); print(f"Nivel educativo a eliminar:")
                gotoxy(5, 7); print(f"Nombre: {level['nivel']}")
                gotoxy(5, 8); print(f"Fecha de Creación: {level['fecha_creacion']}")

                confirm = input("¿Está seguro de que desea eliminar este nivel educativo? (s/n): ").strip()
                if confirm.lower() == 's':
                    levels = [l for l in levels if l["id"] != level_id]
                    json_file.save(levels)
                    gotoxy(5, 10); print(green_color() + "Nivel educativo eliminado con éxito." + reset_color())
                else:
                    gotoxy(5, 10); print("Eliminación cancelada.")
                break
            else:
                gotoxy(5, 6); print("No se encontró el nivel educativo.")
                break

        time.sleep(3)

