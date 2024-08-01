require 'socket'
require 'csv'
require 'timeout'

def to_ascii_binary(message)
  message.chars.map { |char| char.ord.to_s(2).rjust(8, '0') }.join
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
    for j in 0...total_bits
      if j & (parity_pos + 1) != 0
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
  binary_message.chars.map do |bit|
    rand < error_rate ? (bit == '0' ? '1' : '0') : bit
  end.join
end

def generate_random_message(length)
  (0...length).map { (65 + rand(26)).chr }.join
end

# Definir los parámetros de prueba
message_lengths = [16, 32, 64, 128]
error_rates = [0,0.01, 0.05, 0.1]
algorithms = ["Hamming", "Fletcher-16"]
host = '127.0.0.1'

# Crear el archivo CSV para registrar los resultados
CSV.open("prueba_resultados.csv", "wb") do |csv|
  csv << ["Longitud", "Tasa de Error", "Algoritmo", "Mensaje Enviado"]

  # Iterar sobre los diferentes tamaños de mensajes, tasas de error y algoritmos
  message_lengths.each do |length|
    error_rates.each do |rate|
      algorithms.each do |algo|
        message = generate_random_message(length)
        binary_message = to_ascii_binary(message)

        case algo
        when "Hamming"
          encoded_message = hamming_encode(binary_message)
          message_with_checksum = encoded_message
          port = 65432
        when "Fletcher-16"
          checksum = fletcher16(binary_message)
          encoded_message = binary_message
          message_with_checksum = encoded_message + checksum
          port = 65433
        end

        noisy_message = apply_noise(message_with_checksum, rate)

        # Configuración del socket con retry y timeout
        begin
          Timeout.timeout(5) do
            Socket.tcp(host, port) do |socket|
              socket.write(noisy_message)
            end
          end
          puts "Mensaje codificado y con ruido enviado a través del puerto #{port}: #{noisy_message}"
        rescue Errno::ECONNREFUSED => e
          puts "Connection refused: #{e.message}"
        rescue Timeout::Error
          puts "Connection attempt timed out"
        end

        # Registrar los resultados en el archivo CSV
        csv << [length, rate, algo, noisy_message]

        # Agregar un timeout de 2 segundos después de cada llamada
      end
    end
  end
end

puts "Pruebas completadas. Los resultados se han guardado en prueba_resultados.csv."
