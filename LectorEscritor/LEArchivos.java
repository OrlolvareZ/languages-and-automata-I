package LectorEscritor;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/*
 * Clase que contiene los metodos para leer y escribir a un archivo,
 * así como conocer el número de líneas por archivo, el número de palabras por línea y la cantidad de palabras totales en el archivo.
 * 
 * Fecha: 8 de febrero del 2023
 * Autores: Nayely Cortes, Yulisa Lara, Orlando Alvarez
*/

public class LEArchivos{

    private int totalLineas; 
    private int totalPalabras;

    public LEArchivos() {
        totalLineas = 0;
        totalPalabras = 0;
    }

    public int getTotalLineas() {
        return totalLineas;
    }

    public int getTotalPalabras() {
        return totalPalabras;
    }
    
    public void setTotalLineas(int NuevaTotalLineas){
        this.totalLineas = NuevaTotalLineas; 
    }

    public void setTotalPalabras(int NuevaTotalPalabras){
        this.totalPalabras = NuevaTotalPalabras; 
    }

    /*
     * Método que guarda un texto en un archivo de texto
     * @param texto Texto a guardar
     * @param nombreArchivo Nombre del archivo
     * @throws IOException Si ocurre un error al guardar el archivo
     */
    public void guardarTexto(String texto, String nombreArchivo) throws IOException {
        try {

            File archivo = new File(nombreArchivo); 

            // Renombra el archivo si existe
            int numArchivo = 0;
            while (archivo.exists()) {
                archivo.renameTo(new File(nombreArchivo + " (" + numArchivo + ")"));
                numArchivo++;
            }

            FileWriter escritor = new FileWriter(nombreArchivo, true);
            escritor.write(texto + "\n");
            escritor.close();

        } catch (IOException ex) {
            throw ex;
        }
    }

    /*
     * Método que lee un archivo de texto y lo muestra en pantalla
     * @param ruta Ruta del archivo
     * @return Texto del archivo
     * @throws IOException Si ocurre un error al leer el archivo
     */
    public String leerTexto(String ruta) throws IOException {

        // Crear un flujo para leer archivos de texto
        FileReader lector = new FileReader(ruta);
        BufferedReader br = new BufferedReader(lector);
        String linea;
        StringBuffer texto = new StringBuffer();

        try {

            // Mientras que haya lineas en el archivo
            while ((linea = br.readLine()) != null) {

                totalLineas++;
                
                // Separar las palabras por espacios
                String[] palabras = linea.split(" ");
                int palabrasPorLinea = 0;

                // Dejar de contar palabras si la linea es vacia
                if ( !(palabras[0].equals("")) )  {
                    totalPalabras += palabras.length;
                    palabrasPorLinea = palabras.length;
                }

                texto.append(String.format("(%d) %s\n", palabrasPorLinea, linea));
            
            }
            if (br != null) {
                lector.close();
            }

        } catch (IOException ex) {
            throw ex;
        }

        return texto.toString();
    }

}