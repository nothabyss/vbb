import Crypto
from Crypto import Random
import base64
from Crypto.PublicKey import RSA
# from Crypto.Signature.PKCS1_v1_5 import
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP


# Creating Private Key of 1024 bits and Public Key

def rsakeys():
    length = 1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    decoded_publickey = publickey.export_key().decode('utf-8')
    decoded_privatekey = privatekey.export_key().decode('utf-8')

    # output_string = input_string.replace("\n", "")
    # publickey = str(decoded_publickey.replace('\n', ''))
    # privatekey = str(decoded_privatekey.replace('\n', ''))
    publickey = str(decoded_publickey)
    privatekey = str(decoded_privatekey)

    return privatekey, publickey

def rsa_original_keys():
    length = 1024
    privatekey = RSA.generate(length, Random.new().read)
    publickey = privatekey.publickey()
    decoded_publickey = publickey.export_key().decode('utf-8')
    decoded_privatekey = privatekey.export_key().decode('utf-8')

    # output_string = input_string.replace("\n", "")

    return decoded_privatekey, decoded_publickey
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
    private_key = pre_impose_sk(private_key)

    key = RSA.import_key(private_key)

    data = bytes(data, encoding='utf-8')
    h = SHA256.new(data)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)

    # Convert the signature result to a base64 encoded string
    signed_data = base64.b64encode(signature)
    
    return signed_data


# # 利用公钥验证签名
# #Function verify takes two arguments, public key and digital signature in base64
# and returns a boolean True if signature matches the data, False if not matches data.
def verify_signature(public_key, data, signature):
    # Import the public key string as a key object
    public_key = pre_impose_pk(public_key)
    key = RSA.import_key(public_key)

    data = bytes(data, encoding='utf-8')
    h = SHA256.new(data)
    verifier = PKCS1_v1_5.new(key)

    # First decode the base64-encoded signature string into bytes
    signature_bytes = base64.b64decode(signature)

    return verifier.verify(h, signature_bytes)


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
    sk = "-----BEGIN RSA PRIVATE KEY-----" + add_newlines2(sk) + "-----END RSA PRIVATE KEY-----"
    return sk


if __name__ == '__main__':
    # ---------
    # sk, pk = rsakeys()
    # sk = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDanISmp2X1Dwb5CvbXSYtkLkq6MOa/bbPJ9Is7TMRQA+mw0TIGVAieo3V95EezrMcowxpfCaCien7tc4ab3IdIFlx33JPXUvcV1+TpKcS94CDmdkswQHEu5FQX4xRFhYoJOx+IyqKA5uW8fnoVCZF+hcDzUwJsFBe0kFCH7QSZOQIDAQAB'
    # pk = 'MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBANqchKanZfUPBvkK9tdJi2QuSrow5r9ts8n0iztMxFAD6bDRMgZUCJ6jdX3kR7OsxyjDGl8JoKJ6fu1zhpvch0gWXHfck9dS9xXX5OkpxL3gIOZ2SzBAcS7kVBfjFEWFigk7H4jKooDm5bx+ehUJkX6FwPNTAmwUF7SQUIftBJk5AgMBAAECgYEAoRIXjq7iKWgUDCSu8LrIUFznRD5JlZvfjxp2B5AtSINJiLTp9c2uuCvZopMy3UidSQRPhtySFYTJxmyLLoWSygbGq8jYHgflVXI8EUWQdCrvEfrrVkmGtHeUszt+HlarXuL+Raqkgf6R863rg+isYQrsg+D1tq0+urbn3zSjm4ECQQDvOv1hzGkge4gwZLrSKWr3hzrxKp/RoEnRIXITLgCvlUw9NpvzXucSFKcEPJgcHwYj0haVqWjlLKa7zgFd5gvRAkEA6e+EppTmuBu+5e4WJcMhRHBwjM1iwTVvXzTcBo1bKCIEPRKbwLnUSsHVx2+t8ggSwQEZ1qTary8K2j+Y4lRY6QJBANGlCFekIpxspTSDkZSK50p0H5sol1XE+etjO+zC66bzVxRtvszP5f9aSeLUlxhNt7u8aD5Pb7UmJBeAuIHpD4ECQA0gCCREhHFd9Sb3Zby2pv4tBNORjnHiqp3/3Dxt3+hviCdZDO4SPwv2tiTbajoDI/I6OpXlZ/OeQxCdstk3/EkCQQCHP33Cb5A7FLJdt8j5GZzDDC7e5YuMWcg1i4+QQrxtsSrRkTOqHtFsWR8tF2suJS9Ermx1w89DjxqUKU7l4MPe'
    # sk = "MIICXgIBAAKBgQDBjjb9XFms2EShERr+cKyf6Uhp7TPDfUnlX6+F2uOZTcDxNJPx78TQNlWYcImlQyL9iOU+KR1LTERiFXDplyBKlomCeITs1g9ZeD/baWAvMSxK5u1STeli1rK7GvAnXRyCtDP2VtlEn8tnJ2UrnR3BuMLozsy01VPg8FNH/f1OswIDAQABAoGAQEsmvgNSsGUIav49Gr6/wMCjcrg9xRaVmNEvg0Wh67cVu6ms6SUtmcIqrZ/YQSKreU9jYsISfoQfhPs9TgKK0VeQ0n2z8E3/lsTEBCz64dERNvjYocaEdwtyv0naFZeGfcTQeuQK0uJ/7h2jeF1jp6sIbbRAquINdgzHXrsiYRkCQQDNT/X++6RyPDmba4wWjl/GWDI4pmVdeR0FoRSNf5xteXhQUtWHuwXxbg2DQzXyLINt0pn5b0HsaWo8YIWlNVt7AkEA8Vc0qOwar+YMYPNeGXYqFY24haQASa9csilO3bfD5e2p0qVRCmnLihIm9+Ujm7ChM0V8UT3re+gOwdrbk7B4KQJBALC/bJPVSM17IVC2NkRYzwSuepWgUdU1ZZGqCUqDGER6dOQZW2/cxpIAXyuoWbGhNof97MX6TLNcULOnmIYQOC8CQQCc3/qy8wZF4FubiZZZJp4kdILFG920B/FRPdit9o24H8yLyDntcueDUFlUOfXzddTS5w/wHze6yxUMnZ6tWcBBAkEApzoAKhWo+7VSu5lVoYYzBzn0ZuRDk1em6m3ybpoZSUI2GaKqhioKGlO+4i4uB44gSUQSMUI0Iyysfl8qKOTtkw=="
    # pk = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBjjb9XFms2EShERr+cKyf6Uhp7TPDfUnlX6+F2uOZTcDxNJPx78TQNlWYcImlQyL9iOU+KR1LTERiFXDplyBKlomCeITs1g9ZeD/baWAvMSxK5u1STeli1rK7GvAnXRyCtDP2VtlEn8tnJ2UrnR3BuMLozsy01VPg8FNH/f1OswIDAQAB"
    # pk = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGS2QVt4rKpnFpm2g69XwaZI2u\nf1RsE8INDccIsqdibHm2Zz7zvfo+rDOgDwSZ89kXxCwJiKvapMJfj6P7/hzvvSF4\nGPjyYOHzcSpgXeyC+tNylSAxKTekCiLbtaZ0Wu9jljwZDdz4B/V/TN8aTRW8LRC9\nkgauakd4LEZkklgAuQIDAQAB\n-----END PUBLIC KEY-----"
    # pk2 = "\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGS2QVt4rKpnFpm2g69XwaZI2u\nf1RsE8INDccIsqdibHm2Zz7zvfo+rDOgDwSZ89kXxCwJiKvapMJfj6P7/hzvvSF4\nGPjyYOHzcSpgXeyC+tNylSAxKTekCiLbtaZ0Wu9jljwZDdz4B/V/TN8aTRW8LRC9\nkgauakd4LEZkklgAuQIDAQAB\n"
    # pk2= str(pk2.replace('\n', ''))
    # pk2 = "-----BEGIN PUBLIC KEY-----" + add_newlines2(pk2) + "-----END PUBLIC KEY-----"
    # # pk = "-----BEGIN PUBLIC KEY-----" + add_newlines2(pk) + "-----END RSA PUBLIC KEY-----"
    # print(repr(pk))
    # print(repr(pk2))
    # print(pk2 == pk)
    # sk, pk = rsa_original_keys()
    # print(sk)
    # print(pk)
    pk = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDR2JvM5cAzbKF7tCPMnpVLE7RlDEpj2DnJQSc7Xwrysy9V+N/l0jEkqfGwDBcvlkxiGxOtjpp4xgBTjjPGTJngrgAVFuyw8jEpUUdsxYap93ijv1tSrvhjnhW8dqu5n0MC0XrTciE6qzWfdl/ktQHFQd54W7j2x3usZiZufKZwOwIDAQAB'
    Signature = 'XPdlT5AUtjD//jTk160s5TCdt9Q9PAVmEbbOaVO5HWL/C3XDDj9mPjEsb14AxwtTBIKUpZe/Tb8/c0tz6Jb2wYMMA5KrhSdTZ2bYjs96LW+ou8OK+VapL2uXQ1x7o3TbDIshf91DirS7OselKSEYYRkCElnvjIyl29DylM2rHk8='
    text = "123"
    print(len("mx6zfk6c++3/dTGNkTJiRTXyj+8/k9kU47Zg2umsySqgVpWAklS1o7l8yQIDAQAB"))
    # en = encrypt(pk, text)
    # de = decrypt(sk, en)
    # ds = digital_sign(sk, text)
    # pk = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCsOXS0J1vAT5807Uhup809ulJXMYAfQE8OkRen1e6N2WuD+m3V1fn0yE/tSJH4SUqHIQFcG2mR19ds20rjDbYmLnoYnrylxoErKUrlhyTE6Qs/j7yMZaNI99cAYjziF33bj8ktWvQF08+X5iFyUTwNpuBcbwwLX37+pIuSUrQ2ewIDAQAB'
    vs = verify_signature(pk, text, Signature)
    # print("we got a public key:", pk)
    # print("we got a private key:", sk)
    # # print("cypher_text:", en)
    # # print("plain text:", de)
    # print("digital signature", ds)
    print("verify the signature:", vs)
    

    # sk, pk = rsakeys()
    # decoded_publickey = pk.export_key().decode('utf-8')
    # decoded_privatekey = sk.export_key().decode('utf-8')
    # print("public key:")
    # print(str(decoded_publickey.replace('\\n', '\n')))
    # print("-------------------------------")
    # print("private key")
    # print(str(decoded_privatekey.replace('\\n', '\n')))
