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

    # output_string = input_string.replace("\n", "")
    publickey = str(decoded_publickey.replace('\n', ''))
    privatekey = str(decoded_privatekey.replace('\n', ''))

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

def hash_public_key(publick_key,):
    data = bytes(publick_key, encoding='utf-8')
    h = SHA256.new(data)
    hash_value = h.hexdigest()  # 获取十六进制表示的哈希值
    return hash_value



def add_newlines2(text, line_length=64):
    # 在每个line_length的位置插入换行符
    result = ''.join(text[i:i+line_length] + '\n' for i in range(0, len(text), line_length))
    return '\n' + result
def pre_impose_pk(pk):
    pk = "-----BEGIN PUBLIC KEY-----" + add_newlines2(pk) + "-----END PUBLIC KEY-----"
    return pk
def pre_impose_sk(sk):
    sk = "-----BEGIN PRIVATE KEY-----" + add_newlines2(sk) + "-----END PRIVATE KEY-----"
    return sk


if __name__ == '__main__':
    # ---------
    sk, pk = rsakeys()

    # pk = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGS2QVt4rKpnFpm2g69XwaZI2u\nf1RsE8INDccIsqdibHm2Zz7zvfo+rDOgDwSZ89kXxCwJiKvapMJfj6P7/hzvvSF4\nGPjyYOHzcSpgXeyC+tNylSAxKTekCiLbtaZ0Wu9jljwZDdz4B/V/TN8aTRW8LRC9\nkgauakd4LEZkklgAuQIDAQAB\n-----END PUBLIC KEY-----"
    # pk2 = "\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGS2QVt4rKpnFpm2g69XwaZI2u\nf1RsE8INDccIsqdibHm2Zz7zvfo+rDOgDwSZ89kXxCwJiKvapMJfj6P7/hzvvSF4\nGPjyYOHzcSpgXeyC+tNylSAxKTekCiLbtaZ0Wu9jljwZDdz4B/V/TN8aTRW8LRC9\nkgauakd4LEZkklgAuQIDAQAB\n"
    # pk2= str(pk2.replace('\n', ''))
    # pk2 = "-----BEGIN PUBLIC KEY-----" + add_newlines2(pk2) + "-----END PUBLIC KEY-----"
    # # pk = "-----BEGIN PUBLIC KEY-----" + add_newlines2(pk) + "-----END RSA PUBLIC KEY-----"
    # print(repr(pk))
    # print(repr(pk2))
    # print(pk2 == pk)
    print(sk)
    print(pk)

    text = "this is a test"
    print(len("mx6zfk6c++3/dTGNkTJiRTXyj+8/k9kU47Zg2umsySqgVpWAklS1o7l8yQIDAQAB"))
    en = encrypt(pk, text)
    de = decrypt(sk, en)
    ds = digital_sign(sk, text)
    vs = verify_signature(pk, text, ds)
    print("we got a public key:", pk)
    print("we got a private key:", sk)
    print("cypher_text:", en)
    print("plain text:", de)
    print("digital signature", ds)
    print("verify the signature:", vs)
    

    # sk, pk = rsakeys()
    # decoded_publickey = pk.export_key().decode('utf-8')
    # decoded_privatekey = sk.export_key().decode('utf-8')
    # print("public key:")
    # print(str(decoded_publickey.replace('\\n', '\n')))
    # print("-------------------------------")
    # print("private key")
    # print(str(decoded_privatekey.replace('\\n', '\n')))
