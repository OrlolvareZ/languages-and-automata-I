import re


class Clasificador:
    
    def __init__(self, expresiones):
        self.expresiones = expresiones

    def obtener_correspondencias(cadenas : list):
        """
            Esta función obtiene las correspondencias de las expresiones regulares con las cadenas
            y devuelve un diccionario con las expresiones regulares como llaves y las cadenas con las que coinciden como valores,
            y una lista con las cadenas que no coincidieron con ninguna expresión regular
            param expresiones_regulares: Una lista de expresiones regulares
            param cadenas: Una lista de cadenas
            return: Una tupla con un diccionario con las expresiones regulares como llaves y las cadenas con las que coinciden como valores,
            y una lista con las cadenas que no coincidieron con ninguna expresión regular
        """

        correspondencias = {}
        cadenas_sin_correspondencia = set()

        # Para cada expresión regular, se crea una llave en el diccionario con una lista vacía
        for exp in expresiones_regulares:

                correspondencias[exp] = set()

        # Para cada cadena, se verifica si coincide con alguna expresión regular
        for cadena in cadenas:
            coincidio = False

            for exp in expresiones_regulares:

                if re.fullmatch(exp, cadena):
                    # Si coincide, se agrega la cadena al conjunto de correspondencias de la expresión regular
                    correspondencias[exp].add(cadena)
                    coincidio = True

            if not coincidio:
                cadenas_sin_correspondencia.add(cadena)
                

        # Se ordenan las cadenas de cada expresión regular
        for exp in expresiones_regulares:
            correspondencias[exp] = list(correspondencias[exp])
            correspondencias[exp].sort()

        cadenas_sin_correspondencia = list(cadenas_sin_correspondencia)
        cadenas_sin_correspondencia.sort()

        return (correspondencias, cadenas_sin_correspondencia)

class Descriptor:

    """
        Esta clase representa un descriptor de expresiones regulares
        param descripcion: Una descripción de la expresión regular
        param automata: Una tupla que contiene un diccionario que representa autómata finito no determinista
        que representa la expresión regular y un conjunto de estados de aceptación
    """
        
    def __init__(self, descripcion, automata):
        self.descripcion = descripcion
        self.automata = automata

    # El descriptor tiene la tarea de revisar una cadena y analizar cada caracter
    # para determinar si es parte de la expresión regular que describe.
    # Esta expresión regular está dada como un autómata finito no determinista,
    # representado en un diccionario con el formato:
    # {
    #   "estado": [
    #       {"estado_destino": "expresion_regular_que_coincide_con_el_caracter"},
    #       ...
    #    ],
    #     ...
    # }

    def analizar(self, cadena):
        """
            Esta función analiza una cadena y determina si es parte de la expresión regular que describe
            param cadena: Una cadena
            return: True si la cadena es parte de la expresión regular que describe, False en caso contrario
        """

        estado_actual = "q0"

        # Se recorre cada caracter de la cadena
        for caracter in cadena:

            encontro_transicion = False

            # automata[0] es el diccionario que representa el autómata finito no determinista
            # automata[1] es el conjunto de estados de aceptación    
            for transicion in self.automata[0][estado_actual]: # Se obtienen las transiciones del estado actual

                posible_destino = transicion.keys()[0]
                caracter_esperado = transicion[posible_destino]

                if re.fullmatch(caracter_esperado, caracter):
                    estado_actual = posible_destino
                    encontro_transicion = True
                    break
            
            if not encontro_transicion:
                return False

        if estado_actual in self.automata[1]:
            return True
        else:
            return False
