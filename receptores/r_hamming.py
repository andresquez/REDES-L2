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
    decoded_message = ''.join([decoded_message[i] for i in range(n) if not (i & (i + 1) == 0)])
    return decoded_message

encoded_message = input("Ingrese el mensaje codificado en binario: ")
decoded_message = hamming_decode(encoded_message)
print(f"Mensaje decodificado: {decoded_message}")
