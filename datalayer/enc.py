import Crypto
from Crypto import Random
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5


# Creating Private Key of 1024 bits and Public Key
# 公钥和私钥
def rsakeys():
    length = 1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()


    decoded_publickey = publickey.export_key().decode('utf-8')
    decoded_privatekey = privatekey.export_key().decode('utf-8')
    publickey = str(decoded_publickey.replace('\\n', '\n'))
    privatekey = str(decoded_privatekey.replace('\\n', '\n'))
    return privatekey, publickey


# 公钥加密
def encrypt(publick_key, text):
    text = bytes(text, encoding='utf-8')

    cipher = PKCS1_OAEP.new(key=publick_key)
    pkcs1_padding_text = cipher.encrypt(text)
    cipher_text = base64.b64encode(pkcs1_padding_text)
    # 返回字符串形式
    # return str(cipher_text, encoding='utf-8')
    return cipher_text


# 私钥解密
def decrypt(private_key, cipher_text):
    # 对密文进行Base64解码

    cipher_text = base64.b64decode(cipher_text)
    # 使用RSA私钥解密
    cipher = PKCS1_OAEP.new(key=private_key)
    decrypted_text = cipher.decrypt(cipher_text)
    return decrypted_text.decode('utf-8')


# # 利用私钥进行数字签名
# #Function sign takes two arguments, private key and data.
# This function returns base64 string of digital signature.
def digital_sign(private_key, data):
    data = bytes(data, encoding='utf-8')
    h = SHA256.new(data)
    signer = pss.new(private_key)
    signature = signer.sign(h)
    return signature


# # 利用公钥验证签名
# #Function verify takes two arguments, public key and digital signature in base64
# and returns a boolean True if signature matches the data, False if not matches data.
def verify_signature(public_key, data, signature):
    data = bytes(data, encoding='utf-8')
    h = SHA256.new(data)
    verifier = pss.new(public_key)
    try:
        verifier.verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False


if __name__ == '__main__':
    # sk,pk = rsakeys()
    # print("public key:", sk)
    # print("private key:", pk)
    # msg = b'this is a test'
    # locked = digital_sign(sk,msg)
    # verify = digital_verify(pk, locked, msg)
    # print("digital signature", locked)
    # # print(type(locked))
    # print("verify the signature:", verify)

    # ---------
    # sk, pk = rsakeys()
    # text = "this is a test"
    # m = "flag{I_Really_Love_You_Very_much_Forver_every!}"

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
    # de = decrypt(sk, text)

    # sk, pk = rsakeys()
    # decoded_publickey = pk.export_key().decode('utf-8')
    # decoded_privatekey = sk.export_key().decode('utf-8')
    # print("public key:")
    # print(str(decoded_publickey.replace('\\n', '\n')))
    # print("-------------------------------")
    # print("private key")
    # print(str(decoded_privatekey.replace('\\n', '\n')))
    print(1)