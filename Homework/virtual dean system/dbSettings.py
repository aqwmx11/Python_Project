#Author: illusion
#Date: 2017/05/15
#Description: code file to change the setting of some forms in database
#Note: You do not need to run this file

import sqlite3

#为了后续处理简便，在课程信息表格中加入一栏，表示目前有多少教授开班
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("alter table courseInfoForm add column courseNum int")
dbConn.commit()
dbConn.close()
'''

#补上教授开班数信息
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("update courseInfoForm set courseNum=0")
dbConn.commit()
dbConn.close()
'''

#打印目前的课程情况
'''
dbConn=sqlite3.connect('deanSystem.db')
myCursor=dbConn.execute("select * from courseInfoForm")
print(myCursor.fetchall())
dbConn.close()
'''

#为了后续处理简便，在密码表格中增加一栏，表示该学生(老师)目前参与的课程编号
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("alter table pwdForm add column course varchar")
dbConn.commit()
dbConn.close()
'''

#打印目前的密码表情况
'''
dbConn=sqlite3.connect('deanSystem.db')
myCursor=dbConn.execute("select * from pwdForm")
print(myCursor.fetchall())
dbConn.close()
'''

#对于更新列表的几个尝试
'''
oldUserName="teacher1"
courseID="course1"
dbConn=sqlite3.connect('deanSystem.db')
reStr="select course from pwdForm where id='"+oldUserName+"'"
courseList=dbConn.execute(reStr).fetchall()[0][0]
if courseList is not None:
	print("ok")
if courseList is None:
	courseList=courseID
else:
	courseList+=","+courseID
content=""
if len(courseList)!=0 and courseID in courseList:
	content+="</p>您已经认领过该课程！</p>"
else:
	content+="</p>成功认领该课程！</p>"
print(content)
dbConn.close()
'''
'''
courseID="course1"
dbConn=sqlite3.connect('deanSystem.db')
reqStr="select courseNum from courseInfoForm where courseID='"+courseID+"'"
CourseNum=str(int(dbConn.execute(reqStr).fetchall()[0][0])+1)
classID=CourseNum+courseID
formName=classID+"Form"
reqStr="create table "+formName+" (teacherID varchar, studID varchar)"
print(reqStr)
dbConn.close()
'''

#删除失败的列表
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("drop table '1course1Form'")
dbConn.execute("drop table '1course2Form'")
dbConn.execute("drop table '1course3Form'")
dbConn.execute("drop table '2course1Form'")
dbConn.execute("drop table 'course1Form'")
dbConn.execute("drop table 'course2Form'")
dbConn.execute("drop table 'course3Form'")
dbConn.commit()
myCursor=dbConn.execute("SELECT name FROM sqlite_master WHERE type='table' order by name")
print(myCursor.fetchall())
myCursor.close()
dbConn.close()
'''

#重置所有teacher的列表
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("update pwdForm set course= Null")
dbConn.commit()
dbConn.close()
'''

#重置一个认领数
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("update courseInfoForm set courseNum=1 where courseid='course1'")
dbConn.commit()
dbConn.close()
'''

#查看目前的数据库情况
'''
dbConn=sqlite3.connect('deanSystem.db')
myCursor=dbConn.execute("SELECT name FROM sqlite_master WHERE type='table' order by name")
print(myCursor.fetchall())
myCursor.close()
dbConn.close()
'''


#一些尝试
'''
dbConn=sqlite3.connect('deanSystem.db')
myCursor=dbConn.execute("select * from CourseInfoForm where courseID='course4'")
print(myCursor.fetchall())
if len(myCursor.fetchall())==0:
	print("ok")
myCursor.close()
dbConn.close()
'''

#修改了表的结构，去掉pwdForm中的course一栏，改为为每个教师和学生新增一张表
#由于sqlite不支持直接删去一列，并且我们需要测试新的表格是否起效，这里直接删去pwdForm然后重建
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("drop table 'pwdForm'")
dbConn.commit()
'''
#重建新的pwdForm
'''
dbConn.execute("create table pwdForm (id varchar, password varchar, job int, status int)")
#插入admin账户
dbConn.execute("insert into pwdForm (id,password,job,status) values('admin','admin',0,1)")
dbConn.commit()
dbConn.close()
'''

#重置一些错误的表格
'''
dbConn=sqlite3.connect('deanSystem.db')
#dbConn.execute("drop table '2course1Form'")
#dbConn.execute("delete from course1Form where teacherID='teacher2'")
#dbConn.execute("update courseInfoForm set courseNum=1 where courseid='course1'")
#dbConn.execute("delete from teacher2Form where courseID='course1'")
dbConn.commit()
dbConn.close()
'''

#一些测试
'''
dbConn=sqlite3.connect('deanSystem.db')
myCursor=dbConn.execute("select courseID,courseName from courseInfoForm")
classList=myCursor.fetchall()
oneClass=classList[0][0]
className=classList[0][1]
formName=oneClass+"Form"
reqStr="select * from '"+formName+"'"
classList=dbConn.execute(reqStr).fetchall()
someClass=classList[0][0]
formName=someClass+"Form"
reqStr="select count(*) from '"+formName+"'"
numList=dbConn.execute(reqStr).fetchall()
num=numList[0][0]
print(type(num))
myCursor.close()
dbConn.close()
'''

#展示某个表中的数据
def showData(formName):
	dbConn=sqlite3.connect('deanSystem.db')
	reqStr="select * from '"+formName+"'"
	print(dbConn.execute(reqStr).fetchall())
	dbConn.close()

#修正表格数据模板
#参数为：要修改的表格，定位用的列名，具体列名，要改的列名，要改的值
def changeData(formName,idName,idVal,changeName,changeVal):
	dbConn=sqlite3.connect('deanSystem.db')
	reqStr="update '"+formName+"' set '"+changeName+"' = '"+changeVal+"' where '"+idName+"' ='"+idVal+"'"
	dbConn.execute(reqStr)
	dbConn.commit()
	dbConn.close()

'''
changeData("course1Form","teacherID","teacher1","classID","1course1")
changeData("teacher1Form","courseID","course1","classID","1course1")
'''

#创建一个1course1Form
'''
dbConn=sqlite3.connect('deanSystem.db')
reqStr="create table '1course1Form' (studID varchar, dailyGrade int, midGrade int, finalGrade int, totalGrade int)"
dbConn.execute(reqStr)
dbConn.commit()
dbConn.close()
'''
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("update course1Form set classID='1course1' where teacherID='teacher1'")
dbConn.execute("update teacher1Form set classID='1course1' where courseID='course1'")
dbConn.commit()
showData("course1Form")
showData("teacher1Form")
dbConn.close()
'''

#测试数据库中是否存在某个表格
def isExist(formName):
	dbConn=sqlite3.connect('deanSystem.db')
	reqStr="SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+formName+"'"
	myCursor=dbConn.execute(reqStr).fetchall()
	if myCursor[0][0]==0:
		return False
	else:
		return True

#尝试从classID反推courseID
def findCourseID(classID):
	#find the index of letter "c"
	beginIndex=0
	for i in range(len(classID)):
		if classID[i]=='c':
			beginIndex=i
			break
	return classID[beginIndex:]

#尝试是否能获得未评分学生的个数
def findStudNum(classID):
	dbConn=sqlite3.connect('deanSystem.db')
	formName=classID+"Form"
	reqStr="select count(*) from '"+formName+"' where totalGrade is null"
	myCursor=dbConn.execute(reqStr)
	myNum=myCursor.fetchall()[0][0]
	myCursor.close()
	dbConn.close()
	return myNum

#尝试是否能获得已评分学生的个数
def findStudNum2(classID):
	dbConn=sqlite3.connect('deanSystem.db')
	formName=classID+"Form"
	reqStr="select count(*) from '"+formName+"' where totalGrade is not null"
	myCursor=dbConn.execute(reqStr)
	myNum=myCursor.fetchall()[0][0]
	myCursor.close()
	dbConn.close()
	return myNum

#尝试是否能将实数转换为整数
def isInt(myStr):
	try:
		x=int(myStr)
		return isinstance(x,int)
	except ValueError:
		return False

#回滚一个数据库处理
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("delete from '1course1Form' where studID='student1'")
dbConn.commit()
dbConn.close()
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("insert into '1course1Form' (studID) values('student1')")
dbConn.commit()
dbConn.close()
'''
'''
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("delete from '1course1Form' where totalGrade=94")
dbConn.execute("delete from 'student1Form' where totalGrade=94")
dbConn.commit()
dbConn.close()
showData('student1Form')
showData('1course1Form')
'''

if 'c' in '1course1':
	print("here!")