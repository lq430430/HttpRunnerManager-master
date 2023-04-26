
#生成13位时间戳
def gen_ts():
    return str(round(time.time()*1000)

#sha256Hex加密算法
# def gen_sha256Hex(data):
#     sha256=hashlib.sha256()
#     sha256.update(data.encode('utf-8'))
#     return str(sha256.hexdigest())

#连接字符串
# def signature(phone,password,loginType,deviceId,deviceType,projectKey):
#     ts=gen_ts()
#     combin=str(phone+password+loginType+deviceId+deviceType+ts+projectKey)
#     sha256=hashlib.sha256()
#     gen_sign=str(sha256.update(combin.encode('utf-8')))
#     return gen_sign
# def signature1():
#     return 111




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
