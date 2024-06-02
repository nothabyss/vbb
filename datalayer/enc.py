import Crypto
from Crypto import Random
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5


# Creating Private Key of 1024 bits and Public Key

def rsakeys():
    length = 1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    decoded_publickey = publickey.export_key().decode('utf-8')
    decoded_privatekey = privatekey.export_key().decode('utf-8')
    
    publickey = str(decoded_publickey.replace('\\n', '\n'))
    privatekey = str(decoded_privatekey.replace('\\n', '\n'))   

    return privatekey, publickey


# Public Key Encryption
def encrypt(publick_key, text):
    text = bytes(text, encoding='utf-8')
    key = RSA.import_key(publick_key)
    cipher = PKCS1_OAEP.new(key=key)
    pkcs1_padding_text = cipher.encrypt(text)
    cipher_text = base64.b64encode(pkcs1_padding_text)
    # Returns string format
    # return str(cipher_text, encoding='utf-8')
    return cipher_text


# Private key decryption
def decrypt(private_key, cipher_text):
    # Base64 decode the ciphertext

    pkcs1_padding_text = base64.b64decode(cipher_text)

    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key=key)
    plain_text = cipher.decrypt(pkcs1_padding_text)

    return plain_text.decode('utf-8')


# # Digitally sign with private key
# #Function sign takes two arguments, private key and data.
# This function returns base64 string of digital signature.
def digital_sign(private_key, data):
    # Import the private key string as a key object
    key = RSA.import_key(private_key)

    data = bytes(data, encoding='utf-8')
    h = SHA256.new(data)
    signer = pss.new(key)
    signature = signer.sign(h)

    # Convert the signature result to a base64 encoded string
    signed_data = base64.b64encode(signature)
    
    return signed_data


# # 利用公钥验证签名
# #Function verify takes two arguments, public key and digital signature in base64
# and returns a boolean True if signature matches the data, False if not matches data.
def verify_signature(public_key, data, signature):
    # Import the public key string as a key object
    key = RSA.import_key(public_key)

    data = bytes(data, encoding='utf-8')
    h = SHA256.new(data)
    verifier = pss.new(key)

    # First decode the base64-encoded signature string into bytes
    signature_bytes = base64.b64decode(signature)

    try:
        verifier.verify(h, signature_bytes)
        return True
    except (ValueError, TypeError):
        return False


if __name__ == '__main__':
    # ---------
    # sk, pk = rsakeys()
    # text = "this is a test"
    #
    # en = encrypt(pk, text)
    # de = decrypt(sk, en)
    # ds = digital_sign(sk, text)
    # vs = verify_signature(pk, text, ds)
    # print("we got a public key:", sk)
    # print("we got a private key:", pk)
    # print("cypher_text:", en)
    # print("plain text:", de)
    # print("digital signature", ds)
    # print("verify the signature:", vs)
    

    # sk, pk = rsakeys()
    # decoded_publickey = pk.export_key().decode('utf-8')
    # decoded_privatekey = sk.export_key().decode('utf-8')
    # print("public key:")
    # print(str(decoded_publickey.replace('\\n', '\n')))
    # print("-------------------------------")
    # print("private key")
    # print(str(decoded_privatekey.replace('\\n', '\n')))
    print(1)