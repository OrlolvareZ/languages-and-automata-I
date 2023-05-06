/* Sección de definición */
%{
    #include "syntax.tab.h"
    int num_linea = 0;
%}

/* Sección de reglas */
%%

[ \t\r]         { }
"//".+"//"      { }
\n              { num_linea++; }

[a-zA-Z]([a-zA-Z]|_|[0-9])*"$" { return IDENTIFICADOR_STRING; }
[a-zA-Z]([a-zA-Z]|_|[0-9])*"%" { return IDENTIFICADOR_REAL; }
[a-zA-Z]([a-zA-Z]|_|[0-9])*"&" { return IDENTIFICADOR_ENTERO; }
[a-zA-Z]([a-zA-Z]|_|[0-9])*"@" { return IDENTIFICADOR_LOGICO; }
[a-zA-Z]([a-zA-Z]|_|[0-9])*"?" { return IDENTIFICADOR_PROGRAMA; }

"-"             { return OP_RESTA; }
"+"             { return OP_SUMA; }
"/"             { return OP_DIVISION; }
"*"             { return OP_MULTIPLICACION; }
"="             { return OP_ASIGNACION; }

"<"             { return OP_MENOR; }
">"             { return OP_MAYOR; }
"<="            { return OP_MENOR_IGUAL; }
">="            { return OP_MAYOR_IGUAL; }
"=="            { return OP_IGUAL; }
"!="            { return OP_DIFERENTE; }

"&"             { return OP_AND; }
"|"             { return OP_OR; }
"!"             { return OP_NOT; }

"programa"      { return PAL_RES_PROGRAMA; }
"inicio"        { return PAL_RES_INICIO; }
"fin"           { return PAL_RES_FIN; }
"leer"          { return PAL_RES_LEER; }
"escribir"      { return PAL_RES_ESCRIBIR; }
"entero"        { return PAL_RES_ENTERO; }
"real"          { return PAL_RES_REAL; }
"cadena"        { return PAL_RES_CADENA; }
"logico"        { return PAL_RES_LOGICO; }
"si"            { return PAL_RES_SI; }
"sino"          { return PAL_RES_SINO; }
"entonces"      { return PAL_RES_ENTONCES; }
"mientras"      { return PAL_RES_MIENTRAS; }
"hacer"         { return PAL_RES_HACER; }
"repetir"       { return PAL_RES_REPETIR; }
"hasta"         { return PAL_RES_HASTA; }
"variable"      { return PAL_RES_VARIABLE; }

"("             { return DELIM_PARENT_IZQ; }
")"             { return DELIM_PARENT_DER; }
";"             { return DELIM_PUNTO_COMA; }
","             { return DELIM_COMA; }
":"             { return DELIM_DOS_PUNTOS; }

[0-9]+          { return NUMERO_ENTERO; }
[0-9]+\.[0-9]+  { return NUMERO_REAL; }
    
\".*\"          { return CADENA; }

"verdadero"     { return PAL_RES_VERDADERO; }
"falso"         { return PAL_RES_FALSO; }

.               { printf("Token inválido (%s) en la línea (%d)\n", yytext, num_linea); return -1; }

%%

int yywrap() { }
