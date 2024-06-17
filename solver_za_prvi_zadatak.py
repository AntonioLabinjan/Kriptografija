import struct
from functools import reduce

def XOR(xs):
    return bytes([reduce(int.__xor__, list(xs))])

def read_bin_file(file_path):
    with open(file_path, 'rb') as file:
        while True:
            # Read the structure
            # 'I' for 32-bit unsigned int
            # '255p' for Pascal string up to 255 bytes
            # '4p' for Pascal string of 4 bytes (3 characters + length byte)
            # 'B' for 1 byte unsigned int
            # 'q' for 64-bit signed integer
            # 'b' for 1 byte signed int (checksum)
            record_format = 'I255p4pBqB'
            record_size = struct.calcsize(record_format)
            data = file.read(record_size)
            
            if not data:
                break  # End of file
            
            unpacked_data = struct.unpack(record_format, data)
            
            serial = unpacked_data[0]
            name = unpacked_data[1].decode('utf-8').rstrip('\x00')
            currency = unpacked_data[2].decode('utf-8').rstrip('\x00')
            decimals = unpacked_data[3]
            amount = unpacked_data[4]
            checksum = unpacked_data[5]
            
            # Verify checksum
            expected_checksum = XOR(data[:-1])
            if checksum != expected_checksum[0]:
                print(f"Checksum error in record with serial: {serial}")
            
            # Print the unpacked data
            print(f"Serial: {serial}")
            print(f"Name: {name}")
            print(f"Currency: {currency}")
            print(f"Decimals: {decimals}")
            print(f"Amount: {amount}")
            print(f"Checksum: {checksum}\n")

# Example usage
file_path = 'data.bin'
read_bin_file(file_path)
