import socket
import csv
import time

def hamming_decode(encoded):
    n = len(encoded)
    r = 0
    while (2**r - 1) < n:
        r += 1

    error_pos = 0
    for i in range(r):
        parity_pos = 2**i - 1
        parity = 0
        for j in range(parity_pos, n, 2 * (parity_pos + 1)):
            for k in range(j, min(j + parity_pos + 1, n)):
                parity ^= int(encoded[k])
        if parity:
            error_pos += 2**i

    if error_pos:
        if error_pos <= n:
            corrected = list(encoded)
            corrected[error_pos - 1] = '0' if corrected[error_pos - 1] == '1' else '1'
            decoded_message = ''.join(corrected)
        else:
            decoded_message = encoded
    else:
        decoded_message = encoded

    data_bits = []
    for i in range(n):
        if (i + 1) & i != 0:
            data_bits.append(decoded_message[i])
    return ''.join(data_bits), error_pos

def from_ascii_binary(binary_message):
    return ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])

HOST = '127.0.0.1'
PORT = 65432

with open("resultados_hamming.csv", "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Longitud", "Tasa de Error", "Errores Detectados", "Errores Corregidos", "Tiempo de Decodificación"])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Escuchando en el puerto {PORT} para Hamming...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión desde {addr}")
                noisy_message = conn.recv(1024).decode()
                print(f"Mensaje recibido: {noisy_message}")
                
                start_time = time.time()
                decoded_message, error_pos = hamming_decode(noisy_message)
                end_time = time.time()
                
                original_message = from_ascii_binary(decoded_message)
                
                longitud = len(noisy_message)
                tasa_error = noisy_message.count('1') / len(noisy_message)
                errores_detectados = error_pos > 0
                errores_corregidos = error_pos <= len(noisy_message)

                tiempo_decodificacion = end_time - start_time

                csvwriter.writerow([longitud, tasa_error, errores_detectados, errores_corregidos, tiempo_decodificacion])
                
                print(f"Mensaje decodificado: {original_message}")
                print(f"Errores detectados: {errores_detectados}")
                print(f"Errores corregidos: {errores_corregidos}")
                print(f"Tiempo de decodificación: {tiempo_decodificacion}\n")
