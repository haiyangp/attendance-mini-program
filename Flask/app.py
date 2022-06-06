# from flask import Flask,request
# import pymysql

# #导入数据库操作类

import datetime
from itertools import count
from math import fabs
from operator import index
from utils import face_Recgnition

import random
from traceback import print_tb

from sql_connect import Mysql
# from img_save import imgStream


import json
from sre_constants import SUCCESS
from flask import Flask,request,Response, jsonify,url_for
import requests
import os

AppID="wx5aa29e2724377c67"
AppSecret="1383e85972c63b51c4e4956d5b31b45d"

app = Flask(__name__)

# 状态码
# 200 成功 
# 210 老师创建课程失败
# 220 学生加入课程失败
# 230 加入不存在课程
# 240 注册失败
# 250 教师登录失败
# 260 学生登录失败
# 270 当前课程不在签到状态
# 280 座位已被选择
# 290 修改照片失败
# 300 签到失败

# 获取openid
def getOpenid(code):
    response = requests.get("https://api.weixin.qq.com/sns/jscode2session?appid="+AppID+"&secret="+AppSecret+"&js_code="+code+"&grant_type=authorization_code")
    res=json.loads(response.text)
    # print(res)
    open_id=res["openid"]

    return open_id

# 获取一节课的全部信息
def getCourseInfo(db,course):
    cou_id=course[0]
    cou_name=course[1]
    tea_id=course[2]

    res={}
    # 是否正在签到
    res["signing"]=db.findSigning2(data=cou_id,index="cou_id")
    # 班级人数
    res["studentsNumber"]=db.getStudentsNum(cou_id)[0][0]
    # 老师姓名
    res["teacherName"]=db.findTeacher(data=tea_id,index="tea_id")[0][1]
    # 签到次数
    res["signTimes"]=db.getSignTimes(cou_id)

    return res

@app.route('/login', methods=['GET', 'POST'])
def login():



    # 获取请求信息
    code=request.get_json()["code"]
    ifTeacher=request.get_json()["ifTeacher"]

    # 获取open_id
    open_id=getOpenid(code)

    # 数据库对象
    db=Mysql()

    # return open_id, 260, {"Content-Type": "application/json"}

    if ifTeacher:
        results_t=db.findTeacher(data=open_id,index="tea_wxid")

        if results_t:

            return jsonify(results_t)
        else:
            # 不存在返回不存在信息
            return "教师登录失败", 250, {"Content-Type": "application/json"}

    else:
        results_s=db.findStudent(data=open_id,index="stu_wxid")

        if results_s:

            return jsonify(results_s)
        else:
            # 不存在返回不存在信息
            return open_id, 260, {"Content-Type": "application/json"}


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 获取请求信息    
    stu_name=request.values.get("name")
    stu_id=request.values.get("xuehao")
    stu_wxid=request.values.get("openid")

    data={"stu_id":stu_id,"stu_name":stu_name,"stu_wxid":stu_wxid}

    db=Mysql()

    # 是否插入学生成功
    ifSucess=db.insertStudent(data=data)

    
    if ifSucess:
        file_name=stu_name+'_'+stu_id+".jpg"
        request.files.to_dict()["editormd-image-file"].save('./imgs/'+file_name)
        
        results_s = db.findStudent(data=stu_wxid,index="stu_wxid")

        return jsonify(results_s)

    else :
        return "注册失败，该学号已存在", 240, {"Content-Type": "application/json"}

@app.route('/course_get', methods=['GET', 'POST'])
def getCourse():
    id=request.get_json()["id"]
    ifTeacher=request.get_json()["ifTeacher"]

    db=Mysql()

    data_res=[]

    if ifTeacher:
        # 查找课程
        results_c=db.findCourse(data=id,index="tea_id")

        if results_c:
            # 查找每节课的详细信息。
            for course in results_c:
                data_course=[]

                # 课程详细信息
                course_detail=getCourseInfo(db,course)

                for course_item in course:
                    data_course.append(course_item)
                data_course.append(course_detail)

                data_res.append(data_course)

        return jsonify(data_res)


    else:
        results=db.findStudent_Course(data=id,index="stu_id")



        if results:

            for student_course in results:
                data_course=[]

                course=db.findCourse(data=student_course[2],index="cou_id")[0]

                course_detail=getCourseInfo(db,course)
                
                for course_item in course:
                    data_course.append(course_item)
                data_course.append(course_detail)

                data_res.append(data_course)

        return jsonify(data_res)


@app.route('/course_delete', methods=['GET', 'POST'])
def deleteCourse():
    id=request.get_json()["id"]
    ifTeacher=request.get_json()["ifTeacher"]
    cou_id=request.get_json()["cou_id"]

    db=Mysql()

    if ifTeacher:
        db.deleteStudent_Course(data=cou_id,index="cou_id")
        db.deleteCourse(data=cou_id,index="cou_id")
    else:
        db.deleteStudent_Course(data=cou_id,index="cou_id")

    return "删除完成", 200, {"Content-Type": "application/json"}

@app.route('/course_add', methods=['GET', 'POST'])
def addCourse():
    id=request.get_json()["id"]
    ifTeacher=request.get_json()["ifTeacher"]
    cou_id=request.get_json()["cou_id"]
    cou_name=""

    db=Mysql()

    data={}
    data["cou_id"]=cou_id
    

    data
    if ifTeacher:
        cou_name=request.get_json()["cou_name"]
        data["tea_id"]=id
        data["cou_name"]=cou_name

        result=db.insertCourse(data)

        if result:
            return "创建课程成功", 200, {"Content-Type": "application/json"}
        else:
            return "该课程号已被使用", 210, {"Content-Type": "application/json"}

    else:
        data["stu_id"]=id
        data["sc_id"]=cou_id+id+str(random.randint(1,10))

        result=db.insertStudent_Course(data)
        if result==0:
            return "加入课程成功", 200, {"Content-Type": "application/json"}
        elif result==1:
            return "重复加入课程", 220, {"Content-Type": "application/json"}
        elif result==2:
            return "未找到该课程", 230, {"Content-Type": "application/json"}


@app.route('/sign_start', methods=['GET', 'POST'])
def startSign():
    cou_id=request.get_json()["cou_id"]
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sgn_id=cou_id+str(datetime.datetime.now())
    room_type=json.dumps(request.get_json()["roomtype"])
    latitude=request.get_json()["latitude"]
    longitude=request.get_json()["longitude"]

    data={"sgn_id":sgn_id,"sgn_time":time,"sgn_roomtype":room_type,"sgn_state":1,"cou_id":cou_id,"latitude":latitude,"longitude":longitude}

    db=Mysql()

    result=db.insertSign(data)


    return result, 200, {"Content-Type": "application/json"}

@app.route('/sign_stop', methods=['GET', 'POST'])
def stopSign():
    sgn_id=request.get_json()["sgn_id"]

    db=Mysql()
    db.updateSign(sgn_id)

    return "结束签到成功", 200, {"Content-Type": "application/json"}

@app.route('/sign_get', methods=['GET', 'POST'])
def getSign():
    cou_id=request.get_json()["cou_id"]


    db=Mysql()
    result=db.findSigning(data=cou_id,index="cou_id")

    return jsonify(result[0]), 200, {"Content-Type": "application/json"}




@app.route('/sign_send', methods=['GET', 'POST'])
def sendSign():
    sgn_id=request.values.get("sgn_id")
    seat_x=request.values.get("seat_x")
    seat_y=request.values.get("seat_y")

    seat=json.dumps([int(seat_x),int(seat_y)])
    stu_id=request.values.get("stu_id")
    ss_id=stu_id+sgn_id+str(random.randint(1,10))
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file=request.files.to_dict()["editormd-image-file"]

    data={"ss_id":ss_id,"stu_id":stu_id,"sgn_id":sgn_id,"seat":seat,"time":time}

    db=Mysql()

    result=db.findSigning(data=sgn_id,index="sgn_id")
    if not result:
        return "课程不在签到状态", 270, {"Content-Type": "application/json"} 



    result=db.findByStrData(table="students_signs",data=sgn_id,index="sgn_id")

    for sign_student in result:
        if sign_student[3]==seat:
            return "座位已被选择", 280, {"Content-Type": "application/json"} 
    # 签到校验
    if face_Recognition(file):
        db.insertStudent_Sign(data)
        return "签到成功", 200, {"Content-Type": "application/json"} 
    else:
        return "签到失败", 300, {"Content-Type": "application/json"} 
    
@app.route('/excep_send', methods=['GET','POST'])
def sendExcpt():
    excp_describe=request.get_json()["excp_describe"]
    stu_id=request.get_json()["stu_id"]
    sgn_id=request.get_json()["sgn_id"]
    excp_id=stu_id+sgn_id+str(random.randint(1,10))

    db=Mysql()
    data={"excp_describe":excp_describe,"stu_id":stu_id,"sgn_id":sgn_id,"excp_state":1,"excp_id":excp_id}


    db.insertException(data)

    return "发送成功",200,{"Content-Type":"application/json"}

@app.route('/sign_result', methods=['GET','POST'])
def getSignResult():
    sgn_id=request.get_json()["sgn_id"]

    db=Mysql()
    result=db.findByStrData(table="students_signs",data=sgn_id,index="sgn_id")

    data_res=[]
    for student_sign in result:
        data_sign=[]
        cou_id=student_sign[1]

        result_s=db.findStudent(cou_id)[0]

        data_sign.append(student_sign[3])
        data_sign.append(result_s[0])
        data_sign.append(result_s[1])

        data_res.append(data_sign)



    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/expt_get', methods=['GET','POST'])
def getExcpt():
    sgn_id=request.get_json()["sgn_id"]

    db=Mysql()
    result=db.findByStrData(table="exceptions",data=sgn_id,index="sgn_id")

    return jsonify(len(result)),200,{"Content-Type":"application/json"}

@app.route('/expt_get2', methods=['GET','POST'])
def getExcpt2():
    tea_id=request.get_json()["tea_id"]

    db=Mysql()

    data_res=[]

    courses=db.findCourse(data=tea_id,index="tea_id")
    for course in courses:
        cou_id=course[0]

        signs=db.findSign(data=cou_id,index="cou_id")
        for sign in signs:
            sgn_id=sign[0]

            exceptions=db.findByStrData(table="exceptions",data=sgn_id,index="sgn_id")
            for exception in exceptions:
                if exception[2]==1:
                    data_exception={}
                    data_exception["stu_id"]=exception[3]
                    data_exception["stu_name"]=db.findStudent(exception[3])[0][1]

                    data_exception["sgn_index"]=sign[3]
                    data_exception["excp_id"]=exception[0]
                    data_exception["excp_describe"]=exception[1]
                    data_exception["cou_id"]=cou_id
                    data_exception["cou_name"]=course[1]
                    data_res.append(data_exception)

    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/expt_excute', methods=['GET','POST'])
def executeExcpt():
    excp_id=request.get_json()["excp_id"]

    db=Mysql()
    db.alterException(excp_id)

    return "处理成功",200,{"Content-Type":"application/json"}    


@app.route('/sign_record', methods=['GET','POST'])
def getSignRecords():
    cou_id=request.get_json()["cou_id"]

    db=Mysql()
    result_s=db.findSign(data=cou_id,index="cou_id")

    data_res=[]
    for sign in result_s:
        data_sgin=[]
        data_sgin.append(str(sign[1]))
        data_sgin.append(sign[4])
        data_sgin.append(db.getStudentsNumInSign(sign[0])[0][0])

        data_res.append(data_sgin)

    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/sign_record_s', methods=['GET','POST'])
def getSignRecords_s():
    cou_id=request.get_json()["cou_id"]
    stu_id=request.get_json()["stu_id"]

    db=Mysql()
    result_s=db.findSign(data=cou_id,index="cou_id")

    data_res=[]
    for sign in result_s:
        if sign[4]==0:
            data_sign={}
            data_sign["sign_start_time"]=str(sign[1])

            sgn_id=sign[0]
            student_sign=db.findByStrData(table="students_signs",data=sgn_id,index="sgn_id")

            if student_sign:
                data_sign["sign_state"]=True
                data_sign["seat"]=student_sign[0][3]
                data_sign["sign_end_time"]=str(student_sign[0][4])
            else:
                data_sign["sign_state"]=False
            data_res.append(data_sign)

    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/sign_record_ss', methods=['GET','POST'])
def getSignRecords_ss():
    
    stu_id=request.get_json()["stu_id"]
    db=Mysql()
    data_res=[]

    students_signs=db.findByStrData(table="students_signs",data=stu_id,index="stu_id")
    for ss in students_signs:
        data_sign={}
        data_sign["seat"]=ss[3]
        data_sign["time"]=str(ss[4])

        sgn_id=ss[2]
        sign=db.findSign(data=sgn_id,index="sgn_id")[0]
        cou_id=sign[5]
        data_sign["sgn_index"]=sign[3]
        course=db.findCourse(data=cou_id,index="cou_id")[0]
        data_sign["cou_id"]=cou_id
        data_sign["cou_name"]=course[1]

        data_res.append(data_sign)

    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/cmpl_add', methods=['GET','POST'])
def addComplement():

    cou_id=request.get_json()["cou_id"]
    stu_id=request.get_json()["stu_id"]
    stu_name=request.get_json()["stu_name"]
    sign_index=int(request.get_json()["sign_index"])
    

    data={}
    data["bsgn_reason"]=""
    data["bsgn_state"]=0
    data["stu_id"]=stu_id
    data["bsgn_time"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["time"]=data["bsgn_time"]
    data["seat"]=""
    data["cou_id"]=cou_id

    db=Mysql()
    signs=db.findSign(data=cou_id,index="cou_id")
    for sign in signs:
        if sign[3]==sign_index:
            sgn_id=sign[0]
            bsgn_id=sgn_id+str(random.randint(1,20))
            data["sgn_id"]=sgn_id
            data["bsgn_id"]=bsgn_id
            data["ss_id"]=bsgn_id+str(random.randint(1,20))
            break

    db.insertComplement(data)
    db.insertStudent_Sign(data)

    return "补签成功",200,{"Content-Type":"application/json"}

@app.route('/cmpl_send', methods=['GET','POST'])
def addComplement2():

    cou_id=request.get_json()["cou_id"]
    stu_id=request.get_json()["stu_id"]
    sign_index=int(request.get_json()["sign_index"])
    bsgn_reason=request.get_json()["bsgn_reason"]

    data={}
    data["bsgn_reason"]=bsgn_reason
    data["bsgn_state"]=1
    data["stu_id"]=stu_id
    data["bsgn_time"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    db=Mysql()
    signs=db.findSign(data=cou_id,index="cou_id")
    for sign in signs:
        if sign[3]==sign_index:
            sgn_id=sign[0]
            bsgn_id=sgn_id+str(random.randint(1,20))
            data["sgn_id"]=sgn_id
            data["bsgn_id"]=bsgn_id

            break

    db.insertComplement(data)

    return "申请成功",200,{"Content-Type":"application/json"}

@app.route('/cmpl_excute', methods=['GET','POST'])
def excuteComplement():
    cou_id=request.get_json()["cou_id"]

    db=Mysql()

    data_res=[]
    signs=db.findSign(data=cou_id,index="cou_id")
    for sign in signs:
        sgn_id=sign[0]

        complements=db.findByStrData(table="complements",data=sgn_id,index="sgn_id")
        for complement in complements:
            if complement[2]==1:
                data_complement={}
                data_complement["stu_id"]=complement[3]
                data_complement["stu_name"]=db.findStudent(complement[3])[0][1]
                data_complement["bsgn_time"]=str(complement[5])
                data_complement["sgn_index"]=sign[3]
                data_complement["bsgn_id"]=complement[0]
                data_complement["bsgn_reason"]=complement[1]
                data_res.append(data_complement)

    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/cmpl_excute2', methods=['GET','POST'])
def excuteComplement2():
    ifRefuse=request.get_json()["ifRefuse"]
    bsgn_id=request.get_json()["bsgn_id"]

    db=Mysql()


    if not ifRefuse:
        db.alterComplement(bsgn_id,0)
        complement=db.findByStrData(table="complements",data=bsgn_id,index="bsgn_id")[0]
        data={}
        sgn_id=complement[4]
        stu_id=complement[3]
        data["ss_id"]=bsgn_id+str(random.randint(1,20))
        data["stu_id"]=stu_id
        data["sgn_id"]=sgn_id
        data["seat"]=""
        data["time"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.insertStudent_Sign(data)
    else:
        db.alterComplement(bsgn_id,2)

    return "处理成功",200,{"Content-Type":"application/json"}

@app.route('/cmpl_excute3', methods=['GET','POST'])
def excuteComplement3():
    tea_id=request.get_json()["tea_id"]

    db=Mysql()

    data_res=[]

    courses=db.findCourse(data=tea_id,index="tea_id")
    for course in courses:
        cou_id=course[0]

        
        signs=db.findSign(data=cou_id,index="cou_id")
        for sign in signs:
            sgn_id=sign[0]

            complements=db.findByStrData(table="complements",data=sgn_id,index="sgn_id")
            for complement in complements:
                if complement[2]==1:
                    data_complement={}
                    data_complement["stu_id"]=complement[3]
                    data_complement["stu_name"]=db.findStudent(complement[3])[0][1]
                    data_complement["bsgn_time"]=str(complement[5])
                    data_complement["sgn_index"]=sign[3]
                    data_complement["bsgn_id"]=complement[0]
                    data_complement["bsgn_reason"]=complement[1]
                    data_complement["cou_id"]=cou_id
                    data_complement["cou_name"]=course[1]
                    data_res.append(data_complement)

    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/cmpl_get1', methods=['GET','POST'])
def getComplement1():
    cou_id=request.get_json()["cou_id"]
    stu_id=request.get_json()["stu_id"]

    db=Mysql()

    complements=db.findByStrData(table="complements",data=stu_id,index="stu_id")
    data_res=[]
    for complement in complements:
        data_complement={}
        sign=db.findSign(data=complement[4],index="sgn_id")[0]
        if cou_id==sign[5]:
            data_complement["sgn_index"]=sign[3]
            data_complement["bsgn_reason"]=complement[1]
            data_complement["bsgn_state"]=complement[2]
            data_complement["bsgn_time"]=str(complement[5])

            data_res.append(data_complement)

    return jsonify(data_res),200,{"Content-Type":"application/json"}
            
@app.route('/cmpl_get2', methods=['GET','POST'])
def getComplement2():
    cou_id=request.get_json()["cou_id"]

    db=Mysql()

    data_res=[]
    signs=db.findByStrData(table="signs",data=cou_id,index="cou_id")
    for sign in signs:
        sgn_id=sign[0]
        complements=db.findByStrData(table="complements",data=sgn_id,index="sgn_id")

        for complement in complements:
            data_complement={}

            data_complement["sgn_index"]=sign[3]
            data_complement["bsgn_reason"]=complement[1]
            data_complement["bsgn_state"]=complement[2]
            data_complement["bsgn_time"]=str(complement[5])
            data_complement["stu_id"]=complement[3]

            data_complement["stu_name"]=db.findStudent(data=complement[3],index="stu_id")[0][1]


            data_res.append(data_complement)



    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/cmpl_get3', methods=['GET','POST'])
def getComplement3():
    stu_id=request.get_json()["stu_id"]

    db=Mysql()
    data_res=[]

    complements=db.findByStrData(table="complements",data=stu_id,index="stu_id")
    for comp in complements:
        data_comp={}
        data_comp["bsgn_reason"]=comp[1]
        data_comp["bsgn_state"]=comp[2]
        data_comp["bsgn_time"]=str(comp[5])
        sgn_id=comp[4]

        sign=db.findSign(data=sgn_id,index="sgn_id")[0]
        data_comp["sgn_index"]=sign[3]
        course=db.findCourse(data=sign[5],index="cou_id")[0]
        data_comp["cou_id"]=course[0]
        data_comp["cou_name"]=course[1]

        data_res.append(data_comp)

    return jsonify(data_res),200,{"Content-Type":"application/json"}

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    stu_name=request.values.get("name")
    stu_id=request.values.get("xuehao")
    stu_wxid=request.values.get("openid")
    
    ifSucess=True

    db=Mysql()
    results_s=db.findStudent(data=stu_id,index="stu_id")

    if results_s:
        if results_s[0][1]!=stu_name:
            ifSucess=False
        if results_s[0][2]!=stu_wxid:
            ifSucess=False
    else :
        ifSucess=False

    
    if ifSucess:
        file_name=stu_name+'_'+stu_id+".jpg"
        request.files.to_dict()["editormd-image-file"].save('./imgs/'+file_name)
        

        return "修改成功", 200, {"Content-Type": "application/json"}

    else :
        return "修改失败", 290, {"Content-Type": "application/json"}
        
@app.route("/imgs/<filename>")
def get_filename(filename):
 
    with open(r'./imgs/{}'.format(filename),'rb') as f:
        fileas = f.read()
        resp = Response(fileas,mimetype='application/octet-stream')

    return jsonify(resp)
        
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
    

