require 'socket'

def to_ascii_binary(message)
  message.chars.map { |char| char.ord.to_s(2).rjust(8, '0') }.join
end

def from_ascii_binary(binary_message)
  binary_message.scan(/.{8}/).map { |byte| byte.to_i(2).chr }.join
end

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
    if (i + 1 & i) == 0
      encoded[i] = 0
    else
      encoded[i] = data[j].to_i
      j += 1
    end
  end

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

def fletcher16(data)
  sum1 = 0
  sum2 = 0

  data.each_byte do |byte|
    sum1 = (sum1 + byte) % 255
    sum2 = (sum2 + sum1) % 255
  end

  checksum = (sum2 << 8) | sum1
  checksum.to_s(2).rjust(16, '0')
end

def apply_noise(binary_message, error_rate)
  noisy_message = binary_message.chars.map do |bit|
    rand < error_rate ? (bit == '0' ? '1' : '0') : bit
  end.join
  noisy_message
end

HOST = '127.0.0.1'

loop do
  puts "Ingrese un mensaje en texto:"
  message = gets.chomp

  puts "Seleccione el algoritmo a utilizar:"
  puts "1. Hamming"
  puts "2. Fletcher-16"
  algorithm = gets.chomp.to_i

  binary_message = to_ascii_binary(message)
  puts "Mensaje en binario ASCII: #{binary_message}"

  case algorithm
  when 1
    encoded_message = hamming_encode(binary_message)
    puts "Mensaje codificado con Hamming: #{encoded_message}"
    message_with_checksum = encoded_message
    port = 65432
  when 2
    checksum = fletcher16(binary_message)
    puts "Checksum de Fletcher-16: #{checksum}"
    encoded_message = binary_message
    message_with_checksum = encoded_message + checksum
    puts "Mensaje con checksum de Fletcher-16: #{message_with_checksum}"
    port = 65433
  else
    puts "Opción no válida."
    next
  end

  puts "Ingrese la tasa de error (por ejemplo, 0.01 para 1%):"
  error_rate = gets.to_f

  noisy_message = apply_noise(message_with_checksum, error_rate)

  # Configuración del socket
  Socket.tcp(HOST, port) do |socket|
    socket.write(noisy_message)
  end

  puts "Mensaje codificado y con ruido enviado a través del puerto #{port}: #{noisy_message}"

  puts "¿Desea enviar otro mensaje? (s/n)"
  break if gets.chomp.downcase != 's'
end
