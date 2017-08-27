#作者：吴明轩，陈丁香凝
#创建日期：2017年5月26日
#描述：Dijkstra算法实现以及前端实现

#运行这个文件！

import datetime as dt
import sqlite3
from flask import Flask, request, render_template
webApp=Flask(__name__,static_url_path="",static_folder="")

#定义一个函数通过站名来获得该地铁站的id
def getID(stationName):
	dbConn=sqlite3.connect('subwayInfo.db')
	reqStr="select stationID from stationInfoForm where stationName='"+stationName+"'"
	myCursor=dbConn.execute(reqStr)
	myID=myCursor.fetchall()[0][0]
	myCursor.close()
	dbConn.close()
	return myID

#反过来，定义一个函数通过id来获得该地铁站的中文名称
def getStationName(myID):
	dbConn=sqlite3.connect('subwayInfo.db')
	myCursor=dbConn.execute("select stationName from stationInfoForm where stationID="+str(myID))
	myName=myCursor.fetchall()[0][0]
	myCursor.close()
	dbConn.close()
	return myName

#在北京地铁官网中，各个地铁对应的id并不是其线路名称，这里我们用一个函数实现转换
def idToName(myID):
	transDict={"0":"1号线","1":"2号线","2":"4号线","3":"5号线","4":"6号线","5":"8号线",\
	"6":"9号线","7":"10号线","8":"13号线","9":"14号线","10":"15号线","11":"八通线",\
	"12":"昌平线","13":"亦庄线","15":"房山线","16":"机场线"}
	return transDict[str(myID)]

#与上面函数相反功能的函数
#为了简便直接返回字符串
def nameToID(myName):
	transDict={"1号线":"0","2号线":"1","4号线":"2","5号线":"3","6号线":"4","8号线":"5",\
	"9号线":"6","10号线":"7","13号线":"8","14号线":"9","15号线":"10","八通线":"11",\
	"昌平线":"12","亦庄线":"13","房山线":"15","机场线":"16","大兴线":"2"}
	if myName not in transDict:
		return -1
	else:
		return transDict[myName]

'''
#定义一个函数用来返回两个站台之间相差的时间
#调整算法后这个函数似乎不再需要
def getDis(stationID1,stationID2):
	dbConn=sqlite3.connect('subwayInfo.db')
	formName="station"+str(stationID1)+"Form"
	myCursor=dbConn.execute("select distance from '"+formName+"' where stationID="+str(stationID2))
	myDis=myCursor.fetchall()[0][0]
	myCursor.close()
	dbConn.close()
	return myDis
'''

#定义一个函数来确定一个时刻是否在另两个时刻之中
#这个函数用于判断现在的时刻是否已经错过末班车或首班车还没发
def isIn(timeNow,startStr,endStr):
	#为了符合我们存储数据的现有格式，timeNow要求是time类
	#而startStr和endStr要求是形如"3:34"这样的字符串
	#首先运用split函数读出小时和分钟
	startList=startStr.split(":")
	startTime=dt.time(int(startList[0]),int(startList[1]))
	endList=endStr.split(":")
	endTime=dt.time(int(endList[0]),int(endList[1]))
	#需要注意的是有些末班车是形如0:15，这会在判断中出现错误
	if timeNow.hour==0:
		#那么只需要和末班车进行比较
		if endTime.hour!=0:
			return False
		else:
			return timeNow<endTime
	elif endTime.hour==0:
		#那么只需要和首班车进行比较
		return startTime<timeNow
	else:
		return (startTime<timeNow) and (timeNow<endTime)

#定义一个函数用来计算一个time类加上一个int类型的分钟的所得结果，返回time类数据
def timeAdd(timeNow,deltaNum):
	hourNow=timeNow.hour
	minuteNow=timeNow.minute
	if minuteNow+deltaNum<60:
		return dt.time(hourNow,minuteNow+deltaNum)
	elif hourNow<23:
		return dt.time(hourNow+1,minuteNow+deltaNum-60)
	else:
		return dt.time(0,minuteNow+deltaNum-60)

#定义一个函数用来验证所给的字符串是否是一个地铁站名
def isStation(myStr):
	dbConn=sqlite3.connect('subwayInfo.db')
	myCursor=dbConn.execute("select * from stationInfoForm where stationName='"+myStr+"'")
	if len(myCursor.fetchall())==0:
		myCursor.close()
		dbConn.close()
		return False
	else:
		myCursor.close()
		dbConn.close()
		return True

#定义一个函数用来判断所读的字符串是否是一个合法的时间
def isTime(myStr):
	#首先确认该字符串中有且仅有一个:符号
	myCount=0
	for i in myStr:
		if i==":":
			myCount+=1
	if myCount!=1:
		return False
	else:
		timeList=myStr.split(":")
		#尝试将:两边的字符转换为整数
		try:
			myHour=int(timeList[0])
			myMinute=int(timeList[1])
		except:
			return False
		else:
			#验证小时和分钟在合适的范围内
			if myHour>=24 or myHour<0 or myMinute>=60 or myMinute<0:
				return False
			else:
				return True

#定义一个函数返回两个字符串相同字符的个数
def sameNum(str1,str2):
	myCount=0
	for i in str1:
		if i in str2:
			myCount+=1
	return myCount

#定义一个函数用来将所给的字符串匹配站名
def matchStation(myStr):
	#从数据库中取出所有的站名
	dbConn=sqlite3.connect('subwayInfo.db')
	myCursor=dbConn.execute("select stationName from stationInfoForm")
	myList=myCursor.fetchall()
	myCursor.close()

	#循环进行匹配
	resultDict={}
	for i in myList:
		if sameNum(myStr,i[0])>=2:
		#如果有至少两个汉字一样，算配对成功
			resultDict[i[0]]=sameNum(myStr,i[0])

	#按频率倒序排列
	resultList=sorted(resultDict.items(),key=lambda x:x[1], reverse=True)
	
	#去掉频率组成一个新的list
	stationList=[]
	for i in resultList:
		stationList.append(i[0])
	return stationList

#首先，我们建立一个station类表示每一个站台便于后续计算
class Station:

	#定义初始化函数
	def __init__(self, myID):
		#val表示从起点出发到这个站的最短时间，-1表示尚未设置
		self.val=-1
		#myTime表示从起点出发到这个站的最短时刻，0时0分0秒表示尚未设置
		self.myTime=dt.time(0,0)
		#decided表示这个站的最短时间是否被确定，0表示没有，1表示已确定
		self.decided=0
		#journey表示从起点到这个站的前进路线，以列表形式呈现
		self.journey=[]
		#lineList表示从起点到这个站的前进路线的线路号，以列表形式呈现
		self.lineList=[]
		#stationID表示这个站在数据库中的编号
		self.stationID=myID

	#定义函数寻找当前时刻下该站能通到的所有站，以列表形式返回所有id,花费时间、途径线路(3个表)
	def findConnect(self):
		dbConn=sqlite3.connect('subwayInfo.db')
		formName="station"+str(self.stationID)+"Form"
		myCursor=dbConn.execute("select * from '"+formName+"'")
		myList=myCursor.fetchall()
		connectList=[]
		connectTimeList=[]
		connectStationList=[]
		for i in myList:
			if isIn(self.myTime,i[3],i[4]):
				connectList.append(i[0])
				connectTimeList.append(i[2])
				connectStationList.append(i[5])
		myCursor.close()
		dbConn.close()
		return connectList, connectTimeList, connectStationList

	#定义函数打印该站点的情况
	def printInfo(self):
		if self.decided!=1:
			content="这个站点还没有被确定，请检查算法是否有误!"
			return content
		else:
			content="从起点到该站点所需要的时间为:"+str(self.val)+"分钟<br>"
			#再显示路线
			content+="途中经过的站点为: "
			for i in self.journey:
				content+=getStationName(i)+" "
			content+="<br>"
			#最后显示换乘方法
			content+="下面是具体的换乘方法:<br>"
			content+="从起点站坐"+idToName(self.lineList[0])+"<br>"
			countNum=0
			for i in range(len(self.lineList)-1):
				if self.lineList[i]!=self.lineList[i+1]:
					passNum=i-countNum+1
					countNum=i+1
					content+=str(passNum)+"站后换乘"+idToName(self.lineList[i+1])+"<br>"
			content+=str(len(self.lineList)-countNum)+"站后到达终点"
			return content
	
	#定义比较函数，首先比较时间val，相同情况下比较stationID
	def __lt__(self, other):
		if self.val==other.val:
			return self.stationID<other.stationID
		else:
			return self.val<other.val

#现在我们开始进入算法部分
def findPath(stationName1,stationName2,timeNow):
	#timeNow为形如08:45这样的字符串

	#查看表格我们可以知道一共有294个地铁站(0-293号),因此首先需要创造294个Station类对象
	#如此一来，myArray[id]即表示第“id”号地铁站的情况
	myArray=[]
	for i in range(294):
		myArray.append(Station(i))

	#焦点表示现在正在研究的地铁站id，之所以不使用Station类是因为python的类复制似乎比较麻烦
	startID=getID(stationName1)
	endID=getID(stationName2)
	focusPoint=startID
	#设置初始点的各种参数
	#设置初始距离为0
	myArray[startID].val=0
	#设置初始时间为函数中的参数时间，转换为time类便于计算
	timeList=timeNow.split(":")
	myArray[startID].myTime=dt.time(int(timeList[0]),int(timeList[1]))
	#设置决定状态为决定
	myArray[startID].decided=1
	#设置初始站点的途径站点
	myArray[startID].journey.append(startID)
	#设置tempList以储存所有曾经被考虑过但还没有被决定的Station对象的id
	tempList=[startID]

	#开始进入循环
	while True:
		#找到焦点的所有相邻站点，且保证这些站点都没有被确定过
		newStationList,newTimeList,newLineList=myArray[focusPoint].findConnect()
		#去掉这个list里面所有已经被确定过的点
		myIndex=0
		while myIndex<len(newStationList):
			if myArray[newStationList[myIndex]].decided==1:
				del newStationList[myIndex]
				del newTimeList[myIndex]
				del newLineList[myIndex]
				myIndex-=1
			myIndex+=1
		#对所有剩下的点进行更新工作
		for i in range(len(newStationList)):
			if myArray[newStationList[i]].val==-1:
				#这表明这个站点还从来没有访问过
				#写入这个站点的距离(目前)
				#先考虑这一站是否要换乘，我们目前假设换乘需要2分钟
				if len(myArray[newStationList[i]].lineList)!=0 and myArray[newStationList[i]].lineList[-1]!=newLineList[i]:
					newTimeList[i]+=2
				myArray[newStationList[i]].val=myArray[focusPoint].val+newTimeList[i]
				#写入这个站点的时间(目前)
				myArray[newStationList[i]].myTime=timeAdd(myArray[focusPoint].myTime,newTimeList[i])
				#写入这个站点的途径站点，这里避免浅复制
				tempArray=myArray[focusPoint].journey[:]
				tempArray.append(newStationList[i])
				myArray[newStationList[i]].journey=tempArray[:]
				#写入通往这个站点的交通线路
				tempArray2=myArray[focusPoint].lineList[:]
				tempArray2.append(newLineList[i])
				myArray[newStationList[i]].lineList=tempArray2[:]
				#把这个站点的序号推进tempList队列
				tempList.append(newStationList[i])
			else:
				#这表明这个站点已经被访问过
				#如果焦点能提供更短的路线，则更新这个站点
				if myArray[focusPoint].val+newTimeList[i]<myArray[newStationList[i]].val:
					#写入这个站点的距离(目前)
					myArray[newStationList[i]].val=myArray[focusPoint].val+newTimeList[i]
					#写入这个站点的时间(目前)
					myArray[newStationList[i]].myTime=timeAdd(myArray[focusPoint].myTime,newTimeList[i])
					#写入这个站点的途径站点，这里避免浅复制
					tempArray=myArray[focusPoint].journey[:]
					tempArray.append(newStationList[i])
					myArray[newStationList[i]].journey=tempArray[:]
					#写入通往这个站点的交通线路
					tempArray2=myArray[focusPoint].lineList[:]
					tempArray2.append(newLineList[i])
					myArray[newStationList[i]].lineList=tempArray2[:]
		#从tempList中找到下一个焦点
		#首先判断tempList中除了目前的焦点之外是否还有别的元素
		if len(tempList)<=1:
			return "找不到对应的路线，请尝试其他的时间"
		else:
			#首先将现在的焦点从tempList中去除
			tempList.remove(focusPoint)
			#然后在剩下的元素中选出新的焦点
			focusPoint=tempList[0]
			for i in tempList:
				if myArray[i]<myArray[focusPoint]:
					focusPoint=i
			#将这个焦点的decided值改为1
			myArray[focusPoint].decided=1
		#判断新的焦点是否为我们的终点
		if focusPoint==endID:
			return myArray[endID].printInfo()
		#如果不是的话继续返回循环

#现在我们进行前端实现，首页
@webApp.route("/")
def root():
	return webApp.send_static_file("index.html")

#线路规划页面
@webApp.route("/routeSearch",methods=["GET","POST"])
def searchroute():
	searchInfo="计算可能需要一定时间，请耐心等待。"

	#获取数据
	if request.method=="POST":
		startStationName=request.form["startStation"]
		endStationName=request.form["endStation"]
		timeStr=request.form["timeNow"]

		#在计算之前首先确定站点名称存在
		if not isStation(startStationName) or not isStation(endStationName):
			searchInfo="错误的站点名称，请查询后重新输入."
			return render_template("routeSearch.html",searchInfo=searchInfo)
		#确定时间字符串是否合法
		elif not isTime(timeStr):
			searchInfo="非法的时间，请重新输入，注意要用半角符号噢."
			return render_template("routeSearch.html",searchInfo=searchInfo)
		#其他情况下进行计算
		searchInfo=findPath(startStationName,endStationName,timeStr)
		return render_template("routeSearch.html",searchInfo=searchInfo)
	
	return render_template("routeSearch.html",searchInfo=searchInfo)

#模糊搜索页面
@webApp.route("/stationSearch",methods=["GET","POST"])
def searchstation():
	searchInfo="计算可能需要一定时间，请耐心等待。"
	
	#获取数据
	if request.method=="POST":
		searchStr=request.form["searchStr"]
		resultList=matchStation(searchStr)

		if len(resultList)==0:
			searchInfo="对不起，没有找到对应的站名，您可以更换关键词或按线路搜索."
		else:
			searchInfo="以下是和您的搜索结果最匹配的站点:<br>"
			for i in resultList:
				searchInfo+=i+" "

	return render_template("stationSearch.html",searchInfo=searchInfo)

#站点情况页面
@webApp.route("/stationInfo",methods=["GET","POST"])
def stationinfo():
	searchInfo="计算可能需要一定时间，请耐心等待。"

	#获取数据
	if request.method=="POST":
		searchStr=request.form["stationName"]

		#确认输入的字符串是否是一个地铁站名
		if not isStation(searchStr):
			searchInfo="您输入的地铁站不存在，请查询后重新输入."
			return render_template("stationInfo.html",searchInfo=searchInfo)

		else:
			searchInfo="以下是您搜索的站点的所有相邻站点:<br>"
			dbConn=sqlite3.connect('subwayInfo.db')
			formName="station"+str(getID(searchStr))+"Form"
			myCursor=dbConn.execute("select stationName, startTime, endTime, lineID from '"+formName+"'")
			myList=myCursor.fetchall()
			for i in myList:
				searchInfo+="站名: "+i[0]+", 开始时间: "+i[1]+", 结束时间: "+i[2]+", 线路名称: "+idToName(i[3])+"<br>"
			myCursor.close()
			dbConn.close()
			return render_template("stationInfo.html",searchInfo=searchInfo)

	return render_template("stationInfo.html",searchInfo=searchInfo)

#线路搜索页面
@webApp.route("/lineSearch",methods=["GET","POST"])
def searchline():
	searchInfo="计算可能需要一定时间，请耐心等待。"

	#获取数据
	if request.method=="POST":
		searchStr=request.form["lineName"]

		#判断所得的字符串是否是一个地铁线路名
		result=nameToID(searchStr)
		if result==-1:
			searchInfo="您输入的地铁线路名不存在，请查询后重新输入."
			return render_template("lineSearch.html",searchInfo=searchInfo)
		else:
			searchInfo="以下是您搜索的地铁线路的所有站点:<br>"
			dbConn=sqlite3.connect('subwayInfo.db')
			formName="line"+result+"Form"
			myCursor=dbConn.execute("select stationName from '"+formName+"'")
			myList=myCursor.fetchall()
			myCount=0
			#为了网站的美观考虑，每6个站换一行
			for i in myList:
				searchInfo+=i[0]+" "
				if myCount%6==5:
					searchInfo+="<br>"
				myCount+=1
			return render_template("lineSearch.html",searchInfo=searchInfo)

	return render_template("lineSearch.html",searchInfo=searchInfo)

if __name__=="__main__":
	# Adding "threaded=True" significantly boosts the speed of the program on my laptop
	webApp.run(host='0.0.0.0',port=80,debug=True,threaded=True)

#eof
