import os
import json
from datetime import date
from uuid import uuid4  # Para generar UUID si prefieres ese enfoque
from utilities import borrarPantalla, gotoxy, reset_color, green_color, blue_color, red_color
import time

path = 'archivos'

class Periodo:
    def __init__(self, id, inicio_semestre, fin_semestre, active):
        self.id = id  # Identificador único para el periodo.
        self.inicio_semestre = inicio_semestre  # Fecha de inicio del semestre.
        self.fin_semestre = fin_semestre  # Fecha de fin del semestre.
        self.fecha_creacion = str(date.today())  # Convertir fecha a cadena para JSON.
        self.active = active  # Estado de actividad del periodo (True o False).

class CrudPeriodos:
    def __init__(self):
        if not os.path.exists(path):
            os.makedirs(path)
        self.filepath = path + '/periodos.json'
        self.counter_filepath = path + '/counter.json'

        # Inicializar el contador si no existe
        if not os.path.exists(self.counter_filepath):
            with open(self.counter_filepath, 'w') as file:
                json.dump({'counter': 0}, file)  # Contador inicializado a 0

    def _read_data(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as file:
                json.dump([], file)  # Crear archivo vacío con una lista vacía
            return []

        with open(self.filepath, 'r') as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def _get_next_id(self):
        # Leer el contador
        with open(self.counter_filepath, 'r') as file:
            counter_data = json.load(file)
        
        next_id = counter_data['counter'] + 1

        # Actualizar el contador
        with open(self.counter_filepath, 'w') as file:
            json.dump({'counter': next_id}, file)

        return next_id

    def create(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Registro de Periodo Académico" + reset_color())

        periodos = self._read_data()

        # Generar un nuevo ID automáticamente
        periodo_id = self._get_next_id()

        # Ingreso de la fecha de inicio del semestre
        gotoxy(10, 6); inicio_semestre = input("Ingrese la fecha de inicio del semestre (YYYY-MM-DD): ")

        # Ingreso de la fecha de fin del semestre
        gotoxy(10, 7); fin_semestre = input("Ingrese la fecha de fin del semestre (YYYY-MM-DD): ")

        periodo_activo = True

        nuevo_periodo = Periodo(periodo_id, inicio_semestre, fin_semestre, periodo_activo).__dict__

        periodos.append(nuevo_periodo)
        self._save_data(periodos)

        gotoxy(26, 9); print(green_color() + "Periodo registrado con éxito." + reset_color())
        time.sleep(2)
    
    
    def consult(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Consulta de Periodo Académico" + reset_color())

        periodos = self._read_data()

        gotoxy(10, 4); periodo_id = input("Ingrese el identificador único del periodo: ").strip()
        periodo = next((p for p in periodos if str(p['id']) == periodo_id), None)

        if periodo:
            gotoxy(10, 5); print(f"ID: {periodo['id']}")
            gotoxy(10, 6); print(f"Fecha de Inicio: {periodo['inicio_semestre']}")
            gotoxy(10, 7); print(f"Fecha de Fin: {periodo['fin_semestre']}")
            gotoxy(10, 8); print(f"Fecha de Creación: {periodo['fecha_creacion']}")
            gotoxy(10, 9); print(f"Estado: {'Activo' if periodo['active'] else 'Inactivo'}")
        else:
            gotoxy(26, 6); print(red_color() + "No se encontró el periodo." + reset_color())

        gotoxy(10, 11); input("Presione Enter para continuar...")


    def update(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Actualizar Periodo Académico" + reset_color())

        periodos = self._read_data()

        gotoxy(10, 4); periodo_id =input("Ingrese el identificador único del periodo: ").strip()
        periodo = next((p for p in periodos if str(p['id']) == periodo_id), None)

        if periodo:
            while True:
                borrarPantalla()
                gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
                gotoxy(30, 2); print(blue_color() + "Modificar Periodo Académico" + reset_color())
                gotoxy(10, 4); print("1. Cambiar fecha de inicio")
                gotoxy(10, 5); print("2. Cambiar fecha de fin")
                gotoxy(10, 6); print("3. Cambiar estado")
                gotoxy(10, 7); print("4. Salir")
                gotoxy(10, 8); opcion = input("Seleccione una opción (1-4): ")

                if opcion == '1':
                    gotoxy(10, 9); nueva_fecha_inicio = input(f"Fecha de inicio actual ({periodo['inicio_semestre']}): ")
                    if nueva_fecha_inicio.strip():
                        periodo['inicio_semestre'] = nueva_fecha_inicio
                    gotoxy(26, 11); print(green_color() + "Fecha de inicio actualizada con éxito." + reset_color())
                    time.sleep(2)

                elif opcion == '2':
                    gotoxy(10, 9); nueva_fecha_fin = input(f"Fecha de fin actual ({periodo['fin_semestre']}): ")
                    if nueva_fecha_fin.strip():
                        periodo['fin_semestre'] = nueva_fecha_fin
                    gotoxy(26, 11); print(green_color() + "Fecha de fin actualizada con éxito." + reset_color())
                    time.sleep(2)

                elif opcion == '3':
                    gotoxy(10, 9); nuevo_estado = input("Ingrese el nuevo estado (1 = Activo, 0 = Inactivo): ")
                    periodo['active'] = True if nuevo_estado == '1' else False
                    gotoxy(26, 11); print(green_color() + "Estado actualizado con éxito." + reset_color())
                    time.sleep(2)

                elif opcion == '4':
                    break

                else:
                    gotoxy(26, 11); print(red_color() + "Opción no válida. Intente nuevamente." + reset_color())
                    time.sleep(2)

            self._save_data(periodos)

        else:
            gotoxy(26, 6); print(red_color() + "No se encontró el periodo." + reset_color())

        time.sleep(2)

    def delete(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Eliminar Periodo Académico" + reset_color())

        periodos = self._read_data()
        
        if not periodos:
            gotoxy(26, 6); print(red_color() + "No hay periodos registrados." + reset_color())
            time.sleep(2)
            return

        gotoxy(10, 4); periodo_id = input("Ingrese el identificador único del periodo: ").strip()
        periodo = next((p for p in periodos if str(p['id']) == periodo_id), None)

        if periodo:
            # Filtrar la lista para eliminar el período con el ID dado
            periodos_actualizados = [p for p in periodos if str(p['id']) != periodo_id]
            self._save_data(periodos_actualizados)
            gotoxy(26, 6); print(green_color() + "Periodo eliminado con éxito." + reset_color())
        else:
            gotoxy(26, 6); print(red_color() + "No se encontró el periodo." + reset_color())

        time.sleep(2)



