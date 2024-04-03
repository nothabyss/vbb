import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import pickle
import pdb
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import hashlib
#Creating Private Key of 1024 bits and Public Key
# 公钥和私钥
def rsakeys():
    length=1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey

# 公钥加密
#function for encryption which takes public key, plain text as arguments. This function returns a base64 encoded string of ciphertext.
def encrypt(rsa_publickey,plain_text):
    cipher_text=rsa_publickey.encrypt(plain_text,32)[0]
    b64cipher=base64.b64encode(cipher_text)
    return b64cipher

# 私钥解密
#For decryption, we create a function that takes ciphertext and private key as arguments.
def decrypt(rsa_privatekey,b64cipher):
    decoded_ciphertext = base64.b64decode(b64cipher)
    plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
    return plaintext

# # 利用私钥进行数字签名
# #Function sign takes two arguments, private key and data. This function returns base64 string of digital signature.
# def sign(privatekey,data):
#     return base64.b64encode(str((privatekey.sign(data,''))[0]).encode())
#
# # 利用公钥验证签名
# #Function verify takes two arguments, public key and digital signature in base64 and returns a boolean True if signature matches the data, False if not matches data.
# def verify(publickey,data,sign):
#     return publickey.verify(data,(int(base64.b64decode(sign)),))
def digital_sign(privatekey, data):
    ha = SHA256.new(data)
    signer = PKCS1_v1_5.new(privatekey)
    signature = signer.sign(ha)
    return signature
def digital_verify(publickey, signature, data):
    ha = SHA256.new(data)
    verifier = PKCS1_v1_5.new(publickey)
    if verifier.verify(ha, signature):
        return True
    else:
        return False


if __name__=='__main__':
    sk,pk = rsakeys()
    msg = b'dafs'
    locked = digital_sign(sk,msg)
    verify = digital_verify(pk, locked, msg)
    print(locked)
    print(type(locked))
    print(verify)
