# Instrucciones de compilación

```
    bison -dt sintaxis.y && flex a_lexico.lex && gcc lex.yy.c sintaxis.tab.c
```

## Para indicar el archivo de entrada

```
    ./a.out < testprog.txt
```