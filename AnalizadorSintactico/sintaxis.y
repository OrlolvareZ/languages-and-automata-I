%{
    int yylex();
    int yyerror(char*);
%}

%token IDENTIFICADOR_STRING
%token IDENTIFICADOR_REAL
%token IDENTIFICADOR_ENTERO
%token IDENTIFICADOR_LOGICO
%token IDENTIFICADOR_PROGRAMA

%token OP_RESTA
%token OP_SUMA
%token OP_DIVISION
%token OP_MULTIPLICACION
%token OP_ASIGNACION

%token OP_MENOR
%token OP_MAYOR
%token OP_MENOR_IGUAL
%token OP_MAYOR_IGUAL
%token OP_IGUAL
%token OP_DIFERENTE

%token OP_AND
%token OP_OR
%token OP_NOT

%token PAL_RES_PROGRAMA
%token PAL_RES_INICIO
%token PAL_RES_FIN
%token PAL_RES_LEER
%token PAL_RES_ESCRIBIR
%token PAL_RES_ENTERO
%token PAL_RES_REAL
%token PAL_RES_CADENA
%token PAL_RES_LOGICO
%token PAL_RES_SI
%token PAL_RES_SINO
%token PAL_RES_ENTONCES
%token PAL_RES_MIENTRAS
%token PAL_RES_HACER
%token PAL_RES_REPETIR
%token PAL_RES_HASTA
%token PAL_RES_VARIABLES

%token DELIM_PARENT_DER
%token DELIM_PARENT_IZQ
%token DELIM_PUNTO_COMA
%token DELIM_COMA
%token DELIM_DOS_PUNTOS

%token NUMERO_ENTERO
%token NUMERO_REAL

%token CADENA

%token PAL_RES_VERDADERO
%token PAL_RES_FALSO

%%

programa:
    encabezado bloque_declaracion_variables cuerpo

encabezado:
    PAL_RES_PROGRAMA IDENTIFICADOR_PROGRAMA DELIM_PUNTO_COMA
    ;

bloque_declaracion_variables:
    PAL_RES_VARIABLES declaracion_variables
    ;

declaracion_variables:
    identificadores_string DELIM_DOS_PUNTOS PAL_RES_CADENA DELIM_PUNTO_COMA declaracion_variables
    | identificadores_real DELIM_DOS_PUNTOS PAL_RES_REAL DELIM_PUNTO_COMA declaracion_variables
    | identificadores_entero DELIM_DOS_PUNTOS PAL_RES_ENTERO DELIM_PUNTO_COMA declaracion_variables
    | identificadores_logico DELIM_DOS_PUNTOS PAL_RES_LOGICO DELIM_PUNTO_COMA declaracion_variables
    | %empty
    ;

cuerpo:
    PAL_RES_INICIO expresiones PAL_RES_FIN
    | PAL_RES_INICIO PAL_RES_FIN
    ;

expresiones:
    expresion expresiones
    | expresion
    ;

expresion:
    asignacion DELIM_PUNTO_COMA
    | operacion_e_s DELIM_PUNTO_COMA
    | estruc_control
    ;

operacion_e_s:
    escritura
    | lectura
    ;

escritura:
    PAL_RES_ESCRIBIR DELIM_PARENT_IZQ valores DELIM_PARENT_DER
    ;

lectura:
    PAL_RES_LEER DELIM_PARENT_IZQ valores DELIM_PARENT_DER
    ;

valores : 
    valor DELIM_COMA valores
    | valor
    ;

valor :
    expresion_logica
    | expresion_aritmetica
    | cadena
    | DELIM_PARENT_IZQ valor DELIM_PARENT_DER
    ;

asignacion:
    identificadores_string OP_ASIGNACION CADENA
    | identificadores_real OP_ASIGNACION expresion_aritmetica
    | identificadores_entero OP_ASIGNACION expresion_aritmetica
    | identificadores_logico OP_ASIGNACION expresion_logica
    ;

identificadores_string:
    IDENTIFICADOR_STRING
    | IDENTIFICADOR_STRING DELIM_COMA identificadores_string
    ;

identificadores_real:
    IDENTIFICADOR_REAL
    | IDENTIFICADOR_REAL DELIM_COMA identificadores_real
    ;

identificadores_entero:
    IDENTIFICADOR_ENTERO
    | IDENTIFICADOR_ENTERO DELIM_COMA identificadores_entero
    ;

identificadores_logico:
    IDENTIFICADOR_LOGICO
    | IDENTIFICADOR_LOGICO DELIM_COMA identificadores_logico
    ;

cadena:
    CADENA
    | IDENTIFICADOR_STRING
    ;

estruc_control:
    estruc_seleccion
    | estruc_iterativa
    ;

estruc_seleccion:
    bloque_si
    | bloque_si bloque_sino

bloque_si:
    PAL_RES_SI DELIM_PARENT_IZQ expresion_logica DELIM_PARENT_DER PAL_RES_ENTONCES cuerpo
    ;

bloque_sino:
    PAL_RES_SINO cuerpo
    ;

estruc_iterativa:
    bloque_mientras
    | bloque_repetir
    ;

bloque_mientras:
    PAL_RES_MIENTRAS DELIM_PARENT_IZQ expresion_logica DELIM_PARENT_DER PAL_RES_HACER cuerpo
    ;

bloque_repetir:
    PAL_RES_REPETIR cuerpo PAL_RES_HASTA DELIM_PARENT_IZQ expresion_logica DELIM_PARENT_DER DELIM_PUNTO_COMA
    ;

expresion_logica:
    /* Para permitir la aparición recursiva de valores lógicos */
    expresion_logica operador_logico_booleano expresion_logica
    | OP_NOT expresion_logica
    /* Sintaxis para operadores válidos con expresiones aritméticas */
    | expresion_aritmetica operador_logico_aritmetico expresion_aritmetica
    /* Un valor lógico por sí mismo es válido como una expresión lógica */
    | valor_logico
    | operacion_logica
    /* La expresión lógica puede estar entre paréntesis */
    | DELIM_PARENT_IZQ expresion_logica DELIM_PARENT_DER
    ;

operador_logico_aritmetico:
    OP_MENOR | OP_MAYOR | OP_MENOR_IGUAL | OP_MAYOR_IGUAL
    ;

operador_logico_booleano:
    OP_AND | OP_OR | OP_IGUAL | OP_DIFERENTE
    ;

operacion_logica:
    /* Operaciones lógicas válidas con cadenas */
    IDENTIFICADOR_STRING OP_IGUAL IDENTIFICADOR_STRING
    | IDENTIFICADOR_STRING OP_DIFERENTE IDENTIFICADOR_STRING
    /* Operaciones lógicas válidas con reales y enteros */
    | numero operador_logico_aritmetico numero
    /* Operaciones lógicas válidas con lógicos */
    | valor_logico operador_logico_booleano valor_logico
    ;

valor_logico:
    PAL_RES_VERDADERO
    | PAL_RES_FALSO
    | IDENTIFICADOR_LOGICO
    ;

operador_aritmetico:
    OP_SUMA | OP_RESTA | OP_MULTIPLICACION | OP_DIVISION
    ;

expresion_aritmetica:
    /* Para permitir la aparición recursiva de valores numéricos */
    numero
    | expresion_aritmetica operador_aritmetico expresion_aritmetica
    /* Un valor numérico por sí mismo es válido como una expresión aritmética */
    /* La expresión aritmética puede estar entre paréntesis */
    | DELIM_PARENT_IZQ expresion_aritmetica DELIM_PARENT_DER
    ;

numero:
    n_real
    | n_entero
    ;

n_real:
    NUMERO_REAL
    | IDENTIFICADOR_REAL
    ;

n_entero:
    NUMERO_ENTERO
    | IDENTIFICADOR_ENTERO
    ;

%%

int yyerror(char *error)
{
	printf("Error: %s\n", error);
}

int main()
{
	yyparse();
	return 0;
}