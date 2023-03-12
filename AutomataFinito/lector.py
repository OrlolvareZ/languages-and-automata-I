import io
import os
import re
from tkinter import filedialog

class LectorCadenas:

    """
        Esta clase representa un lector de archivos de texto, que permite leer un archivo de texto
        en formato UTF-8 y devolver las cadenas que contiene, por defecto separadas por espacios en blanco
    """

    def seleccionar_leer_archivo(self, initialdir = "C:/Users/" + os.getlogin() + "/Documents", title = "Seleccionar archivo"):
        """
            Esta función abre un cuadro de diálogo para seleccionar un archivo de texto
            return: El nombre del archivo seleccionado o None si no se seleccionó ningún archivo,
            o una excepción si no se pudo leer el archivo
        """

        nombre_archivo = filedialog.askopenfilename(
            # Especifica abrir por defecto el directorio de documentos en Windows,
            # que funciona para cualquier usuario
            initialdir = initialdir,
            title = title,
            # Especifica que solo se puedan seleccionar archivos de texto
            filetypes = (("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )

        try:
            return self._leer_archivo_(nombre_archivo) if nombre_archivo else None
        except Exception as ex:
            raise ex

    def _leer_archivo_(self, ruta_archivo : str, separador : str = r"\s+"):
        """
            Esta función lee el archivo y devuelve las líneas del archivo como una lista
            param ruta_archivo: El archivo a leer
            return: Una lista con las líneas del archivo o None si no se pudo leer el archivo,
            o una excepción si no se pudo leer el archivo
        """

        try:

            texto_archivo = io.open(ruta_archivo, mode="r", encoding="utf-8").read() # leer archivo como UTF-8
            lineas = re.split(r"\s+", texto_archivo)
            
            return lineas

        except Exception as ex:
            raise ex
