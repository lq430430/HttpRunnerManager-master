# debugtalk.py
import random
import time

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

#生成13位时间戳字符
def timestamp_str():
    return str(round(time.time()*1000))
#生成登录签名
def Signature(loginId,password,loginType=None,deviceId=None,deviceType=None，ts==None,projectKey=None):
    combined=loginId + password + loginType+ deviceId+ deviceType+ ts + projectKey;
    signature=sha256hex(combined)
    print(signature)
    return signature
    
def setup_hooks():
    print("setup_hooks")
