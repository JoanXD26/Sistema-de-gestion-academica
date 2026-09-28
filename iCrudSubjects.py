import json
import os
from datetime import date
from clsJson import JsonFile
from components import Menu
from utilities import borrarPantalla, gotoxy, reset_color, green_color, blue_color, red_color

class Asignatura:
    def __init__(self, id, descripcion, nivel, active, profesor=None, fecha_creacion=None):
        self.id = id
        self.descripcion = descripcion
        self.nivel = nivel
        self.profesor = profesor  # Almacenar nombre completo del profesor
        self.fecha_creacion = fecha_creacion if fecha_creacion else str(date.today())
        self.active = active

    def to_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'nivel': self.nivel,
            'profesor': self.profesor,  # Almacenar nombre completo del profesor
            'fecha_creacion': self.fecha_creacion,
            'active': self.active
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            descripcion=data['descripcion'],
            nivel=data['nivel'],
            profesor=data.get('profesor'),  # Obtener el nombre completo del profesor
            active=data['active'],
            fecha_creacion=data.get('fecha_creacion')
        )

    def get_nivel(self):
        nivel_map = {
            'Primer': 'PRIMER SEMESTRE',
            'Segundo': 'SEGUNDO SEMESTRE',
            'Tercer': 'TERCER SEMESTRE',
            'Cuarto': 'CUARTO SEMESTRE',
            'Quinto': 'QUINTO SEMESTRE',
            'Sexto': 'SEXTO SEMESTRE',
            'Séptimo': 'SÉPTIMO SEMESTRE',
            'Octavo': 'OCTAVO SEMESTRE'
        }
        return nivel_map.get(self.nivel, 'Error ingrese una opción válida')

    def __str__(self):
        estado = "Activo" if self.active else "Inactivo"
        return f"ID: {self.id} | Asignatura: {self.descripcion} | Nivel: {self.get_nivel()} | Profesor: {self.profesor} | Estado: {estado} | Creada el: {self.fecha_creacion}"

class CrudSubjects:
    def __init__(self, filepath='asignaturas.json', teachers_filepath='teachers.json'):
        self.path = 'archivos'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        self.filepath = os.path.join(self.path, filepath)
        self.teachers_filepath = os.path.join(self.path, teachers_filepath)
        self.json_file = JsonFile(self.filepath)
        self.teachers_file = JsonFile(self.teachers_filepath)
        self.subjects = self.load_subjects()
        self.teachers = self.load_teachers()
        self.next_id = self.get_next_id()

    def load_subjects(self):
        try:
            data = self.json_file.read()
            return [Asignatura.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_subjects(self):
        data = [subject.to_dict() for subject in self.subjects]
        self.json_file.save(data)

    def load_teachers(self):
        try:
            data = self.teachers_file.read()
            # Crear un diccionario de nombre -> apellido
            return {item['Nombre'].strip().lower(): item['Apellido'].strip() for item in data}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def get_next_id(self):
        if self.subjects:
            return max(subject.id for subject in self.subjects) + 1
        return 1

    def create(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Registro de la Asignatura" + reset_color())
        
        gotoxy(5, 4); descripcion = input("Ingrese el nombre de la materia: ")

        semestre_menu = Menu(
            titulo="¿A qué nivel pertenece la materia?",
            opciones=["1) Primer Semestre", "2) Segundo Semestre", "3) Tercer Semestre", "4) Cuarto Semestre", 
                    "5) Quinto Semestre", "6) Sexto Semestre", "7) Séptimo Semestre", "8) Octavo Semestre"],
            x=30, y=6
        )

        opc = semestre_menu.show()
        opciones_nivel = {
            '1': "Primer",
            '2': "Segundo",
            '3': "Tercer",
            '4': "Cuarto",
            '5': "Quinto",
            '6': "Sexto",
            '7': "Séptimo",
            '8': "Octavo"
        }

        nivel = opciones_nivel.get(opc, None)
        
        if nivel is None:
            print("Opción de semestre no válida. Intente de nuevo.")
            return

        while True:
            gotoxy(5, 8); profesor_nombre = input("Ingrese el nombre del profesor encargado: ").strip().lower()
            if profesor_nombre in self.teachers:
                profesor_apellido = self.teachers[profesor_nombre]
                profesor_completo = f"{profesor_nombre.capitalize()} {profesor_apellido.capitalize()}"
                break
            else:
                gotoxy(5, 8); print(red_color() + "El nombre del profesor no está registrado. Intente de nuevo." + reset_color())

        gotoxy(5, 12); active = input("¿Está activa la asignatura? (S/N): ").strip().lower() == 's'
        
        nueva_asignatura = Asignatura(self.next_id, descripcion, nivel, active, profesor_completo)
        self.subjects.append(nueva_asignatura)
        self.save_subjects()
        self.next_id += 1

        gotoxy(20, 14); print(green_color() + f"Asignatura '{descripcion.upper()}' registrada con éxito." + reset_color())
        gotoxy(20, 16); input("Presione Enter para volver al menú...")

    # Los métodos consult, update y delete permanecen igual.


    def consult(self):
        while True:
            borrarPantalla()
            gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
            gotoxy(30, 2); print(blue_color() + "Consulta de la Asignatura" + reset_color())

            gotoxy(5, 4); descripcion = input("Ingrese el nombre de la materia: ")

            materia = next((subj for subj in self.subjects if subj.descripcion.lower() == descripcion.lower()), None)

            if materia:
                gotoxy(5, 6); print(f"Materia: {materia.descripcion.upper()} | Nivel: {materia.get_nivel()} | Profesor: {materia.profesor} | Estado: {'ACTIVO' if materia.active else 'INACTIVO'}")
                gotoxy(5, 8); input("Presione Enter para continuar...")
                return
            else:
                gotoxy(5, 6); print(red_color() + "No se encontró la materia." + reset_color())
                gotoxy(5, 8); input("Presione Enter para continuar...")
                
    def update(self):
        while True:
            borrarPantalla()
            gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
            gotoxy(30, 2); print(blue_color() + "Actualizar Materia" + reset_color())
            
            gotoxy(5, 4); descripcion = input("Ingrese el nombre de la asignatura a modificar: ").strip().lower()

            subject = next((subj for subj in self.subjects if subj.descripcion.lower() == descripcion), None)

            if subject:
                while True:
                    borrarPantalla()
                    gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
                    gotoxy(30, 2); print(blue_color() + f"Editar Asignatura: {subject.descripcion.upper()}" + reset_color())
                    
                    gotoxy(5, 4); print("¿Qué desea editar?")
                    gotoxy(5, 5); print("1) Nivel educativo")
                    gotoxy(5, 6); print("2) Estado (Activo/Inactivo)")
                    gotoxy(5, 7); print("3) Profesor encargado")
                    gotoxy(5, 8); print("4) Cancelar")
                    
                    gotoxy(5, 10); opcion = input("Seleccione una opción (1-4): ").strip()

                    if opcion == '1':
                        while True:
                            borrarPantalla()
                            gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
                            gotoxy(30, 2); print(blue_color() + "Actualizar nivel educativo" + reset_color())
                            gotoxy(5, 4); print("1) Primer Semestre")
                            gotoxy(5, 5); print("2) Segundo Semestre")
                            gotoxy(5, 6); print("3) Tercer Semestre")
                            gotoxy(5, 7); print("4) Cuarto Semestre")
                            gotoxy(5, 8); print("5) Quinto Semestre")
                            gotoxy(5, 9); print("6) Sexto Semestre")
                            gotoxy(5, 10); print("7) Séptimo Semestre")
                            gotoxy(5, 11); print("8) Octavo Semestre")
                            
                            gotoxy(5, 13); nuevo_nivel_opc = input("Seleccione una opción (1-8): ").strip()

                            opciones_nivel = {
                                '1': "Primer",
                                '2': "Segundo",
                                '3': "Tercer",
                                '4': "Cuarto",
                                '5': "Quinto",
                                '6': "Sexto",
                                '7': "Séptimo",
                                '8': "Octavo"
                            }

                            nuevo_nivel = opciones_nivel.get(nuevo_nivel_opc)

                            if nuevo_nivel:
                                subject.nivel = nuevo_nivel
                                gotoxy(30, 15); print(green_color() + f"Nivel actualizado a {subject.get_nivel()}" + reset_color())
                                gotoxy(30, 17); input("Presione Enter para continuar...")
                                self.save_subjects()
                                break
                            else:
                                gotoxy(30, 15); print(red_color() + "Opción no válida. Intente de nuevo." + reset_color())
                                gotoxy(30, 17); input("Presione Enter para intentar nuevamente...")
                        break
                    
                    elif opcion == '2':
                        while True:
                            borrarPantalla()
                            gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
                            gotoxy(30, 2); print(blue_color() + "Actualizar estado de la materia" + reset_color())
                            
                            gotoxy(5, 4); nuevo_estado = input(f"Ingrese el nuevo estado (1 = Activo, 0 = Inactivo): ").lower()
                            if nuevo_estado in ['0', '1']:
                                subject.active = (nuevo_estado == '1')
                                estado = "Activo" if subject.active else "Inactivo"
                                gotoxy(30, 6); print(green_color() + f"Estado actualizado a {estado.upper()}." + reset_color())
                                self.save_subjects()
                                gotoxy(30, 8); input("Presione Enter para continuar...")
                                break
                            else:
                                gotoxy(5, 8); print(red_color() + "Error seleccione 1 = Activo, 0 = Inactivo." + reset_color())
                                gotoxy(5, 10); input("Presione Enter para intentar nuevamente...")
                        break
                    
                    elif opcion == '3':
                        while True:
                            borrarPantalla()
                            gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
                            gotoxy(30, 2); print(blue_color() + "Actualizar profesor encargado" + reset_color())
                            
                            while True:
                                gotoxy(5, 8); profesor_nombre = input("Ingrese el nombre del nuevo profesor encargado: ").strip().lower()
                                if profesor_nombre in self.teachers:
                                    profesor_apellido = self.teachers[profesor_nombre]
                                    profesor_completo = f"{profesor_nombre.capitalize()} {profesor_apellido.capitalize()}"
                                    subject.profesor = profesor_completo
                                    gotoxy(30, 15); print(green_color() + f"Profesor actualizado a {profesor_completo}." + reset_color())
                                    self.save_subjects()
                                    gotoxy(30, 17); input("Presione Enter para continuar...")
                                    break
                                else:
                                    gotoxy(5, 8); print(red_color() + "El nombre del profesor no está registrado. Intente de nuevo." + reset_color())
                            break
                    
                    elif opcion == '4':
                        return
                    
                    else:
                        gotoxy(5, 11); print(red_color() + "Opción no válida. Intente de nuevo." + reset_color())
                        gotoxy(5, 13); input("Presione Enter para continuar...")
                        
            else:
                gotoxy(5, 6); print(red_color() + "Asignatura no encontrada." + reset_color())
                gotoxy(5, 8); input("Presione Enter para continuar...")

            return

    def delete(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Eliminar Asignatura" + reset_color())
        gotoxy(5, 4); descripcion = input("Ingrese el nombre de la materia a eliminar: ").strip().lower()

        subject = next((subj for subj in self.subjects if subj.descripcion.lower() == descripcion), None)

        if subject:
            self.subjects.remove(subject)
            self.save_subjects()
            gotoxy(5, 6); print(green_color() + f"Asignatura '{subject.descripcion.upper()}' eliminada con éxito." + reset_color())
            gotoxy(5, 8); input("Presione Enter para continuar...")
        else:
            gotoxy(5, 6); print(red_color() + f"Asignatura no encontrada." + reset_color())
            gotoxy(5, 8); input("Presione Enter para continuar...")
