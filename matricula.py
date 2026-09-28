import os
import json
from utilities import borrarPantalla

# Define las rutas a los archivos JSON
path = 'archivos'
students_file = os.path.join(path, 'students.json')
subjects_file = os.path.join(path, 'asignaturas.json')
datajson_file = os.path.join(path, 'datajson.json')

# Función para cargar datos de un archivo JSON
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON en: {file_path}")
        return []

# Función para guardar datos en un archivo JSON
def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Función para obtener el orden de los niveles
def get_level_order(level):
    order = {
        'Primer': 1,
        'Segundo': 2,
        'Tercer': 3,
        'Cuarto': 4,
        # Agregar más niveles según sea necesario
    }
    return order.get(level, float('inf'))  # Usar float('inf') para niveles no definidos

# Función para procesar la inscripción
def process_registration():
    students_data = load_json_file(students_file)
    subjects_data = load_json_file(subjects_file)

    while True:
        
        # Solicitar cédula del estudiante
        cedula = input("Ingrese la cédula del estudiante (o presione Enter para regresar al menú principal): ")

        if not cedula:
            print("Regresando al menú principal...")
            return  # Regresar al menú principal

        # Buscar el estudiante por cédula
        student = next((s for s in students_data if s['id'] == cedula), None)

        if student:
            # Mostrar información del estudiante
            print("Información del Estudiante:")
            print(f"Cédula: {student['id']}")
            print(f"Nombre: {student['nombre']}")
            print(f"Apellido: {student['apellido']}")
            
            # Seleccionar nivel
            levels = sorted(set(subject['nivel'] for subject in subjects_data), key=get_level_order)
            print("Niveles disponibles:")
            for idx, level in enumerate(levels):
                print(f"{idx + 1}. Nivel {level}")

            while True:
                try:
                    choice = int(input("Seleccione el número del nivel: "))
                    if 1 <= choice <= len(levels):
                        selected_level = levels[choice - 1]
                        break
                    else:
                        print(f"Por favor, seleccione un número entre 1 y {len(levels)}.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")

            # Seleccionar materias basadas en el nivel
            filtered_subjects = [subject for subject in subjects_data if subject['nivel'] == selected_level]
            print("Materias disponibles:")
            for idx, subject in enumerate(filtered_subjects):
                print(f"{idx + 1}. {subject['descripcion']}")

            selected_subjects = []
            while True:
                try:
                    choice = input("Seleccione el número de la materia a la que desea inscribirse (o presione Enter para finalizar): ")
                    if not choice:
                        break
                    choice = int(choice)
                    if 1 <= choice <= len(filtered_subjects):
                        selected_subjects.append(filtered_subjects[choice - 1])
                        print(f"Materia '{filtered_subjects[choice - 1]['descripcion']}' añadida.")
                    else:
                        print(f"Por favor, seleccione un número entre 1 y {len(filtered_subjects)}.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")

            # Agrupar materias por nivel y ordenarlas
            level_subjects = {}
            for subject in selected_subjects:
                level = subject.get('nivel', 'Desconocido')  # Usar el campo 'nivel' para clasificar
                if level not in level_subjects:
                    level_subjects[level] = []
                level_subjects[level].append(subject['descripcion'])

            # Mostrar mensaje de inscripción
            print("\n--- Confirmación de Inscripción ---")
            print(f"Nombre: {student['nombre']}")
            print(f"Apellido: {student['apellido']}")
            print(f"Cédula: {student['id']}")
            print(f"Nivel seleccionado: Nivel {selected_level}")
            
            print("Materias inscritas:")
            for level in sorted(level_subjects.keys(), key=get_level_order):
                print(f"- Nivel {level}:")
                for subject in level_subjects[level]:
                    print(f"  - {subject}")

            # Guardar la información en un archivo JSON
            existing_data = load_json_file(datajson_file)
            if not isinstance(existing_data, dict):
                existing_data = {}

            if cedula not in existing_data:
                existing_data[cedula] = {
                    'cedula': student['id'],
                    'nombre': student['nombre'],
                    'apellido': student['apellido'],
                    'nivel': f'Nivel {selected_level}',
                    'materias': level_subjects
                }
            else:
                # Actualizar la inscripción existente
                existing_record = existing_data[cedula]
                for level, subjects in level_subjects.items():
                    if level not in existing_record['materias']:
                        existing_record['materias'][level] = subjects
                    else:
                        existing_record['materias'][level].extend(subjects)

            save_json_file(datajson_file, existing_data)
            print(f"\nLa inscripción se ha guardado en '{datajson_file}'.")
            return  # Regresar al menú principal

        else:
            print("Estudiante no encontrado. Intente nuevamente.")


# Ejecutar el menú principal
if __name__ == "__main__":
    process_registration()

