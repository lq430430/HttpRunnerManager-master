# debugtalk.py
import random

#生成随机数
def random_str(start,end):
    return str(random.randint(start,end))

#网关
def get_gateway(project,environment):
    switch(project):
        case "bxc40dbm16":
            if("sit".equals(environment)):
                gateway = project+ environment + ".bqtsp.bjev.com.cn"
    print("gateway==" + gateway)
    return gateway
