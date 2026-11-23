from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.Random import get_random_bytes

# Generate a random 8-byte DES key
key = input("8-Character Symmetric Key: ").encode('utf-8')

# Message to encrypt
message = input("Message: ")

# Convert message to bytes
data = message.encode('utf-8')

# Create DES cipher using CBC mode
cipher = DES.new(key, DES.MODE_CBC)

# Encrypt the message
padded_data = pad(data, DES.block_size)
encrypted_data = cipher.encrypt(padded_data)

# Encode ciphertext and IV using Base64
encrypted_message = base64.b64encode(
    cipher.iv + encrypted_data
).decode('utf-8')


print("Symmetric Key    :", key.hex())
print("Original Message :", message)
print("Data             :", message.encode('utf-8').hex())
print("Padded Data      :", padded_data.hex())
print("Encrypted Data   :",encrypted_data.hex())
print("Encrypted Message:", encrypted_message)

# Decryption
decoded_data = base64.b64decode(encrypted_message)

iv = decoded_data[:8]
cipherdata = decoded_data[8:]

decrypt_cipher = DES.new(key, DES.MODE_CBC, iv)
decrypted_data = unpad(
    decrypt_cipher.decrypt(cipherdata),
    DES.block_size
)
print("Cipher Data      :", cipherdata.hex())
print("Decrypted Data   :", decrypted_data.hex())
print("Decrypted Message:", decrypted_data.decode('utf-8'))