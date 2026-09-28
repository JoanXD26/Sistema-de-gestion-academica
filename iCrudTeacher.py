import os
import time
from clsJson import JsonFile
from iCrud import ICrud
from components import Menu, Valida
from utilities import borrarPantalla, gotoxy, reset_color, green_color, blue_color, red_color

class Teacher():
    def __init__(self, teacher_id, nombre, apellido, edad, estado="activo"):
        self.teacher_id = teacher_id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.estado = estado  # Nuevo atributo de estado
        
    def __str__(self):
        return f"Teacher({self.teacher_id}, {self.nombre}, {self.apellido}, {self.edad}, {self.estado})"

    def getJson(self):
        return {
            "Id": self.teacher_id,
            "Nombre": self.nombre,
            "Apellido": self.apellido,
            "Edad": self.edad,
            "Estado": self.estado  # Incluir estado en la representación JSON
        }
    
    def nombrecompleto (self):
        return self.nombre + " " + self.apellido
        

class CrudTeachers(ICrud):
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__)) + '/archivos/teachers.json'
        self.json_file = JsonFile(self.path)
        # Inicializar el archivo JSON si no existe
        if not os.path.isfile(self.path):
            self.json_file.save([])
    
    def create(self):
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Registro del Profesor" + reset_color())
        
        while True:
            gotoxy(10, 4); print(" "*50)  # Limpiar línea para evitar superposición
            gotoxy(10, 4); teacher_id = input("Ingresar número de cédula del Profesor: ")

            # Validación del ID
            if validar.solo_numeros(teacher_id):
                teachers = self.json_file.read()
                if any(t["Id"] == teacher_id for t in teachers):
                    gotoxy(10, 5); print(red_color() + "El profesor ya está registrado. Ingrese otro ID." + reset_color())
                else:
                    break  # Si el ID no está registrado, salir del bucle
            else:
                gotoxy(10, 5); print(red_color() + "Error: Ingrese un ID válido." + reset_color())
            
            gotoxy(10, 6); input("Presione Enter para intentar de nuevo...")  # Esperar que el usuario presione Enter para continuar
            gotoxy(10, 5); print(" "*50)  # Limpiar línea del mensaje de error
            gotoxy(10, 6); print(" "*50)  # Limpiar línea del mensaje "Presione Enter..."

        # Validar y obtener el nombre
        while True:
            gotoxy(10, 5); print(" "*50)  # Limpiar línea
            gotoxy(10, 5); first_name = input("Nombre del Profesor: ")
            if validar.solo_letras(first_name) and first_name.strip():
                break
            else:
                gotoxy(10, 5); print(red_color() + "Error: El nombre debe contener solo letras y no debe estar vacío." + reset_color())
            gotoxy(10, 6); input("Presione Enter para intentar de nuevo...")
            gotoxy(10, 5); print(" "*100)  # Limpiar línea del mensaje de error
            gotoxy(10, 6); print(" "*100)  # Limpiar línea del mensaje "Presione Enter..."
            gotoxy(10, 5); print(" "*100)  # Limpiar línea del mensaje 

        # Validar y obtener el apellido
        while True:
            gotoxy(10, 6); print(" "*50)  # Limpiar línea
            gotoxy(10, 6); last_name = input("Apellido del Profesor: ")
            
            if validar.solo_letras(last_name) and last_name.strip():
                break
            else:
                gotoxy(10, 6); print(" "*50)  # Limpiar línea del campo de entrada
                gotoxy(10, 6); print(red_color() + "Error: El apellido debe contener solo letras y no debe estar vacío." + reset_color())
                
                # Esperar que el usuario presione Enter antes de continuar
                gotoxy(10, 7); input("Presione Enter para intentar de nuevo...")
                
                # Limpiar líneas después de que el usuario ha presionado Enter
                gotoxy(10, 6); print(" "*100)  # Limpiar línea del mensaje de error
                gotoxy(10, 7); print(" "*100)  # Limpiar línea del mensaje "Presione Enter..."


        # Validar y obtener la edad
        while True:
            gotoxy(10, 7); print(" "*50)  # Limpiar línea
            gotoxy(10, 7); age = input("Edad: ")
            if validar.edadVald(age):
                age = int(age)
                break
            else:
                gotoxy(10, 7); print(red_color() + "Error: La edad debe ser un número entero y que sea mayor a 0." + reset_color())
                gotoxy(10, 8); input("Presione Enter para intentar de nuevo...")
                gotoxy(10, 7); print(" "*100)  # Limpiar línea del mensaje de error
                gotoxy(10, 8); print(" "*100)  # Limpiar línea del mensaje "Presione Enter..."
        
        # Estado por defecto
        estado = "activo"
        new_teacher = Teacher(teacher_id, first_name, last_name, age, estado).getJson()
        teachers = self.json_file.read()
        teachers.append(new_teacher)
        self.json_file.save(teachers)
        gotoxy(26, 8); print(green_color() + "Profesor registrado con éxito." + reset_color())
        time.sleep(2)

    def update(self):
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Actualizar datos del Profesor" + reset_color())

        while True:
            gotoxy(10, 4); print(" "*50)  # Limpiar línea
            gotoxy(10, 4); teacher_id = input("Ingrese el ID del Profesor a Actualizar: ")

            # Validación del ID
            if validar.solo_numeros(teacher_id):
                teachers = self.json_file.read()
                teacher = next((t for t in teachers if t["Id"] == teacher_id), None)
                if teacher:
                    gotoxy(5, 6); print(f"Nombre: {teacher['Nombre']}")
                    gotoxy(5, 7); print(f"Apellido: {teacher['Apellido']}")
                    gotoxy(5, 8); print(f"Edad: {teacher['Edad']}")
                    gotoxy(5, 9); print(f"Estado: {teacher['Estado']}")
                    break
                else:
                    gotoxy(24, 6); print(red_color() + "No se encontró el profesor." + reset_color())
            else:
                gotoxy(25, 5); print(red_color() + "Error: Ingrese un ID válido." + reset_color())

            gotoxy(25, 6); input("Presione Enter para intentar de nuevo...")
            gotoxy(25, 5); print(" "*50)
            gotoxy(25, 6); print(" "*50)

        while True:
            # Menú de opciones para modificar
            gotoxy(5, 10); print(" "*50)  # Limpiar línea
            gotoxy(5, 10); print("¿Qué desea modificar?")
            gotoxy(5, 11); print("1. Nombre")
            gotoxy(5, 12); print("2. Apellido")
            gotoxy(5, 13); print("3. Edad")
            gotoxy(5, 14); print("4. Estado")  # Nueva opción para modificar el estado
            gotoxy(5, 15); option = input("Seleccione una opción (1, 2, 3 o 4): ")

            if option == '1':
                # Limpiar menú de opciones
                gotoxy(5, 10); print(" "*50)
                gotoxy(5, 11); print(" "*50)
                gotoxy(5, 12); print(" "*50)
                gotoxy(5, 13); print(" "*50)
                gotoxy(5, 14); print(" "*50)
                gotoxy(5, 15); print(" "*50)

                while True:
                    gotoxy(5, 10); print(" "*50)  # Limpiar línea
                    gotoxy(5, 11); new_first_name = input("Ingrese el nuevo nombre del Profesor: ")
                    if validar.solo_letras(new_first_name):
                        for t in teachers:
                            if t["Id"] == teacher_id:
                                t["Nombre"] = new_first_name
                                break
                        gotoxy(28, 13); print(green_color() + "Nombre actualizado con éxito." + reset_color())
                        self.json_file.save(teachers)
                        time.sleep(2)
                        break
                    else:
                        gotoxy(5, 11); print(red_color() + "Error: Ingrese solo letras." + reset_color())
                        gotoxy(5, 12); input("Presione Enter para intentar de nuevo...")
                        gotoxy(5, 11); print(" "*50)
                        gotoxy(5, 12); print(" "*50)

                return  # Regresar al menú principal de profesores

            elif option == '2':
                # Limpiar menú de opciones
                gotoxy(5, 10); print(" "*50)
                gotoxy(5, 11); print(" "*50)
                gotoxy(5, 12); print(" "*50)
                gotoxy(5, 13); print(" "*50)
                gotoxy(5, 14); print(" "*50)
                gotoxy(5, 15); print(" "*50)

                while True:
                    gotoxy(5, 10); print(" "*50)  # Limpiar línea
                    gotoxy(5, 11); new_last_name = input("Ingrese el nuevo apellido del Profesor: ")
                    if validar.solo_letras(new_last_name):
                        for t in teachers:
                            if t["Id"] == teacher_id:
                                t["Apellido"] = new_last_name
                                break
                        gotoxy(28, 13); print(green_color() + "Apellido actualizado con éxito." + reset_color())
                        self.json_file.save(teachers)
                        time.sleep(2)
                        break
                    else:
                        gotoxy(5, 11); print(red_color() + "Error: Ingrese solo letras." + reset_color())
                        gotoxy(5, 12); input("Presione Enter para intentar de nuevo...")
                        gotoxy(5, 11); print(" "*50)
                        gotoxy(5, 12); print(" "*50)

                return  # Regresar al menú principal de profesores

            elif option == '3':
                # Limpiar menú de opciones
                gotoxy(5, 10); print(" "*50)
                gotoxy(5, 11); print(" "*50)
                gotoxy(5, 12); print(" "*50)
                gotoxy(5, 13); print(" "*50)
                gotoxy(5, 14); print(" "*50)
                gotoxy(5, 15); print(" "*50)

                while True:
                    gotoxy(5, 10); print(" "*50)  # Limpiar línea de entrada para la edad
                    gotoxy(5, 11); new_age = input("Ingrese la nueva edad del Profesor: ")

                    if validar.edadVald(new_age):
                        new_age = int(new_age)
                        for t in teachers:
                            if t["Id"] == teacher_id:
                                t["Edad"] = new_age
                                break
                        gotoxy(28, 13); print(green_color() + "Edad actualizada con éxito." + reset_color())
                        self.json_file.save(teachers)
                        time.sleep(2)
                        break
                    else:
                        gotoxy(5, 11); print(red_color() + "Error: La edad debe ser un numero entero y mayor a 0." + reset_color())
                        gotoxy(5, 12); input("Presione Enter para intentar de nuevo...")
                        gotoxy(5, 11); print(" "*100)  # Limpiar línea del mensaje de error
                        gotoxy(5, 12); print(" "*100)  # Limpiar línea del mensaje "Presione Enter..."
                        gotoxy(5, 16); print(" "*100)  # Limpiar línea de entrada para la edad

                return  # Regresar al menú principal de profesores

            elif option == '4':
                # Limpiar menú de opciones
                gotoxy(5, 10); print(" "*50)
                gotoxy(5, 11); print(" "*50)
                gotoxy(5, 12); print(" "*50)
                gotoxy(5, 13); print(" "*50)
                gotoxy(5, 14); print(" "*50)
                gotoxy(5, 15); print(" "*50)

                while True:
                    gotoxy(5, 10); print(" "*50)  # Limpiar línea
                    gotoxy(5, 11); new_status = input("Ingrese el nuevo estado del Profesor (1 = Activo, 0 = Inactivo): ")

                    if new_status in ['0', '1']:
                        # Convertir la entrada en estado
                        estado = "Activo" if new_status == '1' else "Inactivo"

                        # Actualizar el estado del profesor en el diccionario
                        for t in teachers:
                            if t["Id"] == teacher_id:
                                t["Estado"] = estado
                                break

                        gotoxy(28, 13); print(green_color() + f"Estado actualizado a {estado.upper()}." + reset_color())
                        self.json_file.save(teachers)
                        time.sleep(2)
                        break
                    else:
                        gotoxy(5, 11); print(red_color() + "Error: seleccione 1 = Activo, 0 = Inactivo." + reset_color())
                        gotoxy(5, 12); input("Presione Enter para intentar de nuevo...")
                        gotoxy(5, 11); print(" "*50)
                        gotoxy(5, 12); print(" "*50)

                return  # Regresar al menú principal de profesores

            else:
                # Opción no válida: mostrar error, esperar Enter, y luego limpiar
                gotoxy(24, 15); print(red_color() + "Opción no válida. Intente de nuevo." + reset_color())
                gotoxy(24, 16); input("Presione Enter para continuar...")  # Esperar antes de limpiar
                gotoxy(24, 15); print(" " * 50)  # Limpiar mensaje de error
                gotoxy(24, 16); print(" " * 50)  # Limpiar input "Presione Enter para continuar..."
                gotoxy(5, 14); print(" "*50)  # Limpiar solo el área del mensaje de error sin tocar el menú
                continue  # Reiniciar el input de la opción sin mostrar el menú nuevamente


    def consult(self):
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Consulta de Profesores" + reset_color())
        gotoxy(5, 4); teacher_id = input("Ingrese el ID del Profesor a Consultar (dejar en blanco para listar todos): ")
        
        teachers = self.json_file.read()
        if teacher_id:
            if validar.solo_numeros(teacher_id):  # Verificar que el ID ingresado sea válido
                teacher = next((t for t in teachers if t["Id"] == teacher_id), None)
                if teacher:
                    gotoxy(5, 6); print(f"Profesor encontrado: {teacher}")
                else:
                    gotoxy(5, 6); print(red_color() + "Profesor no encontrado." + reset_color())
            else:
                gotoxy(5, 6); print(red_color() + "Error: Ingrese un ID válido." + reset_color())
        else:
            if not teachers:
                gotoxy(5, 6); print("No hay profesores registrados.")
            else:
                for i, teacher in enumerate(teachers):
                    gotoxy(5, 6 + i); print(teacher)

        gotoxy(5, 6 + len(teachers) + 2); input("Presione una tecla para continuar...")

            
    def delete(self):
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Eliminar Profesor" + reset_color())

        while True:
            gotoxy(5, 4); print(" "*50)  # Limpiar línea
            gotoxy(5, 4); teacher_id = input("Ingrese ID del Profesor a Eliminar: ")

            # Validación del ID
            if validar.solo_numeros(teacher_id):
                teachers = self.json_file.read()
                teacher = next((t for t in teachers if t["Id"] == teacher_id), None)
                if teacher:
                    gotoxy(5, 6); print(f"Profesor a eliminar:")
                    gotoxy(5, 7); print(f"Nombre: {teacher['Nombre']}")
                    gotoxy(5, 8); print(f"Apellido: {teacher['Apellido']}")
                    gotoxy(5, 9); print(f"Edad: {teacher['Edad']}")
                    gotoxy(5, 10); print(f"Estado: {teacher['Estado']}")

                    # Confirmar eliminación
                    gotoxy(5, 12); confirm = input("¿Está seguro de que desea eliminar este profesor? (s/n): ")
                    if confirm.lower() == 's':
                        teachers = [t for t in teachers if t["Id"] != teacher_id]
                        self.json_file.save(teachers)
                        gotoxy(25, 13); print(green_color() + "Profesor eliminado con éxito." + reset_color())
                    else:
                        gotoxy(25, 13); print(red_color() + "Eliminación cancelada." + reset_color())
                    break  # Salir del bucle una vez que se ha realizado la acción
                else:
                    gotoxy(26, 6); print(red_color() + "No se encontró el profesor." + reset_color())
                    break  # Salir del bucle si el profesor no se encuentra
            else:
                gotoxy(25, 5); print(red_color() + "Error: Ingrese un ID válido." + reset_color())
                gotoxy(25, 6); input("Presione Enter para intentar de nuevo...")
                gotoxy(25, 5); print(" "*50)
                gotoxy(25, 6); print(" "*50)

        time.sleep(2)
