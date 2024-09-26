import os
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PIL import Image
import pyzbar.pyzbar as pyzbar

def read_qr_code_image(image_path):
    # Open the image and decode the QR code
    img = Image.open(image_path)
    decoded_objects = pyzbar.decode(img)
    if decoded_objects:
        first_object = decoded_objects[0]
        # For debugging
        print("Type of decoded_objects[0]:", type(first_object))
        # Handle different types of decoded_objects[0]
        if hasattr(first_object, 'data'):
            data = first_object.data.decode('utf-8')
        elif isinstance(first_object, bytes):
            data = first_object.decode('utf-8')
        elif isinstance(first_object, str):
            data = first_object
        else:
            raise ValueError("Unexpected type in decoded_objects[0]")
        return data
    else:
        return None

def main():
    # Check if QR code images are available locally
    if os.path.exists("encrypted_data_qr.png") and os.path.exists("decryption_token_qr.png"):
        print("Found QR code images locally.")
        encrypted_data_b64 = read_qr_code_image("encrypted_data_qr.png")
        decryption_token_b64 = read_qr_code_image("decryption_token_qr.png")
    else:
        # Prompt the user to input the base64 strings if QR code images are not found
        print("QR code images not found locally.")
        encrypted_data_b64 = input("Enter the encrypted data (base64): ")
        decryption_token_b64 = input("Enter the decryption token (base64): ")

    # Decode the base64 strings back to bytes
    encrypted_data = base64.b64decode(encrypted_data_b64)
    decryption_token = base64.b64decode(decryption_token_b64)

    # Extract the AES key and IV from the decryption token
    # TODO enter same key & iv values from encryption script
    key = decryption_token[:"ENTER YOUR OWN VALUE"]
    iv = decryption_token["ENTER YOUR OWN VALUE":"ENTER YOUR OWN VALUE"]

    # Decrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(encrypted_data)
    try:
        # Unpad and deserialize the decrypted data
        decrypted_data = unpad(decrypted_padded, AES.block_size)
        data = json.loads(decrypted_data.decode('utf-8'))
        print("Decrypted data:", data)
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        print("Decryption failed:", str(e))

if __name__ == "__main__":
    main()
