#Author: illusion
#Date: 2017/05/14
#Description: python file for the website

from flask import Flask, request, render_template, session, redirect
webApp=Flask(__name__,static_url_path="",static_folder="")
webApp.secret_key='123456'
import sqlite3

'''
# First, create an account for the dean
# These codes are only necessary for the project in the beggining
dbConn=sqlite3.connect('deanSystem.db')
dbConn.execute("create table pwdForm (id varchar(10) primary key not null, password varchar(20) not null, job int not null, status boolean not null)")
# Set our account for the dean
# job refers to dean(0), teacher(1) or student(2)
# status refers to whether the user has set his account
dbConn.execute("insert into pwdForm (id, password, job, status) values('admin','admin',0,1)")
dbConn.commit()

# Test the content in the form
myCursor=dbConn.execute("select * from pwdForm")
for i in myCursor:
	print(i)
myCursor.close()
dbConn.close()
'''

# Create the login website
@ webApp.route("/login",methods=["GET","POST"])
def logIn():
	logInInfo=""

	# Get the data from html file
	if request.method=="POST":
		oldUserName=request.form["oldID"]
		oldPassword=request.form["oldpassword"]

		# Read the old username and password from our database
		dbConn=sqlite3.connect('deanSystem.db')
		searchStr="select * from pwdForm where id='"+oldUserName+"'"
		myCursor=dbConn.execute(searchStr)
		myList=myCursor.fetchall()

		if len(myList)==0:
			logInInfo="对不起，该用户名没有被注册过，请重新输入或注册."
		elif myList[0][1] != oldPassword:
			logInInfo="对不起，密码输入错误，请重新输入."
		else:
			logInInfo="恭喜您，登陆成功！现转入您的操作页面"
			session['oldID']=oldUserName
			if myList[0][3]==False:
				return webApp.send_static_file("templates/pwdSet.html")
			elif myList[0][2]==1:
				return webApp.send_static_file("teacher.html")
			elif myList[0][2]==2:
				return webApp.send_static_file("student.html")
			else:
				return webApp.send_static_file("dean.html")
		
		myCursor.close()
		dbConn.close()

	return render_template("logIn.html",logInInfo=logInInfo)

#Create a function to tell whether a password is legal
def isLegal(myStr):
	flag1=False
	flag2=False 
	flag3=False 
	flag4=False
	#flag1 checks the length of the password
	if len(myStr)>=8 and len(myStr)<=20:
		flag1=True
	#flag 2,3,4 check whether the password contains number, lower, upper letter
	for i in myStr:
		if i.isdigit():
			flag2=True
		if i.islower():
			flag3=True
		if i.isupper():
			flag4=True
	return flag1 and flag2 and flag3 and flag4

# Create the password setting website
@ webApp.route("/pwdSet",methods=["GET","POST"])
def pwdset():
	signUpInfo=""
	oldUserName=session['oldID']

	# Get the data from html file
	if request.method=="POST":
		newPassword=request.form["newpassword"]
		newPassword2=request.form["newpassword2"]

		if newPassword!=newPassword2:
			signUpInfo="对不起，您输入的两次密码不相同，请重新输入."
		elif isLegal(newPassword)==False:
			signUpInfo="对不起，非法的密码，请查看密码要求并重新输入."
		else:
			signUpInfo="恭喜您，密码已经被重置！"

			# Write the new username and password to the data file
			dbConn=sqlite3.connect('deanSystem.db')
			myStr="update pwdForm set password='"+newPassword+"' where id='"+oldUserName+"'"
			dbConn.execute(myStr)
			dbConn.commit()
			# Change the status into True
			myStr="update pwdForm set status=1 where id='"+oldUserName+"'"
			dbConn.execute(myStr)
			dbConn.commit()
			# Take the user to his page
			searchStr="select * from pwdForm where id='"+oldUserName+"'"
			myCursor=dbConn.execute(searchStr)
			myList=myCursor.fetchall()
			dbConn.close()
			if myList[0][2]==1:
				return webApp.send_static_file("teacher.html")
			else:
				return webApp.send_static_file("student.html")

	return render_template("pwdSet.html",signUpInfo=signUpInfo)

#Create the id set website for dean
@webApp.route("/idSet",methods=["GET","POST"])
def setaccount():
	setInfo=""

	# Get the data from html file
	if request.method=="POST":
		newID=request.form["newID"]
		newJob=request.form["newJob"]
	
		# Read from our database to make sure there will not be repeated ids
		dbConn=sqlite3.connect('deanSystem.db')
		searchStr="select * from pwdForm where id='"+newID+"'"
		myCursor=dbConn.execute(searchStr)
		myList=myCursor.fetchall()
		if len(myList)!=0:
			setInfo="该id已经被注册过，请确认后重新输入。"
		else:
			#Create a form for the user
			#Name rule: userid+"Form" e.g. teacher1Form
			formName=newID+"Form"
			if newJob==1:
				reqStr="create table '"+formName+"' (courseID varchar, courseName varchar, classID varchar)"
				dbConn.execute(reqStr)
				dbConn.commit()
			else:
				reqStr="create table '"+formName+"' (courseID varchar, courseName varchar, classID varchar, totalGrade int)"
				dbConn.execute(reqStr)
				dbConn.commit()
			
			#Write into the password Form about the newuser
			myStr="insert into pwdForm (id, password, job, status) values('"+newID+"','666666',"+newJob+",0)"
			dbConn.execute(myStr)
			dbConn.commit()
			setInfo="成功录入！"
		myCursor.close()
		dbConn.close()
	return render_template("idSet.html",setInfo=setInfo)

# Create the log out website
@webApp.route("/logout")
def logout():
	session.pop('oldID',None)
	return render_template("logIn.html",logInInfo="已登出，请重新登录。")

# Create the course set website for dean
@webApp.route("/courseSet",methods=["GET","POST"])
def courseInfo():
	setInfo=""
	dbConn=sqlite3.connect('deanSystem.db')

	# These codes are only necessary for the project in the beggining
	'''
	dbConn=sqlite3.connect('deanSystem.db')
	dbConn.execute("create table courseInfoForm (courseID varchar(10), courseName varchar(20), courseNum int)")
	dbConn.commit()
	'''

	# Get the data from html file
	if request.method=="POST":
		newCourseID=request.form["newcourseid"]
		newCourseName=request.form["newcoursename"]

		# Check if there is another course with the same id
		searchStr="select * from courseInfoForm where courseID='"+newCourseID+"'"
		myCursor=dbConn.execute(searchStr)
		myList=myCursor.fetchall()
		if len(myList)!=0:
			setInfo="该id已经被注册过，请确认后重新输入。"
		else:
			# Write the data into our form
			myStr="insert into courseInfoForm (courseID,courseName,courseNum) values('"+newCourseID+"','"+newCourseName+"',0)"
			dbConn.execute(myStr)
			dbConn.commit()
			setInfo="成功录入课程信息！"
		
		myCursor.close()
		dbConn.close()
	return render_template("courseSet.html",setInfo=setInfo)

# Create the course teach website for teachers
@webApp.route("/courseTeach",methods=["GET","POST"])
def teachcourse():
	oldUserName=session['oldID']
	content=""
	content+="<h1>欢迎来到认领课程界面</h1>"

	#First, print all the course information on the website
	dbConn=sqlite3.connect('deanSystem.db')
	myCursor=dbConn.execute("select * from courseInfoForm")
	content+="<table> <tr> <td>课程id</td> <td>课程名</td> <td>目前已开班数</td> </tr>"
	myList=myCursor.fetchall()
	for i in myList:
		content+="<tr> <td>"+i[0]+"</td> <td>"+i[1]+"</td> <td>"+str(i[2])+"</td> </tr>"
	content+="</table>"
	myCursor.close()
	content+="<p>请在下方输入想要认领的课程id</p>"
	content+='<form action="/courseTeach" method="post"> <a>课程ID</a><input type=text name="courseid"><br> <input type=submit value="认领" /> </form>'

	#Deal with the elective function
	if request.method=="POST":
		courseID=request.form["courseid"]
		#check whether the course id exists
		reStr="select * from courseInfoForm where courseID='"+courseID+"'"
		resultList=dbConn.execute(reStr).fetchall()
		if len(resultList)==0:
			content+="</p>课程编号有误，请重新输入！</p>"

		else:
		
			#check whether the course has already been taught
			formName=oldUserName+"Form"
			reStr="select * from '"+formName+"' where courseID='"+courseID+"'"
			resultList=dbConn.execute(reStr).fetchall()
			if len(resultList)!=0:
				content+="</p>您已经认领过该课程！</p>"
			else:

				# Write the data into courseInfoForm
				reqStr="select courseNum from courseInfoForm where courseID='"+courseID+"'"
				CourseNum=str(int(dbConn.execute(reqStr).fetchall()[0][0])+1)
				reqStr="update courseInfoForm set courseNum="+CourseNum+" where courseID='"+courseID+"'"
				dbConn.execute(reqStr)
				dbConn.commit()

				# Write the data into the user form
				classID=CourseNum+courseID
				formName=oldUserName+"Form"
				reStr="select courseName from courseInfoForm where courseID='"+courseID+"'"
				courseName=dbConn.execute(reStr).fetchall()[0][0]
				reqStr="insert into '"+formName+"' (courseID,courseName,classID) values('"+courseID+"','"+courseName+"','"+classID+"')"
				dbConn.execute(reqStr)
				dbConn.commit()

				# Create a form for the course
				# Form name rule: courseid+Form e.g. course1Form
				formName=courseID+"Form"
				reqStr="create table if not exists '"+formName+"' (classID varchar, teacherID varchar)"
				dbConn.execute(reqStr)
				dbConn.commit()
				reqStr="insert into '"+formName+"' (classID, teacherID) values('"+classID+"','"+oldUserName+"')"
				dbConn.execute(reqStr)
				dbConn.commit()				

				# Create a form for the class
				# Class id generate rule: coursenum+courseid e.g. 1course1,3course5...
				formName=classID+"Form"
				reqStr="create table '"+formName+"' (studID varchar, dailyGrade int, midGrade int, finalGrade int, totalGrade int)"
				dbConn.execute(reqStr)
				dbConn.commit()

				content+="<p>您已成功认领该课程</p>"

	content+="<a href='teacher.html'>返回</a><br>"
	dbConn.close()
	return content

#Create the course select website for students
@webApp.route("/courseSelect",methods=["GET","POST"])
def selectcourse():
	oldUserName=session['oldID']
	content=""
	content+="<h1>欢迎来到选课界面</h1>"

	#First, print all the class information on the website
	dbConn=sqlite3.connect('deanSystem.db')
	content+="<table> <tr> <td>课程id</td> <td>课程名</td> <td>班级id</td> <td>任课老师</td> <td>选课人数</td> </tr>"
	myCursor=dbConn.execute("select courseID, courseName from courseInfoForm")
	courseList=myCursor.fetchall()
	for i in courseList:
		courseID=i[0]
		courseName=i[1]
		formName=courseID+"Form"
		reqStr="select * from '"+formName+"'"
		classList=dbConn.execute(reqStr).fetchall()
		for j in classList:
			classID=j[0]
			teacherID=j[1]
			formName=classID+"Form"
			reqStr="select count(*) from '"+formName+"'"
			studNum=dbConn.execute(reqStr).fetchall()[0][0]
			content+="<tr> <td>"+courseID+"</td> <td>"+courseName+"</td> <td>"+classID+"</td> <td>"+teacherID+"</td> <td>"+str(studNum)+"</td> </tr>"
	content+="</table>"
	myCursor.close()
	content+="<p>请在下方输入想要选的班级id</p>"
	content+='<form action="/courseSelect" method="post"> <a>班级ID</a><input type=text name="classid"><br> <input type=submit value="选课" /> </form>'
	
	#Deal with the elective function
	if request.method=="POST":
		classID=request.form["classid"]
		flag=1
		formName=classID+"Form"

		#check whether the class exists
		reqStr="SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+formName+"'"
		myCursor=dbConn.execute(reqStr).fetchall()
		if myCursor[0][0]==0:
			flag=0
			content+="<p>不存在这个班级，请查询后重新输入.</p>"

		else:
			#check whether the student number exceeds 30
			formName=classID+"Form"
			reqStr="select count(*) from '"+formName+"'"
			studNum=dbConn.execute(reqStr).fetchall()[0][0]
			#studNum shoud never exceed 30, however we just make the condition >= in safe
			if studNum>=30:
				flag=0
				content+="<p>这个班级已经被选满，请选择其他班级.</p>"

		#Check whether the the student already selects the course
		#We assume that students cannot select one course within different teachers
		#According to our name rule, we can easily find the courseID from classID
		beginIndex=0
		for i in range(len(classID)):
			if classID[i]=='c':
				beginIndex=i
				break
		courseID=classID[beginIndex:]
		formName=oldUserName+"Form"
		reqStr="select count(*) from '"+formName+"' where courseID='"+courseID+"'"
		reqNum=dbConn.execute(reqStr).fetchall()[0][0]
		if reqNum!=0:
			flag=0
			content+="<p>你已经选过这门课</p>"
		
		#If flag still equals to 1, indicating that the class id satisfy all three requiremennt
		if flag==1:
			
			#write the data into user form
			#find the courseName
			reqStr="select courseName from CourseInfoForm where courseID='"+courseID+"'"
			courseName=dbConn.execute(reqStr).fetchall()[0][0]
			#insert into userform
			formName=oldUserName+"Form"
			reqStr="insert into '"+formName+"' (courseID, courseName, classID) values('"+courseID+"','"+courseName+"','"+classID+"')"
			dbConn.execute(reqStr)
			dbConn.commit()

			#write the data into the class form
			formName=classID+"Form"
			reqStr="insert into '"+formName+"' (studID) values('"+oldUserName+"')"
			dbConn.execute(reqStr)
			dbConn.commit()

			content+="<p>恭喜，你已经成功选上这门课.</p>"

	content+="<a href='student.html'>返回</a><br>"
	dbConn.close()
	return content

#Create the grade set website for teachers
@webApp.route("/gradeSet",methods=["GET","POST"])
def setgrade():
	oldUserName=session['oldID']
	#If there is any courseID in the session, delete it
	if 'oldClassID' in session:
		session.pop('oldClassID',None)
	
	content="<h1>欢迎来到成绩录入界面</h1>"
	content+="<p>以下是您目前教授的课程列表</p>"

	#Print all the class that the teacher teaches
	dbConn=sqlite3.connect('deanSystem.db')
	content+="<table> <tr> <td>课程id</td> <td>课程名</td> <td>班级id</td> <td>尚未评分人数</td> </tr>"
	formName=oldUserName+"Form"
	reqStr="select * from '"+formName+"'"
	myCursor=dbConn.execute(reqStr)
	myList=myCursor.fetchall()
	for i in myList:
		#获取尚未评分人数
		formName=i[2]+"Form"
		reqStr="select count(*) from '"+formName+"' where totalGrade is null"
		tempCursor=dbConn.execute(reqStr)
		myNum=tempCursor.fetchall()[0][0]
		tempCursor.close()
		content+="<tr> <td>"+i[0]+"</td> <td>"+i[1]+"</td> <td>"+i[2]+"</td> <td>"+str(myNum)+"</td> </tr>"
	
	content+="</table>"
	myCursor.close()
	content+="<p>请在下方输入想要录入成绩的班级ID</p>"
	content+='<form action="/gradeSet" method="post"> <a>班级ID</a><input type=text name="classid"><br> <input type=submit value="提交" /> </form>'
	
	#Deal with the grade set function
	if request.method=="POST":
		classID=request.form["classid"]
		flag=1
		formName=classID+"Form"

		#check if the classid exists in the teacher's class
		formName=oldUserName+"Form"
		reqStr="select count(*) from '"+formName+"' where classID='"+classID+"'"
		myCursor=dbConn.execute(reqStr).fetchall()
		if myCursor[0][0]==0:
			flag=0
			content+="<p>不存在这个班级或者该班级不在您的列表中，请查询后重新输入.</p>"
		else:
			#check if the teacher already sets the weight for dailyGrade, midGrade and finalGrade
			#we do this by finding whether the grade form exists for the class
			session['oldClassID']=classID
			formName=classID+"GradeForm"
			reqStr="SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+formName+"'"
			tempCursor=dbConn.execute(reqStr)
			myNum=tempCursor.fetchall()[0][0]
			tempCursor.close()
			
			if myNum==0:
				#redirect to weight set website
				return webApp.send_static_file("templates/weightSet.html")

			else:
				#redirect to grade enter website
				return redirect("/gradeEnter")

	content+="<a href='teacher.html'>返回</a><br>"
	dbConn.close()
	return content

#Create the weight set website for teachers
@webApp.route("/weightSet",methods=["GET","POST"])
def setweight():
	setInfo=""
	classID=session['oldClassID']
	#msgFlag=1 indicates that we are correct, different mistakes will change this number
	msgFlag=1

	#Deal with the weight
	if request.method=="POST":
		dailyPtg=request.form["dailyptg"]
		midPtg=request.form["midptg"]
		finalPtg=request.form["finalptg"]

		#check whether the percentage is positive integers
		ptgList=[dailyPtg,midPtg,finalPtg]
		for i in ptgList:
			if not i.isdigit():
				msgFlag=0
				break
		#check whether the percentage add to 100
		else:
			mySum=0
			for i in ptgList:
				mySum+=int(i)
			if mySum!=100:
				msgFlag=-1

		#deal with the wrong situation
		if msgFlag==0:
			setInfo="必须输入正整数！"
		elif msgFlag==-1:
			setInfo="权重之和必须为100！"
		else:
			#write the weight into our database
			#name rule: classID+GradeForm e.g. 1course1GradeForm
			dbConn=sqlite3.connect('deanSystem.db')
			formName=classID+"GradeForm"
			reqStr="create table '"+formName+"' (dailyptg int, midptg int, finalptg int)"
			dbConn.execute(reqStr)
			dbConn.commit()
			reqStr="insert into '"+formName+"' (dailyptg, midptg, finalptg) values("+dailyPtg+","+midPtg+","+finalPtg+")"
			dbConn.execute(reqStr)
			dbConn.commit()
			dbConn.close()
			setInfo="成功设置课程分数权重！"
			
			#redirect the user to grade enter website
			return redirect("/gradeEnter")	
	
	return render_template("weightSet.html",setInfo=setInfo)

#Create the grade enter website for teachers
@webApp.route("/gradeEnter",methods=["GET","POST"])
def entergrade():

	classID=session['oldClassID']
	content="<h1>欢迎来到成绩录入系统</h1>"
	content+="<p>下面显示您的班级情况</p>"

	#print the class information onto the website
	content+="<table> <tr> <td>学生id</td> <td>平时成绩</td> <td>期中成绩</td> <td>期末成绩</td> <td>总成绩</td> </tr>"
	dbConn=sqlite3.connect('deanSystem.db')
	formName=classID+"Form"
	reqStr="select * from '"+formName+"'"
	myList=dbConn.execute(reqStr).fetchall()
	for i in myList:
		content+="<tr> <td>"+i[0]+"</td> <td>"+str(i[1])+"</td> <td>"+str(i[2])+"</td> <td>"+str(i[3])+"</td> <td>"+str(i[4])+"</td> </tr>"
	content+="</table>"

	#print the grade set policy onto the website
	content+="<p>下面是您设置的分数权重分配政策</p>"
	formName=classID+"GradeForm"
	reqStr="select * from '"+formName+"'"
	ptgList=dbConn.execute(reqStr).fetchall()[0]
	content+="<p>平时分数:"+str(ptgList[0])+"%,期中分数:"+str(ptgList[1])+"%,期末分数:"+str(ptgList[2])+"%</p>"

	#read the grade from the form
	content+="<p>请在下方输入想要录入的学生id以及平时分数、期中分数、期末分数，系统将自动计算总分数，分数必须是0到100之内的整数</p>"
	content+='<form action="/gradeEnter" method="post"> <a>学生ID</a><input type=text name="studentid"><a>平时成绩</a><input type=text name="dailygrade"><a>期中成绩</a><input type=text name="midgrade"><a>期末成绩</a><input type=text name="finalgrade"><br> <input type=submit value="提交" /> </form>'

	#deal with the grade
	flag=1
	if request.method=="POST":
		studentID=request.form["studentid"]
		dailyGrade=request.form["dailygrade"]
		midGrade=request.form["midgrade"]
		finalGrade=request.form["finalgrade"]

		#check whether the student id is valid
		formName=classID+"Form"
		reqStr="select count(*) from '"+formName+"' where studID='"+studentID+"'"
		myNum=dbConn.execute(reqStr).fetchall()[0][0]
		if myNum==0:
			content+="<p>这个学生的id不存在或者不在您的班级中，请查询后重新输入</p>"
			flag=0
		else:
			#check whether the grade is valid
			gradeList=[dailyGrade,midGrade,finalGrade]
			for i in gradeList:
				if not i.isdigit():
					content+="<p>您输入的成绩有至少一项不是正整数，请重新输入</p>"
					flag=0
					break
			else:
				gradeList=[int(dailyGrade),int(midGrade),int(finalGrade)]
				for i in gradeList:
					if i<0 or i>100:
						content+="<p>您输入的成绩有至少一项不在0到100内，请重新输入</p>"
						flag=0
						break

		#Calculate the total grade
		if flag==1:
			totalGrade=0
			for i in range(3):
				totalGrade+=int(ptgList[i])*gradeList[i]
			totalGrade=round(totalGrade/100)
			
			#Write into the class form
			formName=classID+"Form"
			reqStr="update '"+formName+"' set dailyGrade="+str(gradeList[0])+", midGrade="+str(gradeList[1])+", finalGrade="+str(gradeList[2])+", totalGrade="+str(totalGrade)+" where studID='"+studentID+"'"
			dbConn.execute(reqStr)
			dbConn.commit()

			#Write into the student form
			formName=studentID+"Form"
			reqStr="update '"+formName+"' set totalGrade="+str(totalGrade)+" where classID='"+classID+"'"
			dbConn.execute(reqStr)
			dbConn.commit()
			content+="<p>录入成绩成功！</p>"


	content+="<a href='teacher.html'>返回</a><br>"
	dbConn.close()
	return content

#We finally end all the database manipulate website, hooray!
#The remaining website are all dealing with search, display...

#Create the id search website for deans
@webApp.route("/search",methods=["GET","POST"])
def searchid():
	content="<h1>欢迎来到人员信息搜寻系统</h1>"
	content+="<p>请在下方输入您要查找的老师或者学生的id</p>"
	content+='<form action="/search" method="post"> <a>查询ID</a><input type=text name="oldid"><br> <input type=submit value="查询"/> </form>'

	dbConn=sqlite3.connect('deanSystem.db')

	#check if the id exists
	if request.method=="POST":
		oldID=request.form["oldid"]
		reqStr="select count(*) from pwdForm where id='"+oldID+"'"
		myNum=dbConn.execute(reqStr).fetchall()[0][0]
		if myNum==0:
			content+="<p>您查找的id不存在，请查询后重新输入</p>"
		else:
			#get the job of the user
			reqStr="select job from pwdForm where id='"+oldID+"'"
			myJob=dbConn.execute(reqStr).fetchall()[0][0]
			if myJob==1:
				content+="<p>下面是这位老师的任课情况</p>"
				content+="<table> <tr> <td>课程id</td> <td>课程名</td> <td>班级id</td> </tr>"
				formName=oldID+"Form"
				reqStr="select * from '"+formName+"'"
				myCursor=dbConn.execute(reqStr).fetchall()
				for i in myCursor:
					content+="<tr> <td>"+i[0]+"</td> <td>"+i[1]+"</td> <td>"+i[2]+"</td> </tr>"
				content+="</table>"
			else:
				content+="<p>下面是这位同学的选课情况</p>"
				content+="<table> <tr> <td>课程id</td> <td>课程名</td> <td>班级id</td> <td>总成绩</td> </tr>"
				formName=oldID+"Form"
				reqStr="select * from '"+formName+"'"
				myCursor=dbConn.execute(reqStr).fetchall()
				for i in myCursor:
					content+="<tr> <td>"+i[0]+"</td> <td>"+i[1]+"</td> <td>"+i[2]+"</td> <td>"+str(i[3])+"</td> </tr>"
				content+="</table>"

	content+="<a href='dean.html'>返回</a><br>"
	dbConn.close()
	return content

#Create the course and class search system for deans
@webApp.route("/courseInfo",methods=["GET","POST"])
def searchcourse():
	content="<h1>欢迎来到课程信息搜寻系统</h1>"
	content+="<p>请在下方输入您要查找的课程或者班级的id</p>"
	content+='<form action="/courseInfo" method="post"> <a>查询ID</a><input type=text name="oldid"><br> <input type=submit value="查询"/> </form>'
	dbConn=sqlite3.connect('deanSystem.db')

	#check if the id exists
	if request.method=="POST":
		flag=1
		oldID=request.form["oldid"]
		#Our name rule can tell whether it is an id for a course or a class
		if 'c' not in oldID:
			flag=0
		else:
			formName=oldID+"Form"
			reqStr="SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+formName+"'"
			myCursor=dbConn.execute(reqStr)
			if myCursor.fetchall()[0][0]==0:
				flag=0
			myCursor.close()
		
		#deal with the wrong situation
		if flag==0:
			content+="<p>错误的id，它可能并不存在，或者不是一个课程、班级id</p>"
		
		#deal with the correct situation
		if flag==1:
			#figure out whether it is a class or a course
			if oldID[0].isdigit():
				content+="<p>下面是这个班级的选课情况</p>"
				content+="<table> <tr> <td>学生id</td> <td>平时成绩</td> <td>期中成绩</td> <td>期末成绩</td> <td>总成绩</td> </tr>"
				formName=oldID+"Form"
				reqStr="select * from '"+formName+"'"
				myList=dbConn.execute(reqStr).fetchall()
				for i in myList:
					content+="<tr> <td>"+i[0]+"</td> <td>"+str(i[1])+"</td> <td>"+str(i[2])+"</td> <td>"+str(i[3])+"</td> <td>"+str(i[4])+"</td> </tr>"
				content+="</table>"
			else:
				content+="<p>下面是这个课程的开班情况</p>"
				content+="<table> <tr> <td>班级id</td> <td>教师id</td> </tr>"
				formName=oldID+"Form"
				reqStr="select * from '"+formName+"'"
				myList=dbConn.execute(reqStr).fetchall()
				for i in myList:
					content+="<tr> <td>"+i[0]+"</td> <td>"+i[1]+"</td> </tr>"
				content+="</table>"
				
	content+="<a href='dean.html'>返回</a><br>"
	dbConn.close()
	return content

#We finished all the websites for deans, hooray!
#Create the website for teachers to see who select their courses
@webApp.route("/courseSearch",methods=["GET","POST"])
def searchclass():
	content="<h1>欢迎来到选课名单查询系统</h1>"
	content+="<p>下面是您目前的开班情况</p>"
	oldUserName=session['oldID']
	dbConn=sqlite3.connect('deanSystem.db')

	#print all the class information on the website
	content+="<table> <tr> <td>课程id</td> <td>课程名</td> <td>班级id</td> </tr>"
	formName=oldUserName+"Form"
	reqStr="select * from '"+formName+"'"
	myCursor=dbConn.execute(reqStr).fetchall()
	for i in myCursor:
		content+="<tr> <td>"+i[0]+"</td> <td>"+i[1]+"</td> <td>"+i[2]+"</td> </tr>"
	content+="</table>"
	content+="<p>请在下方输入您要查看的班级id</p>"
	content+='<form action="/courseSearch" method="post"> <a>查询ID</a><input type=text name="oldid"><br> <input type=submit value="查询"/> </form>'

	#deal with the search function
	if request.method=="POST":
		classID=request.form["oldid"]
		#check whether the id is valid
		formName=oldUserName+"Form"
		reqStr="select count(*) from '"+formName+"' where classID='"+classID+"'"
		if dbConn.execute(reqStr).fetchall()[0][0]==0:
			content+="<p>错误的id，请查询后重新输入</p>"
		else:
			formName=classID+"Form"
			content+="<p>下面是这个班级的选课情况</p>"
			content+="<table> <tr> <td>学生id</td> <td>平时成绩</td> <td>期中成绩</td> <td>期末成绩</td> <td>总成绩</td> </tr>"
			reqStr="select * from '"+formName+"'"
			myList=dbConn.execute(reqStr).fetchall()
			for i in myList:
				content+="<tr> <td>"+i[0]+"</td> <td>"+str(i[1])+"</td> <td>"+str(i[2])+"</td> <td>"+str(i[3])+"</td> <td>"+str(i[4])+"</td> </tr>"
			content+="</table>"

	content+="<a href='teacher.html'>返回</a><br>"
	dbConn.close()
	return content	

#We finished all the websites for teachers, hooray!
#Create the website for students to view their grade
@webApp.route("/gradeList")
def viewgrade():
	content="<h1>欢迎来到成绩查询系统</h1>"
	content+="<p>下面是您目前的选课以及成绩情况,None表示尚未出分，请耐心等待</p>"
	oldUserName=session['oldID']
	dbConn=sqlite3.connect('deanSystem.db')

	content+="<table> <tr> <td>课程id</td> <td>课程名</td> <td>班级id</td> <td>总成绩</td> </tr>"
	formName=oldUserName+"Form"
	reqStr="select * from '"+formName+"'"
	myCursor=dbConn.execute(reqStr).fetchall()
	for i in myCursor:
		content+="<tr> <td>"+i[0]+"</td> <td>"+i[1]+"</td> <td>"+i[2]+"</td> <td>"+str(i[3])+"</td> </tr>"
	content+="</table>"
	
	content+="<a href='student.html'>返回</a><br>"
	dbConn.close()
	return content	

#Finally, I am able to finish this challenging project, the amount of code far more exceeds my past coding experience!
#I sincerely appreciate the coordination from flask, sqlite3 and html for not giving me more troubles.
#A world without bugs is just so wonderful!

if __name__=="__main__":
	# Adding "threaded=True" significantly boosts the speed of the program on my laptop
	webApp.run(host='0.0.0.0',port=80,debug=True,threaded=True)

#eof