import re

class Clasificador:
    
    def __init__(self, expresiones_regulares : list):
        self.expresiones_regulares = expresiones_regulares

    def obtener_correspondencias(self, cadenas : list):
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
        for exp in self.expresiones_regulares:

                correspondencias[exp] = set()

        # Para cada cadena, se verifica si coincide con alguna expresión regular
        for cadena in cadenas:
            coincidio = False

            for exp in self.expresiones_regulares:

                if re.fullmatch(exp, cadena):
                    # Si coincide, se agrega la cadena al conjunto de correspondencias de la expresión regular
                    correspondencias[exp].add(cadena)
                    coincidio = True

            if not coincidio:
                cadenas_sin_correspondencia.add(cadena)
                

        # Se ordenan las cadenas de cada expresión regular
        for exp in self.expresiones_regulares:
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
        
    def __init__(self, nombre: str, automata : dict):

        """
            El analizador tiene la tarea de revisar una cadena y analizar cada caracter
            para determinar si es parte de la expresión regular que describe.
            param descripcion: Una descripción de la expresión regular
            param automata: un diccionario que representa un autómata finito no determinista, bajo el siguiente
            formato:

            {
                "transitions" :
                {
                    "estado": [
                        {"estado_destino": "expresion_regular_que_coincide_con_el_caracter"},
                        ...
                    ],
                    ...
                },
                "endstates" :
                [
                    "estado_aceptacion_1",
                    ...,
                    "estado_aceptacion_n"
                ]
            }
        """

        self.nombre = nombre
        self.automata = automata
        self.descripcion_natural = []

    def __str__(self):
        
        descripcion_como_cadena = f"[{self.nombre}]"

        for descripcion in self.descripcion_natural:
            descripcion_como_cadena += descripcion + ","
        # Se elimina la última coma
        return descripcion_como_cadena[:-1]

    def describir(self, cadena):
        """
            Esta función analiza una cadena y determina si es parte de la expresión regular que describe
            param cadena: Una cadena
            return: True si la cadena es parte de la expresión regular que describe, False en caso contrario
        """

        descripcion_natural = []
        encontro_transicion : bool
        estado_actual = "q0"

        try:
            for caracter in cadena:

                for transicion in self.automata["transitions"][estado_actual]: # Se obtienen las transiciones del estado actual
                    
                    encontro_transicion = False
                    descripcion_natural.append(f"Se encontró el caracter '{caracter}' en el estado '{estado_actual}'")
                    posible_destino = next(iter(transicion.keys()))
                    caracter_esperado = transicion[posible_destino]

                    if re.fullmatch(caracter_esperado, caracter):
                        descripcion_natural.append(f"Existe una transición de '{estado_actual}' a '{posible_destino}' con este caracter")
                        estado_actual = posible_destino
                        descripcion_natural.append(f"Ahora el estado actual es '{estado_actual}'")
                        encontro_transicion = True
                        break
                                
                if not encontro_transicion:
                    descripcion_natural.append(f"No se encontró una transición con el caracter '{caracter}' desde el estado '{estado_actual}'")
                    break

                descripcion_natural.append("------------------------")

            if estado_actual in self.automata["endstates"]:
                descripcion_natural.append(f"El autómata finalizó en el estado '{estado_actual}', un estado de aceptación")
                if not encontro_transicion:
                    descripcion_natural.append(f"No obstante, no se encontró una transición para todos los caracteres de la cadena. Por lo tanto, la cadena no es válida")
            else:
                descripcion_natural.append(f"El autómata finalizó en el estado '{estado_actual}', un estado de no aceptación")

            self.descripcion_natural = descripcion_natural
            return descripcion_natural
            
        except Exception as ex:
            raise Exception("El formato del autómata es incorrecto") from ex

