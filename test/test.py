D:\anaconda\envs\blockchain\python.exe G:/ablockchain-voting/project/2024.6.8/10.20/vbb/datalayer/enc.py
-----BEGIN RSA PRIVATE KEY-----MIICWwIBAAKBgQCUQt0GYpAd3omj2Gn117cV6SGnH/YVnz8Nplt5ggG6YZUlJ7uPFci/5Ph8iuT+/sV97ayEAFR9hSh+6LDR7KWW/0vG5gVWvZLtfbZYsnoBsdD+NEUY3giEyp59JkHTb3VjBzeRyh1p4BDDIPvi8ey1H1GyRdl/z+NWYMkAHM11TQIDAQABAoGAGGgDY4wxJkGejeLP2qEWqhw1JoJr67ZJ1nDmyRNePnTW7QVj6lOPNwu13iatOM7u6uKHzjkRr5IOjwm2JfCbd4Yl3XkUHPynniZf2evyO+klp7b0jP7U9yn2H7/YnMxNou2gjTnC9eG+8pEEbAVJ+Dp9wTqndnV40C8FZnlaF9ECQQC1sA/rlQHlkW7uHT4nPA7peLIdx1fnW9WTCwWbBG4xo49ivl9rnrP8iHUCsy6woTHbwPMtyjSelNdW53Xs7MoFAkEA0ObQZ7t9yyp9pcXTZbwSPPijHHn7ZiFlPmc1Gn6xtchyw0AYsuT9pvTYjc94zxl61EbljIdiI9uSucgpag84qQJAQZ1X4ohpqvKe0TeWXqz95atFCCQZxuAPfY8ZcyZidWLQQaTm6QLjlWvidhsn3XoZe3dvWzYPUsYGDsiAehP50QJAD9Ha6HAfZ5pRJ5OinaqvauSdXZOzQRm4VBB2ygncJVsHrdeVxz5mIxWZrKuQh4Zzcc3opkq+WN7Q7rbExB5g+QJAfGnZgmep0hgfgd4jSXOFptInuW2yvflHs2lzhPVnQplpSjMIc5kGqN8hfL/EoC6Za/oTu5Ju4GyxF8Ob2xtzGg==-----END RSA PRIVATE KEY-----
-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCUQt0GYpAd3omj2Gn117cV6SGnH/YVnz8Nplt5ggG6YZUlJ7uPFci/5Ph8iuT+/sV97ayEAFR9hSh+6LDR7KWW/0vG5gVWvZLtfbZYsnoBsdD+NEUY3giEyp59JkHTb3VjBzeRyh1p4BDDIPvi8ey1H1GyRdl/z+NWYMkAHM11TQIDAQAB-----END PUBLIC KEY-----
64
Traceback (most recent call last):
  File "G:\ablockchain-voting\project\2024.6.8\10.20\vbb\datalayer\enc.py", line 128, in <module>
    en = encrypt(pk, text)
  File "G:\ablockchain-voting\project\2024.6.8\10.20\vbb\datalayer\enc.py", line 29, in encrypt
    key = RSA.import_key(publick_key)
  File "D:\anaconda\envs\blockchain\lib\site-packages\Crypto\PublicKey\RSA.py", line 832, in import_key
    (der, marker, enc_flag) = PEM.decode(tostr(extern_key), passphrase)
  File "D:\anaconda\envs\blockchain\lib\site-packages\Crypto\IO\PEM.py", line 129, in decode
    raise ValueError("Not a valid PEM pre boundary")
ValueError: Not a valid PEM pre boundary

进程已结束,退出代码1
