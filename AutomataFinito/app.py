# Este programa genera una interfaz de usuario (usando TKinter) que permite al usuario seleccionar
# un archivo de texto para leer cadenas de él, para luego mostrar las cadenas en la
# interfaz, junto con las coincidencias con tres expresiones regulares dadas.

import io
import os
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog
import re
from lector import Lector
from clasificador import Clasificador

lector = Lector()
clasificador = Clasificador()

def mostrar_mensaje_procesamiento():

    """
        Esta función muestra el mensaje que se mostrará en la caja de texto,
        o muestra un mensaje de error si no se han ingresado expresiones regulares en las cajas de texto
    """

    global campos
    global alerta
    global area_texto

    area_texto.configure(state ='normal') # Se habilita la escritura en el cuadro de texto

    if all(campo.get() for campo in campos): # Se verifica que se hayan ingresado expresiones regulares

        # Convierte los valores de las cajas de texto en expresiones regulares
        expresiones_regulares = []
        for campo in campos:
            expresiones_regulares.append(re.compile(f"^{campo.get()}$"))
        alerta.config(text="")
        mensaje = obtener_mensaje_procesamiento( seleccionar_archivo(), expresiones_regulares )
        area_texto.delete(1.0, tk.END) # Se limpia el cuadro de texto
        area_texto.insert(tk.END, mensaje )
        global boton # Si el archivo se leyó correctamente, se cambia el texto del botón
        if mensaje:
            boton.config(text="Seleccionar otro archivo")
        
    else:
        alerta.config(text="Por favor, ingrese una expresión regular en cada campo")

    area_texto.configure(state ='disabled') # Se deshabilita la escritura en el cuadro de texto

def main():

    """
        Esta función es la función principal del programa, que crea la interfaz de usuario y la muestra
    """

    """
        Crea una ventana con una cuadrícula, tal que luzca de esta manera:
        +-------------------------------+
        | [leer_archivo]                |
        |                               |
        | ----------  Identificadores   |
        | | imagen |  espacio p/ generar|
        | ----------  botones           |
        |                               |
        | ----------  Constantes        |
        | | imagen |  espacio p/ generar|
        | ----------  botones           |
        |                               |
        | ----------  Comentarios       |
        | | imagen |  espacio p/ generar|
        | ----------  botones           |
        |                               |
        | ----------  No clasificados   |
        | | imagen |  espacio p/ generar|
        | ----------  botones           |
        |                               |
        |-------------------------------|

    """

    ventana_principal = tk.Tk()
    ventana_principal.title("Clasificador de cadenas")
    ventana_principal.geometry("800x600")

    # Se crea el botón para seleccionar el archivo
    global boton
    boton = tk.Button(ventana_principal, text="Seleccionar archivo", command=mostrar_mensaje_procesamiento)

    


main()

def declarar_estados():

    y78u

    autom_identificadores = (
        # Estados
        {
            # Un identificador debe comenzar con una letra o un guión bajo,
            # y puede contener letras, números, guiones y guiones bajos
            "q0": [
                {"q1": "[a-zA-Z]|_"},
            ],
            "q1": [
                {"q1": "([a-zA-Z]|[0-9]|-|_)"},
            ],
        },
        # Estados de aceptación
        [
            "q1",
        ]
    )

    autom_constantes = (
        {
            # Una constante numérica puede ser un número entero o un número decimal
            # Un número entero puede ser un dígito o un dígito seguido de un número entero
            # Un número decimal puede ser un número entero seguido de un punto y un número entero
            # Una constante alfanumérica puede ser una cadena de caracteres entre comillas dobles
            # Una cadena de caracteres puede ser un carácter o un carácter seguido de una cadena de caracteres
            # Englobado por comillas dobles
            "q0": [
                {"q1": "-"},
                {"q2": "[0-9]"},
                {"q5" : "\""},
                ],
            "q1": [
                {"q2": "[0-9]"},
            ],
            "q2": [
                {"q2": "[0-9]"},
                {"q3": "."},
            ],
            "q3": [
                {"q4": "[0-9]"},
            ],
            "q4": [
                {"q4": "[0-9]"},
            ],
            "q5": [
                {"q6": "([a-zA-Z]|[0-9])"},
                {"q7": "\""},
            ],
            "q6": [
                {"q6": "([a-zA-Z]|[0-9])"},
                {"q7": "\""},
            ], 
        },
        # Estados de aceptación
        [
            "q2",
            "q4",
            "q7",
        ]
    )

    autom_comentarios = (
        {
            # Un comentario puede ser una línea que comienza con el numeral
            # y está seguida de cualquier carácter
            "q0": [
                {"q1": "#"},
            ],
            "q1": [
                {"q1": "([a-zA-Z]|[0-9]|_|-)"},
            ],
        },
        # Estados de aceptación
        [
            "q1",
        ]
    )

    automatas = {
        "identificadores": autom_identificadores,
        "constantes": autom_constantes,
        "comentarios": autom_comentarios,
    }

    return automatas