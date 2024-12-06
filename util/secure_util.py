from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

class SecureUtil:
    """
    SecureUtil provides utility functions for encoding and decoding data using the DES encryption algorithm.
    
    This class includes methods for encrypting and decrypting strings with a specified key.
    """

    @staticmethod
    def decode(input, key_string):
        """
        Decrypts a base64-encoded string using the DES algorithm.

        Args:
            input (str): The base64-encoded string to be decrypted.
            key_string (str): The key used for decryption. Must be 8 bytes long.

        Returns:
            str: The decrypted plaintext string.

        Raises:
            ValueError: If the input cannot be unpadded or if the key is not valid.
        """
        raw = base64.b64decode(input)
        cipher = DES.new(key_string.encode('utf-8'), DES.MODE_ECB)
        decrypted_bytes = unpad(cipher.decrypt(raw), DES.block_size)
        plain = decrypted_bytes.decode('utf-8')
        return plain
    
    @staticmethod
    def encode(input, key_string):
        """
        Encrypts a string using the DES algorithm and returns a base64-encoded string.

        Args:
            input (str): The plaintext string to be encrypted.
            key_string (str): The key used for encryption. Must be 8 bytes long.

        Returns:
            str: The base64-encoded encrypted string.

        Raises:
            ValueError: If the input cannot be padded or if the key is not valid.
        """
        cipher = DES.new(key_string.encode('utf-8'), DES.MODE_ECB)
        padded_input = pad(input.encode('utf-8'), DES.block_size)
        encrypted_bytes = cipher.encrypt(padded_input)
        str_cipher = base64.b64encode(encrypted_bytes).decode('utf-8')
        return str_cipher
