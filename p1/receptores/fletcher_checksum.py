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

    if checksum_received == checksum_calculated:
        return data
    else:
        return None

message_with_checksum = input("Ingrese el mensaje con checksum en binario: ")

original_message = validate_fletcher16(message_with_checksum)

if original_message:
    print(f"No se detectaron errores. Mensaje original: {original_message}")
else:
    print("Se detectaron errores y el mensaje se descarta.")
