# Este programa genera una interfaz de usuario (usando TKinter) que permite al usuario seleccionar
# un archivo de texto para leer cadenas de él, para luego mostrar las cadenas en la
# interfaz, junto con las coincidencias con tres expresiones regulares dadas.

import os
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog
import re

def seleccionar_archivo():
    """
        Esta función abre un cuadro de diálogo para seleccionar un archivo de texto
        return: El nombre del archivo seleccionado o None si no se seleccionó ningún archivo
    """

    nombre_archivo = filedialog.askopenfilename(
        # Especifica abrir por defecto el directorio de documentos en Windows,
        # que funciona para cualquier usuario
        initialdir = "C:/Users/" + os.getlogin() + "/Documents",
        title = "Seleccionar archivo",
        # Especifica que solo se puedan seleccionar archivos de texto
        filetypes = (("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

    return nombre_archivo if nombre_archivo else None

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

def listar_correspondencias(correspondencias : dict, cadenas_sin_correspondencia : list):
    
    """
        Esta función regresa un texto con cada expresión regular y las cadenas que coinciden con ella,
        pasando de línea y tabulando cada cadena.
        param correspondencias: Un diccionario con las expresiones regulares como llaves y las cadenas con las que coinciden como valores
        param cadenas_sin_correspondencia: Una lista con las cadenas que no coincidieron con ninguna expresión regular
    """

    texto = ""

    for exp, cadenas in correspondencias.items():
        texto += f"Correspondiencias para {exp.pattern[1:-1]}:\n"

        if cadenas:
            for cadena in cadenas:
                texto += f"\t{cadena}\n"
        else:
            texto += "\tNo hay coincidencias\n"

    if cadenas_sin_correspondencia:

        texto += "Estas cadenas no coincidieron con ninguna expresión regular:\n"

        for cadena in cadenas_sin_correspondencia:
            texto += f"\t{cadena}\n"
    
    return texto

def obtener_mensaje_procesamiento(nombre_archivo : str, expresiones_regulares : list):

    """
        Esta función obtiene el mensaje que se mostrará en la caja de texto
        param nombre_archivo: El nombre del archivo seleccionado
        param expresiones_regulares: Una lista de expresiones regulares
        return: El mensaje que se mostrará en la caja de texto
    """

    global correspondencias_en_lista
    
    # Si ya existe la lista de correspondencias y no se especificó un archivo, se muestra la lista de correspondencias
    if correspondencias_en_lista and not nombre_archivo:

        return correspondencias_en_lista

    # Si no existe la lista de correspondencias y se especificó un archivo,
    # se crea la lista de correspondencias y se muestra
    if nombre_archivo:

        archivo = leer_archivo(nombre_archivo)

        if archivo:

            correspondencias = obtener_correspondencias(expresiones_regulares, archivo)
            correspondencias_en_lista = listar_correspondencias(correspondencias[0], correspondencias[1])
            return correspondencias_en_lista
        
        else: return "No se pudo leer el archivo"

    else: return ""

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
            # Se reemplazan los paréntesis por corchetes para que coincidan con el formato de las expresiones regulares,
            # y se agrega un carácter de inicio y otro de fin de cadena, para mayor comodidad del usuario
            entrada_campo = campo.get().replace("(", "[").replace(")", "]")
            expresiones_regulares.append(re.compile(f"^{entrada_campo}$"))
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

    # La lista de correspondencias se guarda en una variable global para que se pueda acceder a ella
    # y esta inicia vacía
    global correspondencias_en_lista
    correspondencias_en_lista = None

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Lector de expresiones regulares")
    root.option_add("*Font", "Poppins 12")

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
    boton = tk.Button(root, text="Seleccionar archivo", command = mostrar_mensaje_procesamiento)
    boton.pack()

    # Crea una leyenda para indicar que se deben ingresar expresiones regulares
    global alerta
    alerta = tk.Label(root, text="")
    alerta.pack()

    # Crear un cuadro de texto para mostrar el resultado
    global area_texto
    area_texto = scrolledtext.ScrolledText(root, height=25, width=100)
    area_texto.pack()

    # Mostrar la ventana
    root.mainloop()

main()