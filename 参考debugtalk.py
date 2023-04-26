# debugtalk.py
import time
import datetime
import random
import re
import calendar
import base64
import os

#验证生成了打卡记录
def getSignRecord(a,b=[],*c):
    for i in range(0,2):
        b.append(a[i]["staffName"])
    c = list(c)
    #判断打卡记录中是否包含打卡审批通过的数据
    d = [False for k in c if k not in b]
    if d:
        return "0"
    else:
        return "1"

#审批时获取任务taskId
def getTaskId(aname,sname,tid_1,tid_2):
    if aname==sname:
        return tid_1
    else:
        return tid_2

#管理员获取审批任务Id
def getTaskId_admin(taskInstanceVos):
    if len(taskInstanceVos) == 2:
        return taskInstanceVos[1]["taskVos"][0]["id"]
    elif len(taskInstanceVos) == 3:
        return taskInstanceVos[2]["taskVos"][0]["id"]
    else:
        return ""

def getTaskId_admin_1(taskInstanceVos):
    return taskInstanceVos[1]["taskVos"][0]["id"]

def getTaskId_admin_2(taskInstanceVos):
    return taskInstanceVos[2]["taskVos"][0]["id"]

#设定延迟时间
def sleep(t):
    time.sleep(t)

#获取当前时间（utc时间）
def get_current_utcTime():
    utcTime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    utcTime = utcTime[:23] + utcTime[26:]
    return utcTime

#获取后一天的时间（utc时间）
def get_nextDay_utcTime():
    now_time=datetime.datetime.utcnow()
    utcTime = (now_time+datetime.timedelta(days=+1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    utcTime = utcTime[:23] + utcTime[26:]
    return utcTime

#获取后一天时间 年-月-日
def get_day_after_time():
    now_time=datetime.datetime.now()
    return (now_time+datetime.timedelta(days=+1)).strftime("%Y-%m-%d")

#第一次保存表单时按规则随机生成字段id
def setComponentId():
    unixTime = str(round(time.time() * 1000))
    return (''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','0','1','2','3','4','5','6','7','8','9'], 8))+unixTime)

def getHeadersToken(req_headers):
    try:
        # TODO: write code...
        result = re.findall("XSRF-TOKEN=(.{36})", req_headers)[0]
        return result
    except Exception as e:
        print(" 
        raise e

#获取假期模板的ID
def getVocationModelId(data,vname):
    length = len(data)
    for i in range(0,length):
        if data[i]["name"] == vname:
            return data[i]["id"]

#根据name获取processUniqueId
def get_processUniqueId(data,vname):
    length = len(data)
    for i in range(0,length):
        if data[i]["name"] == vname:
            return data[i]["processUniqueId"]

#根据name获取modelShowType
def get_modelShowType(data,vname):
    length = len(data)
    for i in range(0,length):
        if data[i]["name"] == vname:
            return data[i]["modelShowType"]


#获取休假规则中假期的vacationId
def getVacationId(data,vname):
    length = len(data)
    for i in range(0,length):
        if data[i]["leaveName"] == vname:
            return data[i]["id"]


#获取当天日期（年-月-日）
def getCurrentDay():
    return time.strftime('%Y-%m-%d')
    
#获取月份（年-月）
def getMonth():
    return time.strftime('%Y-%m')

#获取当前年份
def getCurrentYear():
    return datetime.datetime.now().year

#获取时间格式format，已遗弃
#def getDateFormat(formDetail):
    #if formDetail[0]["titleI18nKey"] == "ihr360.app.0453":
        #return formDetail[0]["format"]
    #elif formDetail[1]["titleI18nKey"] == "ihr360.app.0453":
        #return formDetail[1]["format"]
    #else:
        #return None

#修改后，兼容新的假期合并套件(version版本为0时，提取format的方法,version版本为1时该方法已废弃)
def getDateFormat(formDetail,dateFormat = ""):
    if dateFormat == "":
        if formDetail[0]["titleI18nKey"] == "ihr360.app.0453":
            return formDetail[0]["format"]
        elif formDetail[1]["titleI18nKey"] == "ihr360.app.0453":
            return formDetail[1]["format"]
    else:
        return dateFormat

# version版本为1时，format直接通过接口获取
        
#将毫秒时间戳转化为年月日时间：
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d", timeArray)

    
#根据时间格式format返回开始时间
#新传入一个dataformart参数，兼容新的假期合并套件
# version版本为0时的getStartTime方法
def getStartTime(formDetail,dateFormat=""):
    format_list = ["YYYY-MM-DD","YYYY-MM-DD HH:mm","YYYY-MM-DD A"]
    #上/下午时的传入时间格式
    if str(getDateFormat(formDetail,dateFormat)) == format_list[2]:
        return time.strftime('%Y-%m-%d %H:%M:%S')
    #年-月-日/年-月-日 时：分的传入格式
    elif str(getDateFormat(formDetail,dateFormat)) == format_list[0]:
        return time.strftime('%Y-%m-%d')
    elif str(getDateFormat(formDetail,dateFormat)) == format_list[1]:
        return time.strftime('%Y-%m-%d') + " 09:00"
    else:
        return None
        
# version版本为1时的getStartTime方法，此时format可以直接拿到，无需去解析获取
def getStartTimeV1(formDetail,dateFormat=""):
    format_list = ["YYYY-MM-DD","YYYY-MM-DD HH:mm","YYYY-MM-DD A"]
    #上/下午时的传入时间格式
    if str(dateFormat) == format_list[2]:
        return time.strftime('%Y-%m-%d %H:%M:%S')
    #年-月-日/年-月-日 时：分的传入格式
    elif str(dateFormat) == format_list[0]:
        return time.strftime('%Y-%m-%d')
    elif str(dateFormat) == format_list[1]:
        return time.strftime('%Y-%m-%d') + " 09:00"
    else:
        return None
        
#根据时间格式format返回开始/结束时间(获取时长接口传参)
def getTimeV1():
    return time.strftime('%Y-%m-%d %H:%M:%S')
    
def getTimeV2():
    return time.strftime('%Y-%m-%d %H:%M')
#根据时间格式format返回2个小时后的时间(获取时长接口传参)
def getTimeV3():
    now = datetime.datetime.now()
    return datetime.datetime(year = now.year, month = now.month, day =now.day,hour=now.hour+2,minute=now.minute).strftime('%Y-%m-%d %H:%M')
    
def getTimeV4():
    now = datetime.datetime.now()
    return datetime.datetime(year = now.year, month = now.month, day =now.day,hour=now.hour+2,minute=now.minute).strftime('%Y-%m-%d %H:%M:%S')
    
def getTimeV5(now_time):
    now = datetime.datetime.now()
    if  now_time=='startTime':
        return datetime.datetime(year = now.year, month = now.month, day =now.day,hour=now.hour,minute=now.minute,second=0).strftime('%Y-%m-%d %H:%M:%S')
    elif now_time=="endTime":
        return datetime.datetime(year = now.year, month = now.month, day =now.day,hour=now.hour+2,minute=now.minute,second=0).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None

#根据时间格式format返回结束时间
#新传入一个dataformart参数，兼容新的假期合并套件
# version版本为0时的getStartTime方法
def getEndTime(formDetail,dateFormat=""):
    format_list = ["YYYY-MM-DD","YYYY-MM-DD HH:mm","YYYY-MM-DD A"]
    #上/下午时的传入时间格式
    if str(getDateFormat(formDetail,dateFormat)) == format_list[2]:
        return time.strftime('%Y-%m-%d %H:%M:%S')
    #年-月-日/年-月-日 时：分的传入格式
    elif str(getDateFormat(formDetail,dateFormat)) == format_list[0]:
        return time.strftime('%Y-%m-%d')
    elif str(getDateFormat(formDetail,dateFormat)) == format_list[1]:
        return time.strftime('%Y-%m-%d') + " 11:00"
    else:
        return None

# version版本为1时的getStartTime方法
def getEndTimeV1(formDetail,dateFormat=""):
    format_list = ["YYYY-MM-DD","YYYY-MM-DD HH:mm","YYYY-MM-DD A"]
    #上/下午时的传入时间格式
    if str(dateFormat) == format_list[2]:
        return time.strftime('%Y-%m-%d %H:%M:%S')
    #年-月-日/年-月-日 时：分的传入格式
    elif str(dateFormat) == format_list[0]:
        return time.strftime('%Y-%m-%d')
    elif str(dateFormat) == format_list[1]:
        return time.strftime('%Y-%m-%d') + " 11:00"
    else:
        return None

#根据时间格式format返回时长
# version版本为0时的
def getTotal(formDetail):
    format_list = ["YYYY-MM-DD","YYYY-MM-DD HH:mm","YYYY-MM-DD A"]
    #上/下午时的传入时间格式
    if str(getDateFormat(formDetail)) == format_list[2]:
        return "4"
    #年-月-日/年-月-日 时：分的传入格式
    elif str(getDateFormat(formDetail)) == format_list[0]:
        return "1"
    elif str(getDateFormat(formDetail)) == format_list[1]:
        return "2"
    else:
        return None
        
# version版本为1时的,好像暂时没用到，先忽略
def getTotalV1(formDetail):
    format_list = ["YYYY-MM-DD","YYYY-MM-DD HH:mm","YYYY-MM-DD A"]
    #上/下午时的传入时间格式
    if str(getDateFormat(formDetail)) == format_list[2]:
        return "4"
    #年-月-日/年-月-日 时：分的传入格式
    elif str(getDateFormat(formDetail)) == format_list[0]:
        return "1"
    elif str(getDateFormat(formDetail)) == format_list[1]:
        return "2"
    else:
        return None

#获取表单中的组件id（单个的假期模板）
def getComponentId(formDetail,cType):
    if formDetail[0]["titleI18nKey"] == "ihr360.app.0453":
        if str(cType) == "start_end_time":
            return formDetail[0]["id"]
        elif str(cType) == "applyReason":
            return formDetail[1]["id"]
        else:
            return None
    elif formDetail[1]["titleI18nKey"] == "ihr360.app.0453":
        if str(cType) == "start_end_time":
            return formDetail[1]["id"]
        elif str(cType) == "applyReason":
            return formDetail[2]["id"]
        else:
            return None
    else:
        return None

#获取新假期合并套件中需要的一些表单数据
def getVacationTypes(data,vacationName):
    d = {}
    for i in range(len(data)):
        if data[i]["dataName"] == vacationName:
            d["dataId"] = data[i]["dataId"]
            d["dataName"] = data[i]["dataName"]
            d["format"] = data[i]["format"]
            d["unit"] = data[i]["unit"]
            return d

#获取表单中的组件id（假期合并套件 请假-调休）
def getComponentIdbyLeaveAdjust(formDetail,cType):
    if str(cType) == "vacationType":
        return formDetail[1]["id"]
    elif str(cType) == "start_end_time":
        return formDetail[2]["id"]
    elif str(cType) == "applyReason":
        return formDetail[3]["id"]
    else:
        return None

def getDateFormatByVacationType(data,vacationName):
    for i in range(len(data)):
        if data[i]["dataName"] == vacationName:
            return data[i]["format"]
            

def getVacationIdByVacationType(data,vacationName):
    for i in range(len(data)):
        if data[i]["dataName"] == vacationName:
            return data[i]["dataId"]

#提供新假期合并套件，发起时formDetail中需要的一些表单数据
def getDataByLeaveAdjust(formDetail,a,cType1,cType2,cType3,totalTime,vacationName,dateFormat):
    componentId1 = str(getComponentIdbyLeaveAdjust(formDetail,cType1))
    componentId2 = str(getComponentIdbyLeaveAdjust(formDetail,cType2))
    componentId3 = str(getComponentIdbyLeaveAdjust(formDetail,cType3))
    data = {}
    data[componentId1] = {}
    data[componentId1]["dataId"] = getVacationTypes(a,vacationName)["dataId"]
    data[componentId1]["dataName"] = getVacationTypes(a,vacationName)["dataName"]
    data[componentId1]["format"] = getVacationTypes(a,vacationName)["format"]
    data[componentId1]["unit"] = getVacationTypes(a,vacationName)["unit"]
    data[componentId2] = {}
    data[componentId2]["startTime"] = getStartTime(formDetail,dateFormat)
    data[componentId2]["endTime"] = getEndTime(formDetail,dateFormat)
    data[componentId2]["total"] = str(totalTime)
    data[componentId2]["format"] = getVacationTypes(a,vacationName)["format"]
    data[componentId3] = "用新的假期合并套件请个假啦！"
    return data

#获取表单实例的data（单个的请假模板，哺乳假除外）
def getData(formDetail,cType1,cType2,totalTime):
    componentId1 = str(getComponentId(formDetail,cType1))
    componentId2 = str(getComponentId(formDetail,cType2))
    data = {}
    data[componentId1] = {}
    data[componentId1]["startTime"] = getStartTime(formDetail)
    data[componentId1]["endTime"] = getEndTime(formDetail)
    data[componentId1]["total"] = str(totalTime)
    data[componentId2] = "111"
    return data

#获取表单实例的data V1版 version版本为1时的（单个的请假模板，哺乳假除外）
# version版本为1时,formInstanceVo的data中需要加入format
def getDataV1(formDetail,cType1,cType2,totalTime,dataFormat,detailId,my_unit):
    componentId1 = str(getComponentId(formDetail,cType1))
    componentId2 = str(getComponentId(formDetail,cType2))
    data = {}
    data[componentId1] = {}
    data[componentId1]["startTime"] = getStartTime(formDetail,dataFormat)
    data[componentId1]["endTime"] = getEndTime(formDetail,dataFormat)
    data[componentId1]["total"] = str(totalTime)
    data[componentId1]["attendanceDetailId"] = detailId
    data[componentId1]["format"] = dataFormat
    data[componentId1]["unit"] = my_unit
    data[componentId2] = "111"
    return data
    
#获取表单实例data（打卡）
def getData_Appeal(formDetail):
    componentId1 = str(formDetail[0]["id"])
    componentId2 = str(formDetail[1]["id"])
    data = {}
    data[componentId1] = time.strftime('%Y-%m-%d') + " 09:00"
    data[componentId2] = "上班未打卡"
    return data
    
    
#获取表单实例的data（哺乳假）
def getData_Lactation(formDetail):
    componentId1 = str(formDetail[0]["id"])
    componentId2 = str(formDetail[1]["id"])
    componentId3 = str(formDetail[2]["id"])
    data = {}
    data[componentId1] = {}
    data[componentId1]["endTime"] = getCurrentDay()
    data[componentId1]["startTime"] = getCurrentDay()
    data[componentId2] = {}
    data[componentId2]["endHm"] = "11:00"
    data[componentId2]["startHm"] = "09:00"
    data[componentId2]["total"] = "2"
    data[componentId3] = "申请哺乳假"
    return data
    
#获取加班表单实例的data
def getData_overtime(formDetail):
    componentId1 = str(formDetail[2]["id"])
    componentId2 = str(formDetail[0]["id"])
    componentId3 = str(formDetail[3]["id"])
    data = {}
    data[componentId1] = {}
    data[componentId1]["startTime"] = time.strftime('%Y-%m-%d') + " 18:00"
    data[componentId1]["endTime"] = time.strftime('%Y-%m-%d') + " 20:00"
    data[componentId1]["total"] = "2"
    data[componentId2] = {}
    data[componentId2]["dataId"] = "NORMAL"
    data[componentId2]["dataName"] = "工作日加班"
    data[componentId2]["enabled"] = True
    data[componentId3] = "我要加班"
    return data
    

#获取批量加班不拆单表单实例的data
def getData_overtime1(formDetail):
    #加班人字段的id
    componentId1 = str(formDetail[0]["id"])
    #加班类型的id
    componentId2 = str(formDetail[1]["id"])
    #开始结束时间字段的id
    componentId3 = str(formDetail[3]["id"])
    #申请事由字段的id
    componentId4= str(formDetail[4]["id"])
    #补偿方式字段的id
    componentId5 = str(formDetail[9]["id"])
    data = {}
    data[componentId1] = [{},{},{}]
    data[componentId1][0]["approverType"] = "STAFF"
    data[componentId1][0]["assignee"] = "61ef9334-e812-47e2-88ed-a1c5cf1e6bd9"
    data[componentId1][0]["assigneeName"] = "C01"
    data[componentId1][0]["dataId"] = "61ef9334-e812-47e2-88ed-a1c5cf1e6bd9"
    data[componentId1][0]["dataName"] = "C01"
    data[componentId1][1]["approverType"] = "STAFF"
    data[componentId1][1]["assignee"] = "c842410f-0342-48cd-b0ac-1ba1a8753ac7"
    data[componentId1][1]["assigneeName"] = "C02"
    data[componentId1][1]["dataId"] = "c842410f-0342-48cd-b0ac-1ba1a8753ac7"
    data[componentId1][1]["dataName"] = "C02"
    data[componentId1][2]["approverType"] = "STAFF"
    data[componentId1][2]["assignee"] = "94d15cbb-1e92-4366-95bb-2a3245cc64a9"
    data[componentId1][2]["assigneeName"] = "C03"
    data[componentId1][2]["dataId"] = "94d15cbb-1e92-4366-95bb-2a3245cc64a9"
    data[componentId1][2]["dataName"] = "C03"
    data[componentId2] = {}
    data[componentId2]["dataId"] = "NORMAL"
    data[componentId2]["dataName"] = "工作日加班"
    data[componentId2]["dataKey"] = "overtime_type.enum.normal"
    data[componentId2]["enabled"] = True
    data[componentId3] = {}
    data[componentId3]["startTime"] = time.strftime('%Y-%m-%d') + " 14:00"
    data[componentId3]["endTime"] = time.strftime('%Y-%m-%d') + " 16:00"
    data[componentId3]["total"] = "2"
    data[componentId4] = "我要加班"
    data[componentId5] = {}
    data[componentId5]["dataId"] = "TRANSFER_TO_REST"
    data[componentId5]["dataName"] = "转调休"
    return data
    
#获取当月第一天
def getMonthFirstDay():
    year = datetime.date.today().year
    month = datetime.date.today().month
    firstDay = datetime.date(year=year, month=month, day=1)
    return firstDay.strftime("%Y-%m-%d")
    
#获取当月最后一天
def getMonthLastDay():
    year = datetime.date.today().year
    month = datetime.date.today().month
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)
    lastDay = datetime.date(year=year, month=month, day=monthRange)
    return lastDay.strftime("%Y-%m-%d")

#获取已休假期报表的已休假期信息
def getVocationInfos_initial(a,vname):
    if str(vname) == "年假":
        return a["hasUseStatutoryAnnualDays"]
    elif str(vname) == "调休":
        return a["adjustResetLeaveHourUsed"]
    elif str(vname) == "事假":
        return a["hasUseAffairLeaveDays"]
    elif str(vname) == "丧假":
        return a["hasUseFuneralDays"]
    elif str(vname) == "哺乳假":
        return a["hasUseLactationHours"]
    elif str(vname) == "婚假":
        return a["hasUseMarriageDays"]
    elif str(vname) == "产假":
        return a["hasUseMaternityLeaveDays"]
    elif str(vname) == "探亲假":
        return a["hasUseHomeDays"]
    elif str(vname) == "陪产假":
        return a["hasUsePaternityDays"]
    elif str(vname) == "产检假":
        return a["hasUsePrenatalCheckUpDays"]
    elif str(vname) == "病假":
        return a["hasUseBuckleSalaryHours"]
    elif str(vname) == "其他假期":
        return a["hasUseOtherDays"]
    elif str(vname) == "自定义假期":
        return a["leaveUserDefinedEntityList"][0]["hasUsedDays"]
    else:
        return None


#验证消耗假期额度
def getVocationInfos_consume(a,b,vname,totalTime):
    a1 = getVocationInfos_initial(a,vname)
    b1 = getVocationInfos_initial(b,vname)
    t = b1 - a1
    if t == totalTime:
        return True
    else:
        return False
        
#验证恢复假期额度    
def getVocationInfos_recover(a,c,vname):
    a1 = getVocationInfos_initial(a,vname)
    c1 = getVocationInfos_initial(c,vname)
    if a1 == c1:
        return True
    else:
        return False

#验证日报中生成单据
def gen_doc(a,vname):
    index = int(datetime.datetime.now().day) - 1
    remark = a[index]["remark"]
    return vname in remark
    
#验证日报中撤销单据
def canc_doc(a):
    index = int(datetime.datetime.now().day) - 1
    remark = a[index]["remark"]
    if remark == "":
        return True
    else:
        return False

#验证审批人为空时的异常提示信息：
def get_abnormalType(a,abnormalType):
    l = len(a) - 1
    if a[l]["taskVos"][0]["description"]["abnormalType"] == str(abnormalType):
        return True
    else:
        return False

#根据分组名和审批模板名获取审批模板id
def getModelId(data,groupName,modelName):
    for i in range(len(data)):
        for j in range(len(data[i]["modelVos"])):
            if data[i]["groupName"] == groupName and data[i]["modelVos"][j]["name"] == modelName:
                return data[i]["modelVos"][j]["id"]

#验证指定分组下的申请入口是否存在
def validate_entry(data,groupName,modelName):
    for i in range(len(data)):
        data1 = data[i]["modelVos"]
        if data[i]["groupName"] == groupName:
            return modelName in data1

#验证异常流程数+1
def plus_1(a,b):
    if a == b-1:
        return True
    else:
        return False

#验证异常流程数-1
def minus_1(a,b):
    if a == b+1:
        return True
    else:
        return False

#获取可作为条件的字段并返回数组
def getConditionComps(ConditionComps):
    a = {}
    for i in range(len(ConditionComps)):
        id = ConditionComps[i]["id"]
        title = ConditionComps[i]["title"]
        a[title] = id
    return a
        
#提供预算流程的data数据
def get_budgetProcess_data(ConditionComps,option1,title1,option2="",title2=""):
    data = {}
    a = getConditionComps(ConditionComps)
    length = len(a)
    if length == 1:
        componentId1 = a[title1]
        data[componentId1] = option1
        return data
    elif length == 2:
        componentId1 = a[title1]
        componentId2 = a[title2]
        data[componentId1] = option1
        data[componentId2] = option2
        return data

#验证审批状态
def verifyStatus(data,id,status):
    for i in range(len(data)):
        if data[i]["id"] == id:
            return data[i]["status"] == status

#返回表单分组内的字段id
def get_item(a,item_title):
    for i in range(len(a)):
        if a[i]["title"] == item_title:
            return a[i]["id"]

def get_item_id(formDetail,title,item_title):
    for i in range(len(formDetail)):
        if formDetail[i]["title"] == title:
            return get_item(formDetail[i]["items"],item_title)

#根据表单字段title返回其id
def get_component_id(formDetail,title):
    for i in range(len(formDetail)):
        if formDetail[i]["title"] == title:
            return formDetail[i]["id"]
            
#提供提交转正的formdatail的data（HR端）
def get_positive_data(formDetail,enrollInDate,positiveDate,probationEndDate,dataId,dataName,enabled,salaryProfileChangeType):
    componentId0 = str(get_component_id(formDetail,"入职日期"))
    componentId1 = str(get_component_id(formDetail,"试用期到期日期"))
    componentId2 = str(get_component_id(formDetail,"转正考核结果"))
    componentId3 = str(get_component_id(formDetail,"转正日期"))
    componentId4 = str(get_component_id(formDetail,"调整转正薪资"))
    componentId5 = str(get_component_id(formDetail,"备注"))
    componentId6 = str(get_item_id(formDetail,"调整转正薪资","薪资生效日期"))
    componentId7 = str(get_item_id(formDetail,"调整转正薪资","调整原因"))
    componentId8 = str(get_item_id(formDetail,"调整转正薪资","基本工资"))
    data = {}
    data[componentId0] = timeStamp(enrollInDate)
    data[componentId1] = timeStamp(probationEndDate)
    data[componentId2] = {}
    data[componentId2]["dataId"] = dataId
    data[componentId2]["dataName"] = dataName
    data[componentId2]["enabled"] = enabled
    data[componentId3] = timeStamp(positiveDate)
    data[componentId4] = True
    data[componentId5] = "该员工表现还OK，允许转正"
    data[componentId6] = timeStamp(probationEndDate)
    data[componentId7] = salaryProfileChangeType
    data[componentId8] = "18888"
    return data

#验证流程预算节点
def verify_process(data,staff1,staff2):
    if data[1]["taskVos"][0]["assigneeName"] == staff1 and data[2]["taskVos"][0]["assigneeName"] == staff2:
        return True
    else:
        return False

#获取转正审批结果列表中的审批状态
def get_status(content,id):
    for i in range(len(content)):
        if content[i]["processId"] == id:
            return content[i]["entryApplicationStatus"]

#获取已转正审批列表中的员工姓名
def verify_positive(content,staffName):
    name_list = []
    for i in range(len(content)):
        name_list.append(content[i]["staffName"])
    if staffName in name_list:
        return True
    else:
        return False

#提供提交转正的formdatail的data（员工端）
def get_positive_data_staff(formDetail,enrollInDate,positiveDate,probationEndDate,dataId,dataName,enabled):
    componentId0 = str(get_component_id(formDetail,"入职日期"))
    componentId1 = str(get_component_id(formDetail,"试用期到期日期"))
    componentId2 = str(get_component_id(formDetail,"转正考核结果"))
    componentId3 = str(get_component_id(formDetail,"转正日期"))
    componentId4 = str(get_component_id(formDetail,"备注"))
    data = {}
    data[componentId0] = timeStamp(enrollInDate)
    data[componentId1] = timeStamp(probationEndDate)
    data[componentId2] = {}
    data[componentId2]["dataId"] = dataId
    data[componentId2]["dataName"] = dataName
    data[componentId2]["enabled"] = enabled
    data[componentId3] = timeStamp(positiveDate)
    data[componentId4] = "该员工表现还OK，允许转正"
    return data

#提供提交离职的formdatail的data
def get_quit_data(formDetail,staffName,staffId):
    componentId0 = str(get_component_id(formDetail,"离职类型"))
    componentId1 = str(get_component_id(formDetail,"离职日期"))
    componentId2 = str(get_component_id(formDetail,"离职原因"))
    componentId3 = str(get_component_id(formDetail,"原因说明"))
    componentId4 = str(get_component_id(formDetail,"最后工作日期"))
    componentId5 = str(get_component_id(formDetail,"薪资结算日期"))
    componentId6 = str(get_item_id(formDetail,"福利缴纳","社保最后缴纳月"))
    componentId7 = str(get_item_id(formDetail,"福利缴纳","公积金最后缴纳月"))
    componentId8 = str(get_item_id(formDetail,"系统调整","部门交接给"))
    componentId8 = str(get_item_id(formDetail,"系统调整","下属交接给"))
    componentId10 = str(get_item_id(formDetail,"系统调整","审批交接给"))
    componentId11 = str(get_component_id(formDetail,"备注"))
    data = {}
    data[componentId0] = {}
    data[componentId0]["dataId"] = "ACTIVE"
    data[componentId0]["dataName"] = "主动离职"
    data[componentId1] = get_day_after_time()
    data[componentId2] = []
    a = {
        "dataId": "PURSUE_NEW_CAREER",
        "dataName": "追求新的职业发展"
    }
    data[componentId2].append(a)
    #data[componentId2]["dataId"] = "PURSUE_NEW_CAREER"
    #data[componentId2]["dataName"] = "追求新的职业发展"
    data[componentId3] = "我是原因说明"
    data[componentId4] = get_day_after_time()
    data[componentId5] = get_day_after_time()
    data[componentId6] = getMonth()
    data[componentId7] = getMonth()
    data[componentId10] = {}
    data[componentId10]["assignee"] = staffId
    data[componentId10]["assigneeName"] = staffName
    data[componentId10]["dataId"] = staffId
    data[componentId10]["dataName"] = staffName
    data[componentId11] = "我是备注"
    return data

#提供发起调动的formdetail的data
def get_transfer_data(formDetail):
    componentId0 = str(get_component_id(formDetail,"调动日期"))
    componentId1 = str(get_component_id(formDetail,"调动类型"))
    componentId4 = str(get_item_id(formDetail,"调动部门","原部门"))
    componentId5 = str(get_item_id(formDetail,"调动部门","调动后部门"))
    componentId6 = str(get_item_id(formDetail,"调动职位","原职位"))
    componentId7 = str(get_item_id(formDetail,"调动职位","调动后职位"))
    componentId8 = str(get_item_id(formDetail,"调动职务","原职务"))
    componentId9 = str(get_item_id(formDetail,"调动职务","调动后职务"))
    componentId10 = str(get_item_id(formDetail,"调动职级","原职级"))
    componentId11 = str(get_item_id(formDetail,"调动职级","调动后职级"))
    componentId12 = str(get_item_id(formDetail,"调动工作地点","原工作地点"))
    componentId13 = str(get_item_id(formDetail,"调动工作地点","调动后工作地点"))
    componentId14 = str(get_item_id(formDetail,"调动合同公司","原合同公司"))
    componentId15 = str(get_item_id(formDetail,"调动合同公司","调动后合同公司"))
    componentId16 = str(get_item_id(formDetail,"调动直属领导","原直属领导"))
    componentId17 = str(get_item_id(formDetail,"调动直属领导","调动后直属领导"))
    componentId18 = str(get_component_id(formDetail,"备注"))
    data = {}
    data[componentId0] = get_day_after_time()
    data[componentId1] = {}
    data[componentId1]["dataId"] = "ADJUST"
    data[componentId1]["dataName"] = "调岗"
    data[componentId4] = "部门10"
    data[componentId5] = {}
    data[componentId5]["afterId"] = "15"
    data[componentId5]["afterName"] = "部门6"
    data[componentId5]["beforeId"] = "19"
    data[componentId5]["beforeName"] = "部门10"
    data[componentId5]["bussinessId"] = None
    data[componentId5]["data"] = {}
    data[componentId5]["data"]["dataId"] = "15"
    data[componentId5]["data"]["dataName"] = "部门6"
    data[componentId5]["dataId"] = "15"
    data[componentId5]["dataName"] = "部门6"
    data[componentId5]["preseted"] = True
    data[componentId5]["transferType"] = "DEPARTMENT"
    
    data[componentId6] =  "高级测试工程师"
    data[componentId7] = {}
    data[componentId7]["afterId"] = "ddca49c1-9d49-4cb6-bded-e7becc58ccc3"
    data[componentId7]["afterName"] = "中级攻城狮"
    data[componentId7]["beforeId"] = "5aea415e-5354-4c7f-98ea-acc8285e1944"
    data[componentId7]["beforeName"] =  "高级测试工程师"
    data[componentId7]["bussinessId"] = None
    data[componentId7]["data"] = {}
    data[componentId7]["data"]["dataId"] = "ddca49c1-9d49-4cb6-bded-e7becc58ccc3"
    data[componentId7]["data"]["dataName"] = "中级攻城狮"
    data[componentId7]["dataId"] = "ddca49c1-9d49-4cb6-bded-e7becc58ccc3"
    data[componentId7]["dataName"] = "中级攻城狮"
    data[componentId7]["preseted"] = True
    data[componentId7]["transferType"] = "POSITION"
    
    data[componentId8] = "高级测试工程师"
    data[componentId9] = {}
    data[componentId9]["afterId"] = "84ba7490-db60-4d8a-af0b-35b9c5874f5a"
    data[componentId9]["afterName"] = "中级工程师"
    data[componentId9]["beforeId"] = "5aea415e-5354-4c7f-98ea-acc8285e1944"
    data[componentId9]["beforeName"] = "高级测试工程师"
    data[componentId9]["bussinessId"] = None
    data[componentId9]["data"] = {}
    data[componentId9]["data"]["dataId"] = "84ba7490-db60-4d8a-af0b-35b9c5874f5a"
    data[componentId9]["data"]["dataName"] = "中级工程师"
    data[componentId9]["dataId"] = "84ba7490-db60-4d8a-af0b-35b9c5874f5a"
    data[componentId9]["dataName"] = "中级工程师"
    data[componentId9]["preseted"] = True
    data[componentId9]["transferType"] = "JOBTITLE"
    
    data[componentId10] = "p3"
    data[componentId11] = {}
    data[componentId11]["afterId"] = "fc0ff82e-8cce-4be0-b693-6685ba81a3ce"
    data[componentId11]["afterName"] = "p2"
    data[componentId11]["beforeId"] = "bcbede73-8647-4b49-bfa2-3f9e8dca0e9b"
    data[componentId11]["beforeName"] = "p3"
    data[componentId11]["bussinessId"] = None
    data[componentId11]["data"] = {}
    data[componentId11]["data"]["dataId"] = "fc0ff82e-8cce-4be0-b693-6685ba81a3ce"
    data[componentId11]["data"]["dataName"] = "p2"
    data[componentId11]["dataId"] = "fc0ff82e-8cce-4be0-b693-6685ba81a3ce"
    data[componentId11]["dataName"] = "p2"
    data[componentId11]["preseted"] = True
    data[componentId11]["transferType"] = "POSITIONGRADE"
    
    return data

#返回数字长度
def get_length(data):
    return len(data)
 
#验证休假单状态
def vft_sta(a,status):
    if str(a) == status:
        return True
    else:
        return False
#test11
def aa(a,b):
    d = [False for c in b if c not in a]
    if d:
        return "0"
    else:
        return "1"

def getItem(data):
    a = []
    for i in range(len(data)):
        if "assigneeName" in data[i]:
            a.append(data[i]["assigneeName"])
        else:
            a.append("empty")
    return a


#验证预算节点正确
def verifyTaskVos(taskVos_1,taskVos_2,assignees1,assignees2):
    return getItem(taskVos_1) == assignees1.split(',') and getItem(taskVos_2) == assignees2.split(',')

#返回表单字段的字段名和id的键值对
def getCompsNameAndId(formDetail):
    a = {}
    for i in range(len(formDetail)):
        a[formDetail[i]["title"]] = formDetail[i]["id"]
    return a
# bug64182表单数据准备
def getFormDataByBug64182(formDetail, cname, option,req_headers):
    brand = get_brand_gray(req_headers)
    a = getCompsNameAndId(formDetail)
    data = {}
    # prod的data数据
    data_prod = {}
    data_prod[a[cname[0]]] = {
        "dataId": "4625f237-09bc-4471-8188-4494dbf8ea88",
        "dataName": "C124",
        "assigneeName": "C124",
        "assignee": "4625f237-09bc-4471-8188-4494dbf8ea88"
    }
    data_prod[a[cname[1]]] = [
        {
            "dataId": "0c1d8b6a-0a54-48d1-ae23-be8bfe61f955",
            "dataName": "C123",
            "approverType": "STAFF",
            "assigneeName": "C123",
            "assignee": "0c1d8b6a-0a54-48d1-ae23-be8bfe61f955"
        },
        {
            "dataId": "4625f237-09bc-4471-8188-4494dbf8ea88",
            "dataName": "C124",
            "approverType": "STAFF",
            "assigneeName": "C124",
            "assignee": "4625f237-09bc-4471-8188-4494dbf8ea88"
        }
    ]
    data_prod[a[cname[2]]] = {
        "dataId": "90",
        "dataName": "垃圾站24"
    }
    data_prod[a[cname[3]]] = [
        {
            "dataId": "90",
            "dataName": "垃圾站24"
        },
        {
            "dataId": "87",
            "dataName": "垃圾站23"
        }
    ]
    if option == "员工（单个）":
        data_prod[a[cname[4]]] = {
            "dataName": "员工（单个）",
            "dataId": "员工（单个）",
            "dataKey": None
        }
    else:
        data_prod[a[cname[4]]] = {
            "dataName": "员工（多个）",
            "dataId": "员工（多个）",
            "dataKey": None
        }
    # uatregion的data数据
    data_uat = {}
    data_uat[a[cname[0]]] = {
        "dataId": "ee9185dc-5c07-49e4-bf6a-fddbc5125327",
        "dataName": "C124",
        "assigneeName": "C124",
        "assignee": "ee9185dc-5c07-49e4-bf6a-fddbc5125327"
    }
    data_uat[a[cname[1]]] = [
        {
            "dataId": "f5a68c05-f258-4815-8863-6aeb05e5f056",
            "dataName": "C123",
            "approverType": "STAFF",
            "assigneeName": "C123",
            "assignee": "f5a68c05-f258-4815-8863-6aeb05e5f056"
        },
        {
            "dataId": "ee9185dc-5c07-49e4-bf6a-fddbc5125327",
            "dataName": "C124",
            "approverType": "STAFF",
            "assigneeName": "C124",
            "assignee": "ee9185dc-5c07-49e4-bf6a-fddbc5125327"
        }
    ]
    data_uat[a[cname[2]]] = {
        "dataId": "43",
        "dataName": "垃圾站24"
    }
    data_uat[a[cname[3]]] = [
        {
            "dataId": "43",
            "dataName": "垃圾站24"
        },
        {
            "dataId": "42",
            "dataName": "垃圾站23"
        }
    ]
    if option == "员工（单个）":
        data_uat[a[cname[4]]] = {
            "dataName": "员工（单个）",
            "dataId": "员工（单个）",
            "dataKey": None
        }
    else:
        data_uat[a[cname[4]]] = {
            "dataName": "员工（多个）",
            "dataId": "员工（多个）",
            "dataKey": None
        }
    
    # qa2的data数据
    
    if brand == 'prod':
        data = data_prod
    elif brand == 'uatstable':
        data = data_uat
    else:
        data = "The data is empty! Please check your code!"

    return data

def string2list(a):
    return a.split(",")

#取出第n个审批节点中的审批人
def getApproval(budgetData,num):
    taskVos = budgetData[num]["taskVos"]
    assignee = []
    for i in range(len(taskVos)):
        assignee.append(taskVos[i]["assigneeName"])
    return sorted(assignee)


#验证审批节点中的审批人正确
def verifyApproval(budgetData,num,approval):
    a = getApproval(budgetData,num)
    if "," not in approval:
        print(a[0])
        return approval == a[0]
    else:
        b = string2list(approval)
        print(a,b)
        return a == b
def getHeadersToken(req_headers):
    """
    获取请求头部中token  :param req_headers_cookie: 请求头部中cookie字符 :return: 请求头中cookie中 XSRF-TOKEN的值
    """
    return re.findall("XSRF-TOKEN=(.{36})", req_headers)[0]


def get_base64(appID, appSecret):
    '''
    获取 openapi 中请求头Authorization：appID:appSecret的base64编码
    '''
    return base64.b64encode((appID + ":" + appSecret).encode("utf-8")).decode('utf-8')

#验证加班单状态和审批单状态对应
def validate_overtime_status(status,data):
    if status == "PASS":
        if data == "NOT_EFFECTIVE" or data == "IN_FORCE" or data == "USED":
            return True
        else:
            return False
    elif status == "INITIATE":
        if data == "APPROVING":
            return True
        else:
            return False
    elif status == "CANCEL":
        if data == "INVALID":
            return True
        else:
            return False
    else:
        return False

#验证发起人可编辑权限返回的字段正确
def validate_editForm(item,length):
    if len(item) == length:
        return True
    else:
        return False

#验证我审批插件的待办和申请数量
def validate_num(a1,a2,b1,b2,flag):
    if flag == "add":
        return int(a2)-int(a1)==1&int(b2)-int(b1)==1
    elif flag == "sub":
        return int(a2)-int(a1)==-1&int(b2)-int(b1)==-1
    else:
        return "error args"
#验证message信息
def validate_err(err, data):
    return str(err[0]) in str(data[0])

#验证B端人事类、加班等发起时拉取的入口
def validate_entrance(num, list1,data):
    if len(data) == num:
        return data[0]["name"] in list1 and data[-1]["name"] in list1
    else:
        return False

#获取请求头部中cookie中的brand_gray,存到环境变量
def get_brand_gray(req_headers):
    return re.findall("brand_gray=(.{3,10});", req_headers)[0]

# 用于生成计算时长接口中传的datailId
def generate_random_str():
    random_str1 =''
    random_str2 =''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZ0123456789'
    length = len(base_str)-1
    for i in range(22):
        random_str1 += base_str[random.randint(0,len(base_str)-1)]
    for j in range(13):
        random_str2 += base_str[random.randint(26,len(base_str)-1)]
    return random_str1 + '-'+random_str2

# 依次审批节点空节点，发起时需要赛值进去，从前一个预算接口拿下这个值
def get_approverOptionalVos(data):
    approverOptionalVos = [{},{},{}]
    approverOptionalVos[0]["taskDefinitionKey"] = data[0]["taskDefinitionKey"]
    approverOptionalVos[0]["dataId"] = data[0]["dataId"]
    approverOptionalVos[1]["taskDefinitionKey"] = data[1]["taskDefinitionKey"]
    approverOptionalVos[1]["dataId"] = data[1]["dataId"]
    approverOptionalVos[2]["taskDefinitionKey"] = data[2]["taskDefinitionKey"]
    approverOptionalVos[2]["dataId"] = data[2]["dataId"]
    return approverOptionalVos

#准备加签接口中的staff数据
def get_signature_data(req_headers):
    brand = get_brand_gray(req_headers)
    data = []
    data_uat = [{
            "assigneeName": "C06",
            "dataName": "C06",
            "dataId": "c26e37c8-c35d-409e-954d-c1955ff585df",
            "approverType": "STAFF",
            "assignee": "c26e37c8-c35d-409e-954d-c1955ff585df"
        }]
    data_prod = [{
            "assigneeName": "C06",
            "dataName": "C06",
            "dataId": "b7156fb5-8cf8-4352-a20e-43778dc1e242",
            "approverType": "STAFF",
            "assignee": "b7156fb5-8cf8-4352-a20e-43778dc1e242"
        }]
        
    if brand == 'prod':
        data = data_prod
    elif brand == 'uatstable':
        data = data_uat
    else:
        data = ["The data is empty! Please check your code!"]

    return data

#验证前往编辑页面、修改页面是否保留评论节点
def verifyComment(asyncResult):
    str = ""
    for i in range(len(asyncResult)):
        if asyncResult[i]["name"] == "评论":
            str = "前往编辑保留评论节点"
            break
        else:
            str = "修改不保留评论节点"
    return str
    
#获取已撤回状态第一条流程id
def getApplicationProcessId(applyList,statusName,settingName):
    processId = []
    for i in range(len(applyList)):
        if applyList[i]["status"] == statusName and applyList[i]["approvalSettingName"] == settingName:
            processId.append(applyList[i]["id"])
            break
    return processId[0]
    
#获取指定待我审批的单据taskId
def getWaitTaskId(waitApproveList,processId):
    for i in range(len(waitApproveList)):
        if waitApproveList[i]["id"] == processId:
            return waitApproveList[i]["ruTask"]["id"]


