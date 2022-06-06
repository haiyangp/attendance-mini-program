
from operator import index
from unittest import result
import pymysql
class Mysql(object):
    def __init__(self):
        try:
            self.db = pymysql.connect(host="localhost",user="root",password="root",database="Kaoqing_System")
            #游标对象
            self.cursor = self.db.cursor()
            print("success")
        except:
            print("fail")
    

    # 查找学生
    def findStudent(self,data,index="stu_id"):

        sql='select * from students where '+index+' = '+'\''+data+'\''

        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        results = self.cursor.fetchall()

        return results

    # 查找学生老师或者课程
    def findTeacher(self,data,index="tea_id"):
        # print(obj.type)
        sql='select * from teachers where '+index+' = '+'\''+data+'\''
        
        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        results = self.cursor.fetchall()

        return results


    # 查找课程
    def findCourse(self,data,index):

        sql='select * from courses where '+index+' = '+'\''+data+'\''

        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        results = self.cursor.fetchall()

        return results

    # 查找学生选课记录
    def findStudent_Course(self,data,index):

        sql='select * from students_courses where '+index+' = '+'\''+data+'\''

        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        results = self.cursor.fetchall()

        return results

    # 查找正在签到
    def findSigning2(self,data,index):
        sql='select * from signs where sgn_state = 1 and ' +index+' = '+'\''+data+'\''

        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        results = self.cursor.fetchall()


        if results:
            return True
        else:
            return False

    # 删除课程
    def deleteCourse(self,data,index):
        sql='delete from courses where '+index+' = '+'\''+data+'\''

        self.cursor.execute(sql)
        self.db.commit()

        return True

    def deleteStudent_Course(self,data,index):
        sql='delete from students_courses where '+index+' = '+'\''+data+'\''

        self.cursor.execute(sql)
        self.db.commit()

        return True

    # 插入学生
    def insertStudent(self,data):
        result_temp=self.findStudent(data=data["stu_id"],index="stu_id")
  
        if result_temp:
            return False

        sql='''insert into students (stu_id,stu_name,stu_wxid) values (\'%s\',\'%s\',\'%s\');''' %(data["stu_id"],data["stu_name"],data["stu_wxid"])


        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()


        return True

    # 插入课程
    def insertCourse(self,data):
        result_temp=self.findCourse(data=data["cou_id"],index="cou_id")

        if result_temp:
            return False
        
        sql='''insert into courses (cou_id,cou_name,tea_id) values (\'%s\',\'%s\',\'%s\');''' %(data["cou_id"],data["cou_name"],data["tea_id"])

        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()


        return True

    # 插入学生选课记录
    def insertStudent_Course(self,data):
        haveInserted=False

        result_temp=self.findStudent_Course(data=data["stu_id"],index="stu_id")
        for student_course in result_temp:
            if(student_course[2]==data["cou_id"]) :
                haveInserted=True

        # 重复加入
        if haveInserted:
            return 1

        # 加入不存在的课程
        course=self.findCourse(data=data["cou_id"],index="cou_id")
        if not course:
            return 2

        sql='''insert into students_courses (sc_id,stu_id,cou_id) values (\'%s\',\'%s\',\'%s\');''' %(data["sc_id"],data["stu_id"],data["cou_id"])

        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()

        return 0

    def insertSign(self,data):
        index=self.getSignTimes(data["cou_id"])+1

        sql='''insert signs (sgn_id,sgn_time,sgn_roomtype,sgn_index,sgn_state,cou_id,latitude,longitude) values (\'%s\',\'%s\',\'%s\',%d,%d,\'%s\',%f,%f)''' %(data["sgn_id"],data["sgn_time"],data["sgn_roomtype"],index,data["sgn_state"],data["cou_id"],data["latitude"],data["longitude"])
        


        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()

        return data["sgn_id"]

    def updateSign(self,sgn_id):
        sql='''update signs set sgn_state=0 where sgn_id=\'%s\' ''' %(sgn_id)



        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()

        return True

    def findSign(self,data,index):
        sql='''select * from signs where %s=\'%s\' ''' %(index,data)

        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        result = self.cursor.fetchall()

        return result

    def findSigning(self,data,index):
        sql='''select * from signs where %s=\'%s\' and sgn_state=1 ''' %(index,data)

        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        result = self.cursor.fetchall()

        return result




    def insertStudent_Sign(self,data):
        sql='''insert into students_signs (ss_id,stu_id,sgn_id,seat,time) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')''' %(data["ss_id"],data["stu_id"],data["sgn_id"],data["seat"],data["time"])
        
        print(sql)
        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()

        return True

    def insertException(self,data):
        sql='''insert into exceptions (excp_id,excp_describe,excp_state,stu_id,sgn_id) values (\'%s\',\'%s\',%d,\'%s\',\'%s\')''' %(data["excp_id"],data["excp_describe"],data["excp_state"],data["stu_id"],data["sgn_id"])
        
        print(sql)
        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()

        return True

    def insertComplement(self,data):
        sql='''insert into complements (bsgn_id,bsgn_reason,bsgn_state,stu_id,sgn_id,bsgn_time) values (\'%s\',\'%s\',%d,\'%s\',\'%s\',\'%s\')''' %(data["bsgn_id"],data["bsgn_reason"],data["bsgn_state"],data["stu_id"],data["sgn_id"],data["bsgn_time"])

        print(sql)
        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()

        return True

    def alterComplement(self,bsgn_id,bsgn_state):
        sql ='''update complements set bsgn_state=%d where bsgn_id=\'%s\' ''' %(bsgn_state,bsgn_id)
        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()

        return True

    def alterException(self,excp_id):
        sql ='''update exceptions set excp_state=0 where excp_id=\'%s\' ''' %(excp_id)
        # 插入确认
        self.cursor.execute(sql)
        self.db.commit()

        return True
        

    def findByStrData(self,table,data,index):
        sql='''select * from %s where %s=\'%s\' ''' %(table,index,data)

        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        result = self.cursor.fetchall()

        return result

    def findByDigiData(self,table,data,index):
        sql='''select * from %s where %s=%d ''' %(table,index,data)

        #执行sql语句
        self.cursor.execute(sql)

        #获取所有的记录
        result = self.cursor.fetchall()

        return result

    # 过去一门课的学生学生人数
    def getStudentsNum(self,cou_id):
        sql='''select COUNT(*) from students_courses where cou_id=\'%s\' ''' %(cou_id)

        self.cursor.execute(sql)
        
        result = self.cursor.fetchall()

        return result

    # 过去一门课的学生学生人数
    def getStudentsNumInSign(self,sgn_id):
        sql='''select COUNT(*) from students_signs where sgn_id=\'%s\' ''' %(sgn_id)

        self.cursor.execute(sql)
        
        result = self.cursor.fetchall()

        return result

    def getSignTimes(self,cou_id):
        sql='select sgn_index from signs where sgn_state=0 and cou_id=\''+ cou_id+'\' order by sgn_index desc limit 1'  

        print(sql)

        #执行sql语句
        self.cursor.execute(sql)

        #获取记录
        result = self.cursor.fetchall()

        print(result)

        if result:
            return result[0][0]
        else:
            return 0



    # def getData(self):
    #     sql = "select * from students "
    #     #执行sql语句
    #     self.cursor.execute(sql)
    #     #获取所有的记录
    #     results = self.cursor.fetchall()
    #     return results

    # # 插入课程
    # def insertCourse(self,data):
    #     sql='''insert into courses (cou_id,cou_name,cou_tea_id,qiandao_times,cou_code) values (\'%s\',\'%s\',\'%s\',0,\'%s\');''' %(data["id"],data["name"],data["user_id"],data["code"])

    #     print(sql)
    #     self.cursor.execute(sql)
    #     self.db.commit()

    #     return True



    # # 插入选课
    # def insertXuanke(self,data):
    #     sql='''insert into xuanke (xua_stu_id,xua_cou_id) values (\'%s\',\'%s\');''' %(data["stu_id"],data["cou_id"])

    #     print(sql)
    #     self.cursor.execute(sql)
    #     self.db.commit()

    #     return True

    # #关闭
    # def __del__(self):
    #     self.db.close()
