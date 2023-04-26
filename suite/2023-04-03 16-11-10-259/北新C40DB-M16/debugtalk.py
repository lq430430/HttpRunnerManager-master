# debugtalk.py
import random

#生成随机数
def random_str(start,end):
    return str(random.randint(start,end))

#sha256hex加密
def sha256hex(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    res = sha256.hexdigest()
    print("sha256加密结果:", res)
    return res
    
#生成登录签名
