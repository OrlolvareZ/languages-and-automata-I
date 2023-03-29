""" 
    Este archivo contiene una interfaz que se sirve de objetos lector, clasificador y descriptores
    para leer un archivo de texto y obtener las cadenas de caracteres que contiene, dichas cadenas
    corresponden a elementos léxicos de un lenguaje de programación ficticio.
    
    Estas cadenas de caracteres son después catgorizadas por el clasificador, el cual utiliza expresiones
    regulares para catalogarlas, pueden ser analizadas por un objeto descriptor, que emplea una notación
    sencilla de un automata de estado finito para describir el proceso de reconocimiento de las cadenas de
    caracteres por el clasificador en lenguaje natural.
    
"""

import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from lector import LectorCadenas
from analisis_cadenas import Clasificador, Descriptor
from PIL import ImageTk, Image

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

class App:

    """
        Esta clase contiene la interfaz gráfica de la aplicación.

        La interfaz se representa a continuación bajo la siguiente distribución de widgets:

            +---------------------------------+
            |           [Leer archivo]        |
            |                                 |
            |  [Imagen]   [Imagen]   [Imagen] |                
            |                                 |
            |[List_btns][List_btns][List_btns]|
            +---------------------------------+

            Donde [Leer archivo] es un botón que permite leer un archivo de texto,
            [Imagen] es una imagen que representa el diagrama de Moore de un automata,
            [List_btns] es una lista de botones que permite analizar una cadena de caracteres
            y apreciar de manera textual el proceso de reconocimiento de la misma por el automata
    """

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def definir_exp_reg(self):

        """
            Este método define las expresiones regulares que se emplearán para clasificar las cadenas de caracteres
            que se obtengan del archivo de texto.
        """

        return [
            # Identificadores
            # Un identificador debe comenzar con una letra o un guión bajo,
            # y puede contener letras, números, guiones y guiones bajos
            r"([a-zA-Z]|_)([a-zA-Z]|[0-9]|-|_)*",
            # Constantes
            # Una constante numérica puede ser un número entero o un número decimal
            # Un número entero puede ser un dígito o un dígito seguido de un número entero
            # Un número decimal puede ser un número entero seguido de un punto y un número entero
            # Una constante alfanumérica puede ser una cadena de caracteres entre comillas dobles
            # Una cadena de caracteres puede ser un carácter o un carácter seguido de una cadena de caracteres
            # Englobado por comillas dobles
            r"((-)?([0-9]+)(\.[0-9]+)?)|\"([a-zA-Z]|[0-9])*\"",
            # Comentarios
            # Un comentario puede ser una línea que comienza con el numeral
            # y está seguida de cualquier carácter
            r"#([a-zA-Z]|[0-9]|_|-)*",
        ]

    def exp_como_automatas(self):

        """
            Este método define los automatas de estado finito que describen el proceso de reconocimiento de las cadenas
            de caracteres por las expresiones regulares definidas en el método definir_exp_reg.

            Ver la clase Descriptor para más información del formato de los autómatas.
        """

        autom_identificadores = {
            # Transiciones
            "transitions" :
            {
                "q0": [
                    {"q1": "[a-zA-Z]|_"},
                ],
                "q1": [
                    {"q1": "([a-zA-Z]|[0-9]|-|_)"},
                ],
            },
            # Estados de aceptación
            "endstates" :
            [
                "q1",
            ]
        }

        autom_constantes = {
            # Transiciones
            "transitions" : 
            {
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
            "endstates" : [
                "q2",
                "q4",
                "q7",
            ]
        }

        autom_comentarios = {
            # Transiciones
            "transitions" : 
            {
                "q0": [
                    {"q1": "#"},
                ],
                "q1": [
                    {"q1": "([a-zA-Z]|[0-9]|_|-)"},
                ],
            },
            # Estados de aceptación
            "endstates" : [
                "q1",
            ]
        }

        automatas = {
            "identificadores": autom_identificadores,
            "constantes": autom_constantes,
            "comentarios": autom_comentarios,
        }

        return automatas

    def describir_analisis(self, cadena : str, descriptores: list[Descriptor], maxlineas : int = 30):

        """
            Este método permite analizar una cadena de caracteres y mostrar el proceso de reconocimiento de la misma
            por los objetos descriptores de la lista indicada por parámetro.
            param cadena: Cadena de caracteres a analizar
            param descriptores: Lista de objetos Descriptor que describen el proceso de reconocimiento de la cadena
            param maxlineas: Número máximo de líneas a mostrar por cada descriptor en una ventana emergente
        """

        analisis = ""

        try:
            for descriptor in descriptores:

                lista_estatutos = descriptor.describir(cadena)
                lineas_a_mostrar = len(lista_estatutos)
                contador_lineas = 0
                contador_lineas_total = 0
                
                if len(lista_estatutos) > maxlineas:
                    lineas_a_mostrar = maxlineas

                for estatuto in lista_estatutos:
                    analisis += estatuto + "\n"
                    contador_lineas += 1
                    contador_lineas_total += 1

                    if lineas_a_mostrar == contador_lineas or contador_lineas_total == len(lista_estatutos):

                        if len(lista_estatutos) > maxlineas:
                            estatus_lineas = f"(Mostrando líneas {contador_lineas_total - maxlineas + 1 if contador_lineas_total < len(lista_estatutos) else contador_lineas_total - contador_lineas + 1}"
                            estatus_lineas += f" a {contador_lineas_total if contador_lineas_total < len(lista_estatutos) else len(lista_estatutos)}"
                            estatus_lineas += f", de {len(lista_estatutos)})\n"
                            analisis = estatus_lineas + analisis

                        messagebox.showinfo(f"Análisis de la cadena {cadena} como {descriptor.nombre}", analisis)
                        analisis = ""
                        contador_lineas = 0

        except:
            messagebox.showerror("Error", "No se pudo analizar la cadena, el formato del automata no es correcto")

    def crear_funcion(self, cadena, descriptores : list[Descriptor]):

        """
            Este método permite extraer la función de describir_analisis de la clase Analizador
            para poder utilizarla como parámetro de un botón de manera adecuada.
            param cadena: Cadena de caracteres a analizar
            param descriptores: Lista de objetos Descriptor que describen el proceso de reconocimiento de la cadena
        """

        return lambda: self.describir_analisis(cadena, descriptores)

    def construir_interfaz(self, correspondencias : dict, cadenas_sin_correspondencia : list):

        """
            Esta función construye la interfaz gráfica de la aplicación
            param correspondencias: Diccionario que contiene las expresiones regulares como llaves
                                    y cadenas de caracteres que las describen como valores
            param cadenas_sin_correspondencia: Lista de cadenas de caracteres que no tienen correspondencia con ninguna expresión regular del diccionario
        """
        # Limpia la ventana principal
        global ventana_principal
        for widget in ventana_principal.winfo_children():
                widget.destroy()

        global boton
        boton = tk.Button(
            ventana_principal,
            text = "Leer archivo",
            command = self.leer_archivo_leng_prueba,
            height = 10
        )
        boton.grid(column=1, row=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # Se leen las imagenes correspondientes al diagrama de Moore de cada automata
        # y una etiqueta para las cadenas que no tienen correspondencia
        img_identificadores = Image.open(self.resource_path("./imagenes/autom_identificadores.png"))
        img_identificadores = ImageTk.PhotoImage(img_identificadores.resize((300, 230)))
        lbl_iden = tk.Label(ventana_principal, image=img_identificadores)
        lbl_iden.image = img_identificadores
        lbl_iden.grid(row=1, column=0)

        img_constantes = Image.open(self.resource_path("./imagenes/autom_constantes.png"))
        img_constantes = ImageTk.PhotoImage(img_constantes.resize((300, 240)))
        lbl_const = tk.Label(ventana_principal, image=img_constantes)
        lbl_const.image = img_constantes
        lbl_const.grid(row=1, column=1)

        img_comentarios = Image.open(self.resource_path("./imagenes/autom_comentarios.png"))
        img_comentarios = ImageTk.PhotoImage(img_comentarios.resize((300, 240)))
        lbl_com = tk.Label(ventana_principal, image=img_comentarios)
        lbl_com.image = img_comentarios
        lbl_com.grid(row=1, column=2)

        tk.Label(ventana_principal, text="Elementos no clasificados").grid(row=1, column=3)

        # Se crean los frames para los botones de cada automata
        frame_identificadores = VerticalScrolledFrame(ventana_principal)
        frame_identificadores.grid(row=2, column=0)
        frame_constantes = VerticalScrolledFrame(ventana_principal)
        frame_constantes.grid(row=2, column=1)
        frame_comentarios = VerticalScrolledFrame(ventana_principal)
        frame_comentarios.grid(row=2, column=2)
        frame_sin_correspondencia = VerticalScrolledFrame(ventana_principal)
        frame_sin_correspondencia.grid(row=2, column=3)

        # Se crean los botones para solicitar la descripción del análisis de cada cadena que corresponde a
        # cada automata, se les asigna un ancho con base en la cadena más larga reconocida en todo el
        # archivo de entrada, y se colocan en el frame correspondiente.

        exp_reg = clasificador.expresiones_regulares
        todas_las_cadenas = correspondencias[exp_reg[0]] + correspondencias[exp_reg[1]] + correspondencias[exp_reg[2]]
        ancho_boton = max( [len(cadena) for cadena in todas_las_cadenas])

        # Correspondencias para identificadores
        global descriptor_identificadores
        for cadena in correspondencias[exp_reg[0]]:
            tk.Button(
                frame_identificadores.interior,
                text=cadena,
                command = self.crear_funcion(cadena, [descriptor_identificadores]),
                width = ancho_boton
            ).pack()

        # Correspondencias para constantes
        global descriptor_constantes
        for cadena in correspondencias[exp_reg[1]]:
            boton = tk.Button(
                frame_constantes.interior,
                text=cadena,
                command = self.crear_funcion(cadena, [descriptor_constantes]),
                width = ancho_boton
            )
            boton.pack()

        # Correspondencias para comentarios
        global descriptor_comentarios
        for cadena in correspondencias[exp_reg[2]]:
            tk.Button(
                frame_comentarios.interior,
                text=cadena,
                command = self.crear_funcion(cadena, [descriptor_comentarios]),
                width = ancho_boton
            ).pack()

        # Cadenas sin correspondencia
        for cadena in cadenas_sin_correspondencia:
            tk.Button(
                frame_sin_correspondencia.interior,
                text=cadena,
                command =
                    self.crear_funcion(cadena, [
                        descriptor_identificadores,
                        descriptor_constantes,
                        descriptor_comentarios,
                    ]),
                width = ancho_boton
            ).pack()

    def leer_archivo_leng_prueba(self):

        """
            Esta función lee un archivo de texto y obtiene las cadenas de caracteres que contiene.
            El archivo contiene cadenas de caracteres que corresponden a elementos léxicos de un
            lenguaje de programación ficticio.

            Una vez que se lee el archivo, se obtienen las correspondencias de cada cadena con
            las expresiones regulares que definen los elementos léxicos del lenguaje, y se
            construye la interfaz gráfica de la aplicación.
        """

        try:
            global lector
            cadenas = lector.seleccionar_leer_archivo()
            global boton
            boton.configure(text="Leer otro archivo")
        except:
            messagebox.showerror("Error", "No se pudo leer el archivo")
            return

        if cadenas:
            global clasificador
            correspondencias = clasificador.obtener_correspondencias(cadenas)
            self.construir_interfaz(correspondencias[0], correspondencias[1])

    def main(self):

        """
            Esta función es la función principal del programa, que solicita la lectura de un archivo
            con el lenguaje de prueba y la construcción de otros widgets necesarios para la aplicación.
        """

        global lector
        lector = LectorCadenas()
        global clasificador
        clasificador = Clasificador(expresiones_regulares = self.definir_exp_reg())
        automatas = self.exp_como_automatas()

        global descriptor_identificadores
        descriptor_identificadores = Descriptor("identificador", automatas["identificadores"])
        global descriptor_constantes
        descriptor_constantes = Descriptor("constante", automatas["constantes"])
        global descriptor_comentarios
        descriptor_comentarios = Descriptor("comentario", automatas["comentarios"])

        global ventana_principal
        ventana_principal = tk.Tk()
        ventana_principal.title("Clasificador de componentes léxicos para lenguaje de prueba")
        ventana_principal.geometry("1200x600")
        ventana_principal.resizable(True, True)
        ventana_principal.columnconfigure(0, weight=1)
        ventana_principal.columnconfigure(1, weight=1)
        ventana_principal.columnconfigure(2, weight=1)
        ventana_principal.columnconfigure(3, weight=1)
        ventana_principal.rowconfigure(0, weight=1, pad=10) # fila del botón
        ventana_principal.rowconfigure(1, weight=2) # Fila de las imágenes
        ventana_principal.rowconfigure(2, weight=3) # Fila de los botones

        global boton
        boton = tk.Button(
            ventana_principal,
            text = "Leer archivo",
            command = self.leer_archivo_leng_prueba,
            height = 10
        )
        boton.grid(column=1, row=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        ventana_principal.mainloop()

App().main()