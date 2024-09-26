import json
import base64
import qrcode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def main():
    # Get user input
    user_input = input("Enter data to encrypt (string, dict, boolean, etc.): ")

    # Try to parse input as JSON; if it fails, treat as a string
    try:
        data = json.loads(user_input)
    except json.JSONDecodeError:
        data = user_input

    # Serialize data to bytes
    serialized_data = json.dumps(data).encode('utf-8')

    # Generate a #-byte decryption token
    # TODO enter your own #-byte decryption token length value
    decryption_token = get_random_bytes("ENTER YOUR OWN VALUE")

    # Use the first # bytes as the AES key and the next # bytes as the IV
    # TODO enter your own key & iv token values for encryption (ex: key [:32], iv [32:64])
    key = decryption_token[:"ENTER YOUR OWN VALUES"]
    iv = decryption_token["ENTER YOUR OWN VALUES":"ENTER YOUR OWN VALUES"]

    # Encrypt the data using AES in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(serialized_data, AES.block_size))

    # Encode the encrypted data and decryption token to base64 strings
    encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    decryption_token_b64 = base64.b64encode(decryption_token).decode('utf-8')

    # Generate QR codes for the encrypted data and decryption token
    qr_encrypted = qrcode.make(encrypted_data_b64)
    qr_encrypted.save("encrypted_data_qr.png")

    qr_token = qrcode.make(decryption_token_b64)
    qr_token.save("decryption_token_qr.png")

    print("Encrypted data and decryption token have been saved as QR code images.")

if __name__ == "__main__":
    main()
