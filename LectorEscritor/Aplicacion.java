package LectorEscritor;

import java.io.IOException;

import javax.swing.JFileChooser;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

public class Aplicacion {

    public static void main(String[] args) {

        // Crea un menú con JOptionPane que tenga botones para leer un archivo, crear un archivo y salir.
        String[] opciones = {"Leer archivo", "Crear archivo", "Salir"};
        LEArchivos lea = new LEArchivos();
        
        // Se inicializan los componentes donde se desplegará/escribirá el texto del archivo
        JTextArea areaTexto = new JTextArea();
        JScrollPane scroll = new JScrollPane(areaTexto);
        scroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        scroll.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);

        while(true){
            
            // Se pregunta al usuario qué desea hacer
            int opcion = JOptionPane.showOptionDialog(
                null, 
                "¡Bienvenido! Seleccione una opción", 
                "Menú lector/escritor de archivos",
                JOptionPane.DEFAULT_OPTION, 
                JOptionPane.INFORMATION_MESSAGE, 
                null, 
                opciones, 
                null);

            switch(opcion){
    
                // Opción de leer un archivo
                case 0:

                    // Reiniciar la cuenta de líneas y palabras tras cada lectura
                    lea.setTotalLineas(0);
                    lea.setTotalPalabras(0);

                    areaTexto.setEditable(false);
    
                    // Abrir el archivo con un JFileChooser
                    JFileChooser fileChooser = new JFileChooser();
                    fileChooser.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter("Archivos de texto", "txt"));
                    int caso = fileChooser.showOpenDialog(null);

                    if (caso == JFileChooser.APPROVE_OPTION)
                    {
                        
                        String ruta = fileChooser.getSelectedFile().getAbsolutePath();
                        
                        try {

                            String contenido = lea.leerTexto(ruta);
                            // Cargar el contenido y los totales de líneas y palabras
                            areaTexto.setText(contenido);
                            int totalPalabras = lea.getTotalPalabras();
                            int totalLineas = lea.getTotalLineas();
                            JLabel etiquetaPalabras = new JLabel("Total de palabras: " + totalPalabras);
                            JLabel etiquetaLineas = new JLabel("Total de líneas: " + totalLineas);
                            JPanel panel = new JPanel();

                            // Se agregan los componentes al panel y se configura su distribución
                            panel.setLayout(new javax.swing.BoxLayout(panel, javax.swing.BoxLayout.Y_AXIS));
                            panel.setPreferredSize(new java.awt.Dimension(600, 420));
                            scroll.setPreferredSize(new java.awt.Dimension(600, 400)); 
                            panel.add(scroll);
                            panel.add(etiquetaPalabras);
                            panel.add(etiquetaLineas);

                            JOptionPane.showMessageDialog(null, panel, "Contenido del archivo", JOptionPane.PLAIN_MESSAGE);
                            
                        } catch (IOException ex) {
                            JOptionPane.showMessageDialog(null, "Error al leer el archivo", "Error", JOptionPane.ERROR_MESSAGE);
                        }
                    }
    
                break;
    
                // Opción de escribir en archivo
                case 1:
                
                    areaTexto.setEditable(true);
                    // Se limpia el panel
                    areaTexto.setText("");
                
                    // Se agregan los componentes al panel y se configura su distribución y tamaño
                    JPanel panel = new JPanel();
                    panel.setPreferredSize(new java.awt.Dimension(600, 420));
                    scroll.setPreferredSize(new java.awt.Dimension(600, 400));                   
                    panel.add(scroll);

                    // Se abre un nuevo flujo para evitar que al cancelar el guardado se pierda el texto
                    flujoEscritura : while(true) {
                        
                        int opcionGuardar = JOptionPane.showConfirmDialog(null, panel, "Escriba el contenido del nuevo archivo", JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
        
                        if (opcionGuardar == JOptionPane.OK_OPTION)
                        {
                            // Guarda el texto en un archivo con un JFileChooser
                            JFileChooser fileChooserGuardar = new JFileChooser();
                            int casoGuardar = fileChooserGuardar.showSaveDialog(null);
        
                            if (casoGuardar == JFileChooser.APPROVE_OPTION)
                            {
                                String nombreArchivo = fileChooserGuardar.getSelectedFile().getAbsolutePath();
                                String texto = areaTexto.getText();
        
                                // Se guarda el texto ingresado en el área de texto
                                try {
                                    lea.guardarTexto(
                                        texto,
                                        nombreArchivo + (nombreArchivo.contains(".txt") ? "" : ".txt") // Si el nombre del archivo no contiene la extensión, se agrega
                                        );
                                    JOptionPane.showMessageDialog(null, "El texto se guardó correctamente", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                                    break flujoEscritura;
                                } catch (IOException ex) {
                                    JOptionPane.showMessageDialog(null, "Error al guardar el archivo", "Error", JOptionPane.ERROR_MESSAGE);
                                }
                            }
                        }
                        else{
                            break flujoEscritura;
                        }
                    }

                break;
    
                // Salir
                default:
    
                    System.exit(0);
    
            }
        }
        
    }

    
}
