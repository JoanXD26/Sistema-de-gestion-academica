import os
from datetime import date
from clsJson import JsonFile

# Definir la ruta base
path = 'archivos'

# Asegurarse de que la carpeta 'archivos' exista
if not os.path.exists(path):
    os.makedirs(path)

# Definir las rutas para los archivos JSON
path_students = os.path.join(path, 'students.json')
path_notas = os.path.join(path, 'notas.json')
path_materias = os.path.join(path, 'datajson.json')
path_asignaturas = os.path.join(path, 'asignaturas.json')

# Instancias de JsonFile para manejar los archivos JSON en la carpeta "archivos"
students_json = JsonFile(path_students)
notas_json = JsonFile(path_notas)
materias_json = JsonFile(path_materias)
asignaturas_json = JsonFile(path_asignaturas)

def CrudNotes():
    
    class Nota:
        def __init__(self, id, periodo, profesor, asignatura, active=True, fecha_creacion=None, nota_final=None):
            self.id = id
            self.periodo = periodo
            self.profesor = profesor
            self.asignatura = asignatura
            self.detalleNota = []
            self.fecha_creacion = fecha_creacion if fecha_creacion else date.today().strftime("%Y-%m-%d")
            self.active = active
            self.nota_final = nota_final  # Añadido para guardar la nota final

        def add_nota(self, estudiante, nota1, nota2, examen, recuperacion=None, observacion=None):
            detalle = DetalleNota(
                id=len(self.detalleNota) + 1,
                estudiante=estudiante,
                nota1=nota1,
                nota2=nota2,
                examen=examen,
                recuperacion=recuperacion,
                observacion=observacion
            )
            self.detalleNota.append(detalle)

        def to_dict(self):
            return {
                "id": self.id,
                "periodo": self.periodo,
                "profesor": self.profesor,
                "asignatura": self.asignatura,
                "detalleNota": [dn.to_dict() for dn in self.detalleNota],
                "fecha_creacion": self.fecha_creacion,
                "active": self.active,
                "nota_final": self.nota_final  # Añadido para guardar la nota final
            }

    class DetalleNota:
        def __init__(self, id, estudiante, nota1, nota2, examen, recuperacion=None, observacion=None):
            self.id = id
            self.estudiante = estudiante
            self.nota1 = nota1
            self.nota2 = nota2
            self.examen = examen
            self.recuperacion = recuperacion
            self.observacion = observacion

        def to_dict(self):
            return {
                "id": self.id,
                "estudiante": self.estudiante,
                "nota1": self.nota1,
                "nota2": self.nota2,
                "examen": self.examen,
                "recuperacion": self.recuperacion,
                "observacion": self.observacion
            }

    class GestorNotas:
        def __init__(self, notas_json, students_json, materias_json, asignaturas_json):
            self.notas_json = notas_json
            self.students_json = students_json
            self.materias_json = materias_json
            self.asignaturas_json = asignaturas_json
            self.notas = self.cargar_notas()

        def cargar_notas(self):
            try:
                data = self.notas_json.read()
                notas = []
                for nota in data:
                    n = Nota(
                        id=nota["id"],
                        periodo=nota["periodo"],
                        profesor=nota["profesor"],
                        asignatura=nota["asignatura"],
                        active=nota.get("active", True),
                        fecha_creacion=nota.get("fecha_creacion", date.today().strftime("%Y-%m-%d")),
                        nota_final=nota.get("nota_final")  # Cargar nota_final
                    )
                    for dn in nota["detalleNota"]:
                        detalle = DetalleNota(
                            id=dn["id"],
                            estudiante=dn["estudiante"],
                            nota1=dn["nota1"],
                            nota2=dn["nota2"],
                            examen=dn["examen"],
                            recuperacion=dn.get("recuperacion"),
                            observacion=dn.get("observacion")
                        )
                        n.detalleNota.append(detalle)
                    notas.append(n)
                return notas
            except FileNotFoundError:
                return []

        def guardar_notas(self):
            data = [nota.to_dict() for nota in self.notas]
            self.notas_json.save(data)

        def buscar_profesor_por_materia(self, descripcion):
            asignaturas = self.asignaturas_json.read()
            for asignatura in asignaturas:
                if asignatura["descripcion"].lower() == descripcion.lower() and asignatura["active"]:
                    return asignatura["profesor"]
            return "Profesor no asignado"

        def buscar_estudiantes_por_materia(self, materia):
            estudiantes = self.materias_json.read()  # Leer desde materias_json
            
            # Obtener el nombre del profesor para la materia
            profesor = self.buscar_profesor_por_materia(materia)
            
            matriculados = []
            for estudiante in estudiantes.values():
                for nivel, materias in estudiante.get('materias', {}).items():
                    if materia.lower() in [m.lower() for m in materias]:
                        matriculados.append(estudiante)
                        break
            
            return profesor, matriculados

        def buscar_estudiante(self, cedula):
            estudiantes = self.materias_json.read()  # Leer desde materias_json
            return estudiantes.get(cedula, None)

        def agregar_notas(self, estudiante):
            print(f"Ingrese las notas para {estudiante['nombre']} {estudiante['apellido']}:")

            def obtener_nota(mensaje):
                while True:
                    try:
                        valor = input(mensaje)
                        if valor == '':  # Manejar caso en que el usuario presiona Enter sin ingresar un valor
                            print("El valor no puede estar vacío. Inténtelo de nuevo.")
                            continue
                        return float(valor)
                    except ValueError:
                        print("Por favor, ingrese un número válido.")
            
            # Ingresar las notas de los parciales y el examen final
            parcial1 = obtener_nota("Nota del Parcial 1: ")
            parcial2 = obtener_nota("Nota del Parcial 2: ")
            examen_final = obtener_nota("Nota del Examen Final: ")
            
            # Calcular la suma total sin el examen de recuperación
            suma_total = parcial1 + parcial2 + examen_final
            
            # Inicializar la nota final
            nota_final = suma_total

            if suma_total < 70:
                print(f"El estudiante {estudiante['nombre']} {estudiante['apellido']} no aprobó directamente")
                print("El estudiante tiene que dar examen de recuperación")
                
                # Si la suma es menor a 70, se solicita la nota de recuperación
                examen_recuperacion = obtener_nota("Nota del Examen de Recuperación: ")
                
                # Calcular el promedio final incluyendo la nota de recuperación
                promedio_final = (suma_total + examen_recuperacion) / 2
                
                if promedio_final >= 70:
                    print(f"El estudiante {estudiante['nombre']} {estudiante['apellido']} aprobó con supletorio. Nota final: {promedio_final}/100.")
                    nota_final = promedio_final
                else:
                    print(f"El estudiante {estudiante['nombre']} {estudiante['apellido']} reprobó. Nota final: {promedio_final}/100.")
                    nota_final = promedio_final
            else:
                print(f"El estudiante {estudiante['nombre']} {estudiante['apellido']} aprobó con {suma_total}.")

            # Actualizamos las notas en el diccionario del estudiante
            estudiante['notas'] = {
                'parcial1': parcial1,
                'parcial2': parcial2,
                'examen_final': examen_final,
                'recuperacion': examen_recuperacion if suma_total < 70 else None
            }

            # También actualizamos la nota final en el objeto Nota
            nota = Nota(
                id=len(self.notas) + 1,
                periodo="Primer",  # Suponiendo un periodo, esto debe ser ajustado según tu caso
                profesor="profesor_example",  # Ajustar según corresponda
                asignatura="asignatura_example",  # Ajustar según corresponda
                active=True,
                nota_final=nota_final
            )
            self.notas.append(nota)
            self.guardar_notas()  # Guardar todas las notas incluyendo la nueva nota

            # Guardar los cambios en el archivo JSON
            estudiantes = self.materias_json.read()  # Leer desde materias_json
            estudiantes[estudiante['cedula']] = estudiante
            self.materias_json.save(estudiantes)  # Guardar cambios

    # Instancia del GestorNotas
    gestor_notas = GestorNotas(notas_json, students_json, materias_json, asignaturas_json)

    # Ejemplo de uso
    materia = input("Ingrese el nombre de la materia para buscar estudiantes: ")
    profesor, estudiantes_matriculados = gestor_notas.buscar_estudiantes_por_materia(materia)

    # Imprimir nombre de la materia y profesor
    print(f"Materia: {materia}")
    print(f"Profesor: {profesor}")

    if estudiantes_matriculados:
        print("Estudiantes matriculados en la materia:")
        for estudiante in estudiantes_matriculados:
            print(f"{estudiante['nombre']} {estudiante['apellido']} - Cédula: {estudiante['cedula']}")
        
        cedula = input("Ingrese el número de cédula del estudiante para agregar notas: ")
        estudiante = gestor_notas.buscar_estudiante(cedula)
        
        if estudiante:
            # Si el estudiante es encontrado, se agregan las notas
            gestor_notas.agregar_notas(estudiante)
        else:
            print("Estudiante no encontrado.")
    else:
        print("No hay estudiantes matriculados en esa materia.")
        
        
if __name__ == "__main__":
    CrudNotes()
