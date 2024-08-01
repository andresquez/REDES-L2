import socket
import csv
import time

def fletcher16(data):
    sum1 = 0
    sum2 = 0

    for byte in data.encode():
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255

    return (sum2 << 8) | sum1

def validate_fletcher16(message):
    data = message[:-16]
    checksum_received = int(message[-16:], 2)
    checksum_calculated = fletcher16(data)
    return checksum_received == checksum_calculated, checksum_calculated

def from_ascii_binary(binary_message):
    return ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])

HOST = '127.0.0.1'
PORT = 65433

with open("resultados_fletcher.csv", "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Longitud", "Tasa de Error", "Errores Detectados", "Errores Corregidos", "Tiempo de Decodificación"])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Escuchando en el puerto {PORT} para Fletcher-16...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión desde {addr}")
                message_with_checksum = conn.recv(1024).decode()
                print(f"Mensaje recibido: {message_with_checksum}")

                start_time = time.time()
                valid, _ = validate_fletcher16(message_with_checksum)
                end_time = time.time()
                
                if valid:
                    original_message = message_with_checksum[:-16]
                    errores_detectados = False
                    errores_corregidos = False
                    decoded_message = from_ascii_binary(original_message)
                else:
                    original_message = "ERROR"
                    errores_detectados = True
                    errores_corregidos = False
                    decoded_message = "ERROR"

                longitud = len(message_with_checksum)
                tasa_error = message_with_checksum.count('1') / len(message_with_checksum)
                tiempo_decodificacion = end_time - start_time

                csvwriter.writerow([longitud, tasa_error, errores_detectados, errores_corregidos, tiempo_decodificacion])
                
                print(f"Mensaje decodificado: {decoded_message}")
                print(f"Errores detectados: {errores_detectados}")
                print(f"Errores corregidos: {errores_corregidos}")
                print(f"Tiempo de decodificación: {tiempo_decodificacion}\n")
