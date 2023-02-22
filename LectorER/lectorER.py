# Este programa genera una interfaz de usuario (usando TKinter) que permite al usuario seleccionar
# un archivo de texto para leer cadenas de él, para luego mostrar las cadenas en la
# interfaz, junto con las coincidencias con tres expresiones regulares dadas.

import os
import tkinter as tk
from tkinter import filedialog
import re

def seleccionar_archivo():
    """
        Esta función abre un cuadro de diálogo para seleccionar un archivo de texto
        return: El nombre del archivo seleccionado o None si no se seleccionó ningún archivo
    """

    archivo = filedialog.askopenfilename(
        # Especifica abrir por defecto el directorio de documentos en Windows,
        # que funciona para cualquier usuario
        initialdir = "C:/Users/" + os.getlogin() + "/Documents",
        title = "Seleccionar archivo",
        # Especifica que solo se puedan seleccionar archivos de texto
        filetypes = (("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    if archivo:
        return archivo
    else:
        return None

def leer_archivo(ruta_archivo : str):
    """
        Esta función lee el archivo y devuelve las líneas del archivo como una lista
        param file: El archivo a leer
        return: Una lista con las líneas del archivo o None si no se pudo leer el archivo
    """

    try:

        file_text = open(ruta_archivo, "r").read()
        lines = file_text.splitlines() # Obtener las líneas del archivo
        return lines

    except:
        return None

def obtener_correspondencias(expresiones_regulares : list, cadenas : list):
    """
        Esta función obtiene las correspondencias de las expresiones regulares con las cadenas
        param expresiones_regulares: Una lista de expresiones regulares
        param cadenas: Una lista de cadenas
        return: Un diccionario con las expresiones regulares como llaves y las cadenas con las que coinciden como valores
    """

    correspondencias = {}

    try :

        for exp in expresiones_regulares:
            correspondencias[exp] = []
            for cadena in cadenas:
                if re.fullmatch(exp, cadena):
                    correspondencias[exp].append(cadena)
    except:
        pass

    return correspondencias

def listar_correspondencias(correspondencias : dict):
    
    """
        Esta función regresa un texto con cada expresión regular y las cadenas que coinciden con ella,
        pasando de línea y tabulando cada cadena.
        param correspondencias: Un diccionario con las expresiones regulares como llaves y las cadenas con las que coinciden como valores
    """

    texto = ""

    for exp, cadenas in correspondencias.items():
        texto += f"Correspondiencias para {exp}:\n"

        if cadenas:
            for cadena in cadenas:
                texto += f"\t{cadena}\n"
        else:
            texto += "\tNo hay coincidencias\n"
    
    return texto

def solicitar_archivo_a_usuario():

    nombre_archivo = seleccionar_archivo()

    # Se limpia el cuadro de texto
    global mensaje
    mensaje.delete(1.0, tk.END)

    global lista_correspondencias
    
    # Si ya existe la lista de correspondencias y no se especificó un archivo, se muestra la lista de correspondencias
    if lista_correspondencias and not nombre_archivo:

        return lista_correspondencias

    # Si no existe la lista de correspondencias y se especificó un archivo, se crea la lista de correspondencias y se muestra
    if nombre_archivo:

        archivo = leer_archivo(nombre_archivo)

        if archivo:

            # Cambiar la leyenda del botón
            global boton
            boton.config(text="Seleccionar otro archivo")

            # Obtener las expresiones regulares de las cajas de texto
            global campos
            expresiones_regulares = []

            # Convierte el valor de la caja de texto a una expresión regular
            for campo in campos:
                try:
                    expresiones_regulares.append(re.compile(campo.get()).pattern)
                except:
                    expresiones_regulares.append(None)

            # Verificar que los campos no estén vacíos
            if not all(expresiones_regulares):
                return "Por favor, ingrese una expresión regular en cada campo"

            lista_correspondencias = listar_correspondencias(obtener_correspondencias(expresiones_regulares, archivo))
            return lista_correspondencias
        
        else: return "No se pudo leer el archivo"

    else: return ""

def main():

    """
        Esta función es la función principal del programa, que crea la interfaz de usuario y la muestra
    """

    # La lista de correspondencias se guarda en una variable global para que se pueda acceder a ella
    # y esta inicia vacía
    global lista_correspondencias
    lista_correspondencias = None

    # Crear la ventana principal
    root = tk.Tk()

    # Crea tres cajas de texto para dar entrada a las expresiones regulares
    global campos
    campos = []
    for i in range(3):
        campos.append(tk.Entry(root))
        # Agregar la leyenda que indica para qué expresión regular es la caja de texto
        tk.Label(root, text=f"Expresión regular {i+1}:").pack()
        campos[i].pack()

    # Crear un botón para solicitar el archivo
    global boton
    boton = tk.Button(root,
        text="Seleccionar archivo",
        # Muestra las coincidencias en el cuadro de texto
        command=lambda: mensaje.insert(tk.END, solicitar_archivo_a_usuario())
        )
    boton.pack()

    # Crear un cuadro de texto para mostrar el resultado
    global mensaje
    mensaje = tk.Text(root, height=25, width=100)
    # Habilita la barra de desplazamiento vertical
    mensaje.config(yscrollcommand=tk.Scrollbar(root).set)
    mensaje.pack()

    # Mostrar la ventana
    root.mainloop()

main()