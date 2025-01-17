import socket

def hamming_decode(encoded):
    n = len(encoded)
    r = 0
    while (2**r - 1) < n:
        r += 1

    # Detectar errores
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
            # Corregir el bit
            corrected = list(encoded)
            corrected[error_pos - 1] = '0' if corrected[error_pos - 1] == '1' else '1'
            print(f"Error detectado y corregido en la posición: {error_pos}")
            decoded_message = ''.join(corrected)
        else:
            print("Error no corregible detectado.")
            decoded_message = encoded
    else:
        print("No se detectaron errores.")
        decoded_message = encoded

    # Eliminar bits de paridad
    data_bits = []
    for i in range(n):
        if (i + 1) & i != 0:
            data_bits.append(decoded_message[i])
    return ''.join(data_bits)

def from_ascii_binary(binary_message):
    return ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])

# Configuración del socket
HOST = '127.0.0.1'
PORT = 65432

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
            decoded_message = hamming_decode(noisy_message)
            original_message = from_ascii_binary(decoded_message)
            print(f"Mensaje decodificado: {original_message}\n")
