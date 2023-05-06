# Instrucciones de compilación

```
    bison -dt syntax.y && flex lex.l && gcc lex.yy.c syntax.tab.c
    ./a.out < testprog.txt
```

## Para indicar el archivo de entrada

```
    ./a.out < testprog.txt
```