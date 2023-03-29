/* Sección de definición */
%{

    int numLinea = 1;
    FILE *apuntadorArchivo;
    FILE *apuntadorArchivoErrores;

    void escribirLexema(char *lexema, int token, int posTab, int numLinea)
    void escribirError(char *lexema, char *desc, int numLinea)

%}

/* Sección de reglas (exp. regulares) */
%%

    [ \t\r]         // los espacios en blanco no generan tokens

    /*
        Identificadores
        - Inician con una letra y pueden contener más letras y/o guión bajo y/o números
        - Al final se concatenerá un caracter de control:
            $ para identificadores string
            % para identificadores de valor real
            & para identificadores de valor entero
            @ para identificadores de valor lógico
        - Los identificadores tendrán el valor -2 en la tabla de símbolos,
          cualquier otro tipo de lexema tendrá -1
    */
    [a-zA-Z]([a-zA-Z]|"_"|[0-9])*"$" { escribirLexema(yytext, -53, -2, numLinea); }
    [a-zA-Z]([a-zA-Z]|"_"|[0-9])*"%" { escribirLexema(yytext, -52, -2, numLinea); }
    [a-zA-Z]([a-zA-Z]|"_"|[0-9])*"&" { escribirLexema(yytext, -51, -2, numLinea); }
    [a-zA-Z]([a-zA-Z]|"_"|[0-9])*"@" { escribirLexema(yytext, -54, -2, numLinea); }
    [a-zA-Z]([a-zA-Z]|"_"|[0-9])*    { escribirLexema(yytext, -55, -2, numLinea); }

    /* Operadores aritméticos */
    "-"             { escribirLexema(yytext, -25, -2, numLinea); }
    "+"             { escribirLexema(yytext, -24, -2, numLinea); }
    "/"             { escribirLexema(yytext, -22, -2, numLinea); }
    "*"             { escribirLexema(yytext, -21, -2, numLinea); }
    "="             { escribirLexema(yytext, -26, -2, numLinea); }

    /* Operadores relacionales */
    "<"             { escribirLexema(yytext, -31, -2, numLinea); }
    ">"             { escribirLexema(yytext, -33, -2, numLinea); }
    "<="            { escribirLexema(yytext, -32, -2, numLinea); }
    ">="            { escribirLexema(yytext, -34, -2, numLinea); }
    "=="            { escribirLexema(yytext, -35, -2, numLinea); }
    "!="            { escribirLexema(yytext, -36, -2, numLinea); }

    /* Operadores lógicos */
    "&"             { escribirLexema(yytext, -41, -2, numLinea); }
    "|"             { escribirLexema(yytext, -42, -2, numLinea); }
    "!"             { escribirLexema(yytext, -43, -2, numLinea); }

    /* Palabras reservadas */
    "programa"      { escribirLexema(yytext, -1, -2, numLinea); }
    "inicio"        { escribirLexema(yytext, -2, -2, numLinea); }
    "fin"           { escribirLexema(yytext, -3, -2, numLinea); }
    "leer"          { escribirLexema(yytext, -4, -2, numLinea); }
    "escribir"      { escribirLexema(yytext, -5, -2, numLinea); }
    "entero"        { escribirLexema(yytext, -11, -2, numLinea); }
    "real"          { escribirLexema(yytext, -12, -2, numLinea); }
    "cadena"        { escribirLexema(yytext, -13, -2, numLinea); }
    "logico"        { escribirLexema(yytext, -14, -2, numLinea); }
    "si"            { escribirLexema(yytext, -6, -2, numLinea); }
    "sino"          { escribirLexema(yytext, -7, -2, numLinea); }
    "entonces"      { escribirLexema(yytext, -16, -2, numLinea); }
    "mientras"      { escribirLexema(yytext, -17, -2, numLinea); }
    "hacer"         { escribirLexema(yytext, -14, -2, numLinea); }
    "repetir"       { escribirLexema(yytext, -9, -2, numLinea); }
    "hasta"         { escribirLexema(yytext, -10, -2, numLinea); }
    "variable"      { escribirLexema(yytext, -15, -2, numLinea); }

    /* Caracteres especiales */
    "("             { escribirLexema(yytext, -73, -2, numLinea); }
    ")"             { escribirLexema(yytext, -74, -2, numLinea); }
    ";"             { escribirLexema(yytext, -75, -2, numLinea); }
    ","             { escribirLexema(yytext, -76, -2, numLinea); }
    ":"             { escribirLexema(yytext, -77, -2, numLinea); }

    /*
        Comentarios
        - Inician y terminan con // y puede contener cualquier otro caracter
        - No puede estar vacío
        - Se considera una sola línea.
    */
    "//".+"//"      { }

    /*
        Números enteros (constante entera)
        - No incluye negativos
    */
    [0-9]+          { escribirLexema(yytext, -61, -2, numLinea); }
    /*
        Números reales (constante real)
        - Números seguido de punto seguido de números
        - No incluye notación científica
    */
    [0-9]+\.[0-9]+  { escribirLexema(yytext, -62, -2, numLinea); }
    /*
        Cadenas (constante cadena)
        - Va limitada por “ al inicio y al final
        - Se considera una sola linea
    */
    "\"".*"\""          { escribirLexema(yytext, -63, -2, numLinea); }
    /*
        Valor lógico (constnate lógica)
        - Verdadero o falso
    */
    "verdadero"     { escribirLexema(yytext, -64, -2, numLinea); }
    "falso"         { escribirLexema(yytext, -65, -2, numLinea); }

    \n              { numLinea++; }

    .               { escribirError(yytext, "Token no reconocido", numLinea); }

%%

void escribirLexema(char *lexema, int token, int posTab, int numLinea)
{
    fprintf(apuntadorArchivo,
        "| %-14s| %-15d| %-19d| %-12d|\n",
        lexema, token, posTab, numLinea
    );
    
}

void escribirError(char *lexema, char *desc, int numLinea)
{
    fprintf(apuntadorArchivoErrores,
        "| %-14s | %-30s| %-10d|\n",
        lexema, desc, numLinea
    );

}

int yywrap() { }

int main(int length, char **args)
{
    if (length == 1)
    {
        printf("Error: por favor especifica la ruta del archivo\n");
        return 1;
    }

    FILE *apuntadorArchivo;
    apuntadorArchivo = fopen("./tokens.txt", "w");

    fprintf(apuntadorArchivo, "\n"
        "|************************Tabla de tokens************************|\n"
        "| Lexema       | Token         | Posición en tabla | # de línea |\n"
        "|**************|***************|*******************|************|\n"
    );

    FILE *apuntadorArchivoErrores;
    apuntadorArchivoErrores = fopen("./errors.txt", "w");

    fprintf(apuntadorArchivoErrores, "\n"
        "|***********************Tabla de errores************************|\n"
        "| Lexema       | Descripción                       | # de línea |\n"
        "|**************|***********************************|************|\n"
    );

    yylex();
    
    fclose(apuntadorArchivo);
    fclose(apuntadorArchivoErrores);
    
    /* 
        ep = fopen("./errors.tmp", "r");
        char ch;
        while ((ch = fgetc(ep)) != EOF)
            putchar(ch);
        fclose(ep);
        printf("\n");
    */

    return 0;
}