from components import Menu, Valida
from utilities import borrarPantalla, gotoxy, reset_color, green_color, blue_color, red_color
from clsJson import JsonFile
from iCrud import ICrud
from datetime import datetime
import time

path = 'archivos'

class CrudStudents(ICrud):
    def create(self):
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Registro del Estudiante" + reset_color())

        json_file = JsonFile(path + '/students.json')

        while True:
            gotoxy(10, 4); print(" "*50)  # Limpiar línea para evitar superposición
            gotoxy(10, 4); student_id = input("Ingrese el número de cédula: ")

            # Validación del ID
            if validar.solo_numeros(student_id) and len(student_id) == 10:
                students = json_file.read()
                if json_file.find("id", student_id):
                    gotoxy(10, 5); print(red_color() + "El estudiante ya está registrado. Ingrese otro ID." + reset_color())
                else:
                    break  # Si el ID no está registrado, salir del bucle
            else:
                gotoxy(10, 5); print(red_color() + "Error: Ingrese 10 números." + reset_color())
            
            gotoxy(10, 6); input("Presione Enter para intentar de nuevo...")  # Esperar que el usuario presione Enter para continuar
            gotoxy(10, 5); print(" "*50)  # Limpiar línea del mensaje de error
            gotoxy(10, 6); print(" "*50)  # Limpiar línea del mensaje "Presione Enter..."

        while True:
            gotoxy(10, 5); print(" "*50)  # Limpiar línea para evitar superposición
            gotoxy(10, 5); nombre = input("Ingrese el nombre del estudiante: ")
            gotoxy(10, 6); print(" "*50)  # Limpiar línea para evitar superposición
            gotoxy(10, 6); apellido = input("Ingrese el apellido del estudiante: ")
            
            # Validación
            if validar.solo_letras(nombre) and validar.solo_letras(apellido):
                break  # Si la validación es correcta, salir del bucle
            else:
                gotoxy(10, 5); print(red_color() + "Error: Ingrese solo letras para nombre y apellido." + reset_color())  # Mensaje de error
                gotoxy(10, 6); input("Presione Enter para intentar de nuevo...")  # Esperar que el usuario presione Enter para continuar
                gotoxy(10, 5); print(" "*50)  # Limpiar línea del mensaje de error
                gotoxy(10, 6); print(" "*50)  # Limpiar línea del mensaje "Presione Enter..."

        # Agregar la fecha de registro y estado del estudiante
        fecha_registro = datetime.now().strftime("%Y-%m-%d Hora: %H:%M:%S")
        estado = True  # El estudiante está activo por defecto

        new_student = {
            "id": student_id, 
            "nombre": nombre, 
            "apellido": apellido, 
            "fecha_registro": fecha_registro,
            "estado": estado
        }
        
        students.append(new_student)
        json_file.save(students)
        gotoxy(26, 8); print(green_color() + "Estudiante registrado con éxito." + reset_color())

        time.sleep(3)

    def update(self):
        validar = Valida()
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Actualizar datos del estudiante" + reset_color())

        while True:
            gotoxy(10, 4); print(" "*50)  # Limpiar la línea
            gotoxy(10, 4); student_id = input("Ingrese el número de cédula: ")

            # Validación del ID
            if validar.solo_numeros(student_id) and len(student_id) == 10:
                json_file = JsonFile(path + '/students.json')
                students = json_file.read()
                student = json_file.find("id", student_id)
                if student:
                    student = student[0]
                    nombre_mayusculas = student['nombre'].upper()
                    apellido_mayusculas = student['apellido'].upper()
                    gotoxy(5, 6); print(f"Nombre: {nombre_mayusculas}")
                    gotoxy(5, 7); print(f"Apellido: {apellido_mayusculas}")
                    gotoxy(5, 8); print(f"Estado actual: {'Activo' if student['estado'] else 'Inactivo'}")
                    break
                else:
                    gotoxy(24, 6); print(red_color() + "No se encontró el estudiante." + reset_color())
            else:
                gotoxy(25, 5); print(red_color() + "Error: Ingrese solo números de 10 dígitos." + reset_color())

            gotoxy(25, 6); input("Presione Enter para intentar de nuevo...")
            gotoxy(25, 5); print(" "*50)
            gotoxy(25, 6); print(" "*50)

        while True:
            # Menú de opciones para modificar
            gotoxy(5, 9); print("¿Qué desea modificar?")
            gotoxy(5, 10); print("1. Nombre")
            gotoxy(5, 11); print("2. Apellido")
            gotoxy(5, 12); print("3. Estado")
            gotoxy(5, 14); option = input("Seleccione una opción (1, 2 o 3): ")

            if option == '1':
                while True:
                    gotoxy(5, 15); print(" "*50)  # Limpiar línea para evitar superposición
                    gotoxy(5, 15); nuevo_nombre = input("Ingrese el nuevo nombre del estudiante: ")
                    if validar.solo_letras(nuevo_nombre):
                        nuevo_nombre_mayusculas = nuevo_nombre.upper()
                        for s in students:
                            if s["id"] == student_id:
                                s["nombre"] = nuevo_nombre_mayusculas
                                break
                        gotoxy(28, 17); print(green_color() + "Nombre actualizado con éxito." + reset_color())
                        json_file.save(students)
                        time.sleep(3)
                        break
                    else:
                        gotoxy(5, 16); print(red_color() + "Error: Ingrese solo letras." + reset_color())
                        gotoxy(5, 17); input("Presione Enter para intentar de nuevo...")
                        gotoxy(5, 16); print(" "*50)
                        gotoxy(5, 17); print(" "*50)

                return  # Regresar al menú principal de estudiantes

            elif option == '2':
                while True:
                    gotoxy(5, 15); print(" "*50)  # Limpiar línea para evitar superposición
                    gotoxy(5, 15); nuevo_apellido = input("Ingrese el nuevo apellido del estudiante: ")
                    if validar.solo_letras(nuevo_apellido):
                        nuevo_apellido_mayusculas = nuevo_apellido.upper()
                        for s in students:
                            if s["id"] == student_id:
                                s["apellido"] = nuevo_apellido_mayusculas
                                break
                        gotoxy(28, 17); print(green_color() + "Apellido actualizado con éxito." + reset_color())
                        json_file.save(students)
                        time.sleep(3)
                        break
                    else:
                        gotoxy(5, 16); print(red_color() + "Error: Ingrese solo letras." + reset_color())
                        gotoxy(5, 17); input("Presione Enter para intentar de nuevo...")
                        gotoxy(5, 16); print(" "*50)
                        gotoxy(5, 17); print(" "*50)

                return  # Regresar al menú principal de estudiantes

            elif option == '3':
                while True:
                    # Modificar el estado del estudiante
                    gotoxy(5, 16); nuevo_estado = input("Ingrese el nuevo estado (1 = Activo, 0 = Inactivo): ")
                    
                    if nuevo_estado in ['0', '1']:
                        nuevo_estado = True if nuevo_estado == '1' else False
                        for s in students:
                            if s["id"] == student_id:
                                s["estado"] = nuevo_estado
                                break
                        gotoxy(28, 18); print(green_color() + "Estado actualizado con éxito." + reset_color())
                        json_file.save(students)
                        time.sleep(3)
                        break
                    else:
                        gotoxy(5, 18); print(red_color() + "Error: Ingrese 1 para Activo o 0 para Inactivo." + reset_color())
                        
                    gotoxy(5, 19); input("Presione Enter para intentar de nuevo...")  # Pausa para que el usuario vea el error
                    # Limpieza de mensajes e input para una nueva entrada
                    gotoxy(5, 18); print(" "*50)  # Limpiar mensaje de error
                    gotoxy(5, 19); print(" "*50)  # Limpiar "Presione Enter para intentar de nuevo"
                    gotoxy(5, 16); print(" "*50)  # Limpiar el input anterior para ingresar el estado
                    
                return
                        
            else:
                gotoxy(5, 16); print(red_color() + "Error: Opcion no valida." + reset_color())
                
            gotoxy(5, 17); input("Presione Enter para intentar de nuevo...")
            gotoxy(5, 16); print(" "*50)
            gotoxy(5, 17); print(" "*50)
            gotoxy(5, 14); print(" "*50)

    def delete(self):
        validar = Valida()  # Crear una instancia de la clase Valida
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Eliminar Estudiante" + reset_color())

        while True:
            gotoxy(5, 4); print(" "*50)  # Limpiar la línea
            gotoxy(5, 4); student_id = input("Ingrese ID del estudiante a eliminar: ")

            # Validación del ID
            if validar.solo_numeros(student_id):
                json_file = JsonFile(path + '/students.json')
                students = json_file.read()

                student = json_file.find("id", student_id)
                if student:
                    student = student[0]
                    nombre_mayusculas = student['nombre'].upper()
                    apellido_mayusculas = student['apellido'].upper()
                    gotoxy(5, 6); print(f"Estudiante a eliminar:")
                    gotoxy(5, 7); print(f"Nombre: {nombre_mayusculas}")
                    gotoxy(5, 8); print(f"Apellido: {apellido_mayusculas}")

                    # Confirmar eliminación
                    gotoxy(5, 10); confirm = input("¿Está seguro de que desea eliminar este estudiante? (s/n): ")
                    if confirm.lower() == 's':
                        students = [s for s in students if s["id"] != student_id]
                        json_file.save(students)
                        gotoxy(25, 12); print(green_color() + "Estudiante eliminado con éxito." + reset_color())
                    else:
                        gotoxy(25, 12); print(red_color() + "Eliminación cancelada." + reset_color())
                    break  # Salir del bucle una vez que se ha realizado la acción
                else:
                    gotoxy(26, 6); print(red_color() + "No se encontró el estudiante." + reset_color())
                    break  # Salir del bucle si el estudiante no se encuentra
            else:
                gotoxy(25, 5); print(red_color() + "Error: Ingrese 10 numeros." + reset_color())
                gotoxy(25, 6); input("Presione Enter para intentar de nuevo...")
                gotoxy(25, 5); print(" "*50)
                gotoxy(25, 6); print(" "*50)

        time.sleep(3)

    def consult(self):
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(30, 2); print(blue_color() + "Consulta de Estudiante" + reset_color())
        gotoxy(5, 4); student_id = input("Ingrese la cédula del estudiante: ")
        
        json_file = JsonFile(path + '/students.json')
        student = json_file.find("id", student_id)
        
        if student:
            gotoxy(5, 6); print(f"ID: {student[0]['id']}")
            nombre_mayusculas = student[0]['nombre'].upper()
            apellido_mayusculas = student[0]['apellido'].upper()
            gotoxy(5, 7); print(f"Estudiante: {nombre_mayusculas} {apellido_mayusculas}")
            gotoxy(5, 8); print(f"Fecha de Registro: {student[0]['fecha_registro']}")
            gotoxy(5, 9); print(f"Estado: {'Activo' if student[0]['estado'] else 'Inactivo'}")
        else:
            gotoxy(5, 6); print(red_color() + "No se encontró el estudiante." + reset_color())

        gotoxy(5, 12); input("Presione Enter para continuar...")    