def hamming_encode(data)
  n = data.length
  r = 0

  # Determinar el número de bits de paridad necesarios
  while (2**r - 1) < (n + r)
    r += 1
  end

  total_bits = n + r
  encoded = Array.new(total_bits, 0)

  j = 0
  for i in 0...total_bits
    if (i + 1 & i) == 0
      # Posiciones de paridad
      encoded[i] = 0
    else
      encoded[i] = data[j].to_i
      j += 1
    end
  end

  # Calcular bits de paridad
  for i in 0...r
    parity_pos = 2**i - 1
    parity = 0
    for j in parity_pos...total_bits
      if (j & (parity_pos + 1)) != 0
        parity ^= encoded[j]
      end
    end
    encoded[parity_pos] = parity
  end

  encoded.join
end

puts "Ingrese un mensaje en binario:"
message = gets.chomp

encoded_message = hamming_encode(message)
puts "Mensaje codificado con Hamming: #{encoded_message}"
