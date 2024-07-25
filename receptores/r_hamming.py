def hamming_decode(encoded):
    n = len(encoded)
    r = 0

    while (2**r - 1) < n:
        r += 1

    error_position = 0
    for i in range(r):
        parity_pos = 2**i - 1
        parity = 0
        j = parity_pos
        while j < n:
            for k in range(parity_pos + 1):
                if j + k < n:
                    parity ^= int(encoded[j + k])
            j += 2 * (parity_pos + 1)
        if parity != 0:
            error_position += parity_pos + 1

    if error_position != 0:
        print(f"Error detectado y corregido en la posición: {error_position}")
        encoded = list(encoded)
        encoded[error_position - 1] = str(1 - int(encoded[error_position - 1]))

    data = []
    for i in range(n):
        if (i & (i + 1)) != 0:
            data.append(encoded[i])

    return ''.join(data)

encoded_message = input("Ingrese el mensaje codificado en binario: ")

decoded_message = hamming_decode(encoded_message)
print(f"Mensaje decodificado: {decoded_message}")
