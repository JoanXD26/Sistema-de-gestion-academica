from components import Menu
from iCrudStudents import CrudStudents
from iCrudTeacher import CrudTeachers
from iCrudSubjects import CrudSubjects
from iCrudPeriod import CrudPeriodos
from iCrudGrades import CrudLevels
from iCrudNotes import CrudNotes
from matricula import process_registration
from utilities import borrarPantalla, gotoxy, reset_color, green_color, blue_color, red_color
# from dataLoader import test_load_files

path = 'archivos'

def main():
    while True:
        borrarPantalla()
        gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
        gotoxy(5, 2);main_menu = Menu("Menú Principal", ["1) Estudiantes", "2) Profesores", "3) Asignaturas", 
        "4) Perido Academico", "5) Niveles", "6) Calificaciones", "7) Matriculacion", "8) Salir"], 30, 4)
        opc = main_menu.show()
        
        if opc == "1":
            while True:
                borrarPantalla()
                gotoxy(2, 1); print(green_color() + "*"*90 + reset_color())
                students_menu = Menu("Menú Estudiantes", ["1) Registrar", "2) Consultar", "3) Editar", "4) Eliminar", "5) Salir"], 30, 4)
                opc1 = students_menu.show()
                students = CrudStudents()
                
                if opc1 == "1":
                    students.create()
                elif opc1 == "2":
                    students.consult()
                elif opc1 == "3":
                    students.update()
                elif opc1 == "4":
                    students.delete()
                elif opc1 == "5":
                    break
        
        elif opc == "2":
            while True:
                borrarPantalla()
                teacher_menu = Menu("Menú Profesores", ["1) Registrar", "2) Consultar", "3) Editar", "4) Eliminar", "5) Salir"], 30, 4)
                opc2 = teacher_menu.show()
                teachers = CrudTeachers()
                
                if opc2 == "1":
                    teachers.create()
                elif opc2 == "2":
                    teachers.consult()
                elif opc2 == "3":
                    teachers.update()
                elif opc2 == "4":
                    teachers.delete()
                elif opc2 == "5":
                    break
        
        elif opc == "3":
            while True:
                borrarPantalla()
                subjects_menu = Menu("Menú de Asignaturas", ["1) Registrar", "2) Consultar", "3) Editar", "4) Eliminar", "5) Salir"], 30, 4)
                opc3 = subjects_menu.show()
                subjects = CrudSubjects()
                
                if opc3 == "1":
                    subjects.create()
                elif opc3 == "2":
                    subjects.consult()
                elif opc3 == "3":
                    subjects.update()
                elif opc3 == "4":
                    subjects.delete()
                elif opc3 == "5":
                    break
        
        elif opc == "4":
            while True:
                borrarPantalla()
                periodo_menu = Menu("Menú de Perido Academico", ["1) Registrar", "2) Consultar", "3) Editar", "4) Eliminar", "5) Salir"], 30, 4)
                opc4 = periodo_menu.show()
                period = CrudPeriodos()
                
                if opc4 == "1":
                    period.create()
                elif opc4 == "2":
                    period.consult()
                elif opc4 == "3":
                    period.update()
                elif opc4 == "4":
                    period.delete()
                elif opc4 == "5":
                    break
        
        elif opc == "5":
            while True:
                borrarPantalla()
                level_menu = Menu("Menú de Nivel", ["1) Registrar", "2) Consultar", "3) Editar", "4) Eliminar", "5) Salir"], 30, 4)
                opc4 = level_menu.show()
                notes = CrudLevels()
                
                if opc4 == "1":
                    notes.create()
                elif opc4 == "2":
                    notes.consult()
                elif opc4 == "3":
                    notes.update()
                elif opc4 == "4":
                    notes.delete()
                elif opc4 == "5":
                    break
        
        elif opc == "6":
            borrarPantalla()
            CrudNotes()
                
        
        elif opc == "7":
            borrarPantalla()
            process_registration()
                
                
        elif opc == "8":
            borrarPantalla()
            print("Saliendo del sistema...")
            break

if __name__ == "__main__":
    main()
