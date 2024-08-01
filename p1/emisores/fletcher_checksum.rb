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
puts "Mensaje con checksum: #{message + checksum}"
