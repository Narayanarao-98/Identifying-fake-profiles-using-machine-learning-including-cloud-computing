from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Fixed 16-byte key (128-bit key for AES)
key = b'ThisIsA16ByteKey'  # Must be 16 bytes for AES-128

# Function to encrypt data
def encrypt_data(data):
    # Create a new AES cipher object in ECB mode (no IV needed)
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Pad data to ensure it's a multiple of block size (16 bytes for AES)
    padded_data = pad(data.encode(), AES.block_size)
    
    # Encrypt the data
    ciphertext = cipher.encrypt(padded_data)
    
    # Return the ciphertext encoded in base64
    ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
    
    return ciphertext_base64

# Function to decrypt data
def decrypt_data(ciphertext_base64):
    # Decode the base64-encoded ciphertext
    ciphertext = base64.b64decode(ciphertext_base64)
    
    # Create a new AES cipher object in ECB mode with the same key
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Decrypt the data
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return decrypted_data.decode()

# # Example usage
# data = "This is a secret message!"
# encrypted_data = encrypt_data(data)
# print("Encrypted Data:", encrypted_data)

# # Decrypt the data
# decrypted_data = decrypt_data(encrypted_data)
# print("Decrypted Data:", decrypted_data)
