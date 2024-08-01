import socket

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

    return checksum_received == checksum_calculated

def from_ascii_binary(binary_message):
    return ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])

# Configuración del socket
HOST = '127.0.0.1'
PORT = 65433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Escuchando en el puerto {PORT} para Fletcher-16...")
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conexión desde {addr}")
            message_with_checksum = conn.recv(1024).decode()
            print("Mensaje recibido:", message_with_checksum)
            if validate_fletcher16(message_with_checksum):
                original_message = message_with_checksum[:-16]
                print(f"No se detectaron errores. Mensaje original: {from_ascii_binary(original_message)}\n")
            else:
                print("Se detectaron errores y el mensaje se descarta.\n")
