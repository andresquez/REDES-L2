import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos desde los archivos CSV
df_fletcher = pd.read_csv("resultados_fletcher.csv")
df_hamming = pd.read_csv("resultados_hamming.csv")

# Convertir tiempos de decodificación a flotantes para análisis
df_fletcher['Tiempo de Decodificación'] = df_fletcher['Tiempo de Decodificación'].astype(float)
df_hamming['Tiempo de Decodificación'] = df_hamming['Tiempo de Decodificación'].astype(float)

# Comparación del tiempo de ejecución según la longitud de la cadena para ambos algoritmos
def plot_execution_time_comparison(df_fletcher, df_hamming):
    plt.figure(figsize=(12, 6))
    
    # Graficar el tiempo de ejecución para Fletcher-16
    plt.plot(df_fletcher['Longitud'], df_fletcher['Tiempo de Decodificación'], marker='o', color='red', label='Fletcher-16')
    
    # Graficar el tiempo de ejecución para Hamming
    plt.plot(df_hamming['Longitud'], df_hamming['Tiempo de Decodificación'], marker='o', color='blue', label='Hamming')
    
    plt.xlabel('Longitud del Mensaje')
    plt.ylabel('Tiempo de Decodificación (s)')
    plt.title('Comparación del Tiempo de Ejecución Según la Longitud de la Cadena')
    plt.legend()
    plt.grid(True)
    plt.show()

# Gráfica de barras comparando errores detectados y errores corregidos entre los dos algoritmos
def plot_errors_comparison(df_fletcher, df_hamming):
    plt.figure(figsize=(12, 6))
    
    # Agrupar errores detectados y corregidos por algoritmo
    labels = ['Errores Detectados', 'Errores Corregidos']
    fletcher_errors = [df_fletcher['Errores Detectados'].sum(), df_fletcher['Errores Corregidos'].sum()]
    hamming_errors = [df_hamming['Errores Detectados'].sum(), df_hamming['Errores Corregidos'].sum()]
    
    x = range(len(labels))
    
    # Graficar los errores para Fletcher-16
    plt.bar(x, fletcher_errors, width=0.4, label='Fletcher-16', color='red', align='center')
    
    # Graficar los errores para Hamming
    plt.bar([i + 0.4 for i in x], hamming_errors, width=0.4, label='Hamming', color='blue', align='center')
    
    plt.xlabel('Tipo de Error')
    plt.ylabel('Cantidad')
    plt.title('Comparación de Errores Detectados y Corregidos entre Algoritmos')
    plt.xticks([i + 0.1 for i in x], labels)
    plt.legend()
    plt.grid(axis='y')
    plt.show()

# Llamar a las funciones de visualización
plot_execution_time_comparison(df_fletcher, df_hamming)
plot_errors_comparison(df_fletcher, df_hamming)


def plot_detected_errors_vs_message_length(df_fletcher, df_hamming):
    plt.figure(figsize=(12, 6))
    
    # Agrupar errores detectados por longitud del mensaje
    grouped_fletcher = df_fletcher.groupby('Longitud')['Errores Detectados'].sum()
    grouped_hamming = df_hamming.groupby('Longitud')['Errores Detectados'].sum()
    
    lengths = sorted(set(grouped_fletcher.index) | set(grouped_hamming.index))
    fletcher_errors = [grouped_fletcher.get(length, 0) for length in lengths]
    hamming_errors = [grouped_hamming.get(length, 0) for length in lengths]
    
    x = range(len(lengths))
    
    # Graficar los errores detectados
    plt.bar(x, fletcher_errors, width=0.4, label='Fletcher-16', color='red', align='center')
    plt.bar([i + 0.4 for i in x], hamming_errors, width=0.4, label='Hamming', color='blue', align='center')
    
    plt.xlabel('Longitud del Mensaje')
    plt.ylabel('Errores Detectados')
    plt.title('Errores Detectados vs Longitud del Mensaje')
    plt.xticks([i + 0.2 for i in x], lengths)
    plt.legend()
    plt.grid(axis='y')
    plt.show()

# Llamar a la función de visualización
plot_detected_errors_vs_message_length(df_fletcher, df_hamming)
