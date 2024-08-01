require 'socket'

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

puts "Ingrese un mensaje en binario:"
message = gets.chomp

checksum = fletcher16(message)
message_with_checksum = message + checksum

# Configuración del socket
HOST = '127.0.0.1'
PORT = 65432

Socket.tcp(HOST, PORT) do |socket|
  socket.write(message_with_checksum)
end

puts "Mensaje con checksum enviado."
