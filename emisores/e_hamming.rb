def hamming_encode(data)
  n = data.length
  r = 0

  while (2**r - 1) < (n + r)
    r += 1
  end

  total_bits = n + r
  encoded = Array.new(total_bits, 0)

  j = 0
  for i in 0...total_bits
    if (i & (i + 1)) == 0
      encoded[i] = 0
    else
      encoded[i] = data[j].to_i
      j += 1
    end
  end

  for i in 0...r
    parity_pos = 2**i - 1
    parity = 0
    j = parity_pos
    while j < total_bits
      for k in 0..parity_pos
        if j + k < total_bits
          parity ^= encoded[j + k]
        end
      end
      j += 2 * (parity_pos + 1)
    end
    encoded[parity_pos] = parity
  end

  encoded.join
end

puts "Ingrese un mensaje en binario:"
message = gets.chomp

encoded_message = hamming_encode(message)
puts "Mensaje codificado con Hamming: #{encoded_message}"
