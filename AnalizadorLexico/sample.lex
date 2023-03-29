/* Sección de definición */
%{

int numLinea = 1;
FILE *apuntadorArchivo;
FILE *apuntadorArchivoErrores;

void escribirLexema(char *lexema, int token, int posTab, int numLinea);
void escribirError(char *lexema, char *desc, int numLinea);

%}

/* Sección de reglas (exp. regulares) */
%%

[ \t\r]         { }         /* los espacios en blanco no generan tokens */

[a-zA-Z]([a-zA-Z]|"_"|[0-9])*"$" { escribirLexema(yytext, -53, -2, numLinea); }
[a-zA-Z]([a-zA-Z]|"_"|[0-9])*"%" { escribirLexema(yytext, -52, -2, numLinea); }
[a-zA-Z]([a-zA-Z]|"_"|[0-9])*"&" { escribirLexema(yytext, -51, -2, numLinea); }
[a-zA-Z]([a-zA-Z]|"_"|[0-9])*"@" { escribirLexema(yytext, -54, -2, numLinea); }
[a-zA-Z]([a-zA-Z]|"_"|[0-9])*    { escribirLexema(yytext, -55, -2, numLinea); }

"-"             { escribirLexema(yytext, -25, -1, numLinea); }
"+"             { escribirLexema(yytext, -24, -1, numLinea); }
"/"             { escribirLexema(yytext, -22, -1, numLinea); }
"*"             { escribirLexema(yytext, -21, -1, numLinea); }
"="             { escribirLexema(yytext, -26, -1, numLinea); }

"<"             { escribirLexema(yytext, -31, -1, numLinea); }
">"             { escribirLexema(yytext, -33, -1, numLinea); }
"<="            { escribirLexema(yytext, -32, -1, numLinea); }
">="            { escribirLexema(yytext, -34, -1, numLinea); }
"=="            { escribirLexema(yytext, -35, -1, numLinea); }
"!="            { escribirLexema(yytext, -36, -1, numLinea); }

"&"             { escribirLexema(yytext, -41, -1, numLinea); }
"|"             { escribirLexema(yytext, -42, -1, numLinea); }
"!"             { escribirLexema(yytext, -43, -1, numLinea); }

"programa"      { escribirLexema(yytext, -1, -1, numLinea); }
"inicio"        { escribirLexema(yytext, -2, -1, numLinea); }
"fin"           { escribirLexema(yytext, -3, -1, numLinea); }
"leer"          { escribirLexema(yytext, -4, -1, numLinea); }
"escribir"      { escribirLexema(yytext, -5, -1, numLinea); }
"entero"        { escribirLexema(yytext, -11, -1, numLinea); }
"real"          { escribirLexema(yytext, -12, -1, numLinea); }
"cadena"        { escribirLexema(yytext, -13, -1, numLinea); }
"logico"        { escribirLexema(yytext, -14, -1, numLinea); }
"si"            { escribirLexema(yytext, -6, -1, numLinea); }
"sino"          { escribirLexema(yytext, -7, -1, numLinea); }
"entonces"      { escribirLexema(yytext, -16, -1, numLinea); }
"mientras"      { escribirLexema(yytext, -17, -1, numLinea); }
"hacer"         { escribirLexema(yytext, -14, -1, numLinea); }
"repetir"       { escribirLexema(yytext, -9, -1, numLinea); }
"hasta"         { escribirLexema(yytext, -10, -1, numLinea); }
"variable"      { escribirLexema(yytext, -15, -1, numLinea); }

"("             { escribirLexema(yytext, -73, -1, numLinea); }
")"             { escribirLexema(yytext, -74, -1, numLinea); }
";"             { escribirLexema(yytext, -75, -1, numLinea); }
","             { escribirLexema(yytext, -76, -1, numLinea); }
":"             { escribirLexema(yytext, -77, -1, numLinea); }

"//".+"//"      { /* Los comentarios no generan tokens */ }

[0-9]+          { escribirLexema(yytext, -61, -1, numLinea); }
[0-9]+"."[0-9]+ { escribirLexema(yytext, -62, -1, numLinea); }
\".*\"          { escribirLexema(yytext, -63, -1, numLinea); }
"verdadero"     { escribirLexema(yytext, -64, -1, numLinea); }
"falso"         { escribirLexema(yytext, -65, -1, numLinea); }

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

    FILE *apuntadorArchivoLenguaje;
    apuntadorArchivoLenguaje = fopen(args[1], "r");
    yyin = apuntadorArchivoLenguaje;

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