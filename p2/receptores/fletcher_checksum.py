import socket

def fletcher16(data):
    sum1 = 0
    sum2 = 0

    for byte in data:
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255

    return (sum2 << 8) | sum1

def validate_fletcher16(message):
    data = message[:-16]
    checksum_received = int(message[-16:], 2)

    checksum_calculated = fletcher16(data.encode())

    return checksum_received == checksum_calculated

# Configuración del socket
HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Conexión desde {addr}")
        message_with_checksum = conn.recv(1024).decode()
        if validate_fletcher16(message_with_checksum):
            original_message = message_with_checksum[:-16]
            print(f"No se detectaron errores. Mensaje original: {original_message}")
        else:
            print("Se detectaron errores y el mensaje se descarta.")
