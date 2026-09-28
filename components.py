class Valida:
    def solo_numeros(self, valor):
        if valor.isdigit() and len(valor) == 10:
            return True
        return False
    
    def solo_letras(self, valor, longitud=None):
        if valor.isalpha() and (longitud is None or len(valor) == longitud):
            return True
        return False

    def edadVald(self, valor):
        if valor.isdigit():
            edad = int(valor)  # Convertir el valor a entero
            if edad > 0:  # Comparar con un entero
                return True
        return False

class Menu:
    def __init__(self, titulo, opciones, x, y):
        self.titulo = titulo
        self.opciones = opciones
        self.x = x
        self.y = y

    def show(self):
        """Muestra el menú y obtiene la opción seleccionada."""
        print(f"{self.titulo}\n")
        for opcion in self.opciones:
            print(opcion)
        opcion = input("Seleccione una opción: ")

        return opcion



