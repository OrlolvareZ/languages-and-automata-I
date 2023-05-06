# Instrucciones de compilación

```
    bison -dt sintaxis.y && flex lex.l && gcc lex.yy.c syntax.tab.c
```

## Para indicar el archivo de entrada

```
    ./a.out < testprog.txt
```