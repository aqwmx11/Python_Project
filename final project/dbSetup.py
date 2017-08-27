#作者：吴明轩，陈丁香凝
#创建日期：2017年5月23日
#描述：生成数据库并存储所需要的地铁信息
#在实际操作中，你不需要运行这个文件，数据库将直接附在文件夹中

#在本项目中，我们一共需要三大类表格
#每一站的表格，包含所有与该站能够直接相连的地铁站的id与中文名，距离，首末班车时间（以该站为起点），同属哪条线路
#总站表格，包含所有的地铁站的id和中文名
#每一条地铁线的表格，包含该线路上所有站的id与站名

from urllib import request
from bs4 import BeautifulSoup as BS
import sqlite3

#尝试获取北京地铁网站的html文本
myUrl="http://www.bjsubway.com/e/action/ListInfo/?classid=39&ph=1"
dataFromWeb=request.urlopen(myUrl)
#非常神奇的是这个网站使用gb2312编码而不是utf-8
strData=dataFromWeb.read().decode("gb2312","ignore")

'''
#首先抓取所有地铁站并为它们建立id
#注意到所有地铁站站名所属id的命名规则为sub+数字，数字从0到18
idList=[]
for i in range(19):
	idList.append("sub"+str(i))

#初始化集合存储已经被存过的站名
stationSet=set()
#初始化分配id
myID=0

#开始爬虫
oBS=BS(strData,"html.parser")
for i in idList:
	rawBS=oBS.find_all("",{"id":i})[0].find_all("tbody")[0].find_all("th")
	for j in rawBS:
		if j.string is not None:
			stationSet.add(j.string.strip())

#将爬虫的结果写入数据库
dbConn=sqlite3.connect('subwayInfo.db')
dbConn.execute("create table stationInfoForm (stationID int, stationName varchar)")
for i in stationSet:
	reqStr="insert into stationInfoForm (stationID, stationName) values("+str(myID)+",'"+i+"')"
	dbConn.execute(reqStr)
	myID+=1
dbConn.commit()
dbConn.close()
'''

#定义一个函数通过站名来获得该地铁站的id
def getID(stationName):
	dbConn=sqlite3.connect('subwayInfo.db')
	reqStr="select stationID from stationInfoForm where stationName='"+stationName+"'"
	myCursor=dbConn.execute(reqStr)
	myID=myCursor.fetchall()[0][0]
	myCursor.close()
	dbConn.close()
	return myID

#为每一个地铁站建立一个表格
#命名方式为station+id+Form,如station1Form
'''
dbConn=sqlite3.connect('subwayInfo.db')
myCursor=dbConn.execute("select * from stationInfoForm")
myList=myCursor.fetchall()
for i in range(len(myList)):
	formName="station"+str(i)+"Form"
	reqStr="create table '"+formName+"' (stationID int, stationName varchar, distance int, startTime text, endTime text, lineID int)"
	dbConn.execute(reqStr)
	dbConn.commit()
myCursor.close()
dbConn.close()
'''

'''
#我们首先获取直接相连的地铁站的id与中文名，首末班车时间（以该站为起点），同属哪条线路这些信息
#然而网站上的时间表格式非常不统一，我们只能分而处理
#其中，1、5、8、16号线和八通线、亦庄线、房山线的表格模式是一样的，将其在网页中的编号组成一组
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
myList=[0,3,5,18,11,13,15]
for i in myList:
	searchID="sub"+str(i)
	stationList=[]
	timeList=[]
	rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
	for j in rawBS:
		j=str(j.string).strip()
		stationList.append(j)
	rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
	for j in rawBS:
		j=str(j.string).strip()
		timeList.append(j)
	#现在我们开始处理我们接收到这些站点和时间，对于每个站点来说，除了首发站和尾站外它将得到两个邻站的信息
	for k in range(len(stationList)):
		stationID=getID(stationList[k])
		formName="station"+str(stationID)+"Form"
		if k>0:
			#这表明这个站点存在前一站
			prevStation=stationList[k-1]
			prevID=getID(prevStation)
			prevStartTime=timeList[4*k+2]
			prevEndTime=timeList[4*k+3]
			#把对应信息写到数据库的对应表格中
			reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(i)+")"
			dbConn.execute(reqStr)
			dbConn.commit()
		if k<len(stationList)-1:
			#这表明这个站点存在后一站
			nextStation=stationList[k+1]
			nextID=getID(nextStation)
			nextStartTime=timeList[4*k]
			nextEndTime=timeList[4*k+1]
			#把对应信息写到数据库的对应表格中
			reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(i)+")"
			dbConn.execute(reqStr)
			dbConn.commit()
	print("已经写好一条线路!")
dbConn.close()
'''

#检查网页发现十四号线居然有两个table，所以在数据库中补上
#获取现在的地铁站表并编成一个list
'''
dbConn=sqlite3.connect('subwayInfo.db')
myCursor=dbConn.execute("select * from stationInfoForm")
myID=281
stationList=[]
for i in myCursor:
	stationList.append(i[1])
myCursor.close()
oBS=BS(strData,"html.parser")
rawBS=oBS.find_all("",{"id":"sub9"})[0].find_all("tbody")[1].find_all("th")
for j in rawBS:
	if j.string is not None:
		stationName=str(j.string).strip()
		if stationName not in stationList:
			stationList.append(stationName)
			reqStr="insert into stationInfoForm (stationID, stationName) values("+str(myID)+",'"+stationName+"')"
			dbConn.execute(reqStr)
			formName="station"+str(myID)+"Form"
			reqStr="create table '"+formName+"' (stationID int, stationName varchar, distance int, startTime text, endTime text, lineID int)"
			dbConn.execute(reqStr)
			dbConn.commit()
			myID+=1
dbConn.close()
print("成功写完数据！")
print(len(stationList))
'''

#机场线的首末班格式与前面一致，但神奇的是没有在网页上加载出来，是我看html代码时发现的，这里补上
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(16)
stationList=[]
timeList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList.append(j)
#现在我们开始处理我们接收到这些站点和时间，对于每个站点来说，除了首发站和尾站外它将得到两个邻站的信息
for k in range(len(stationList)):
	stationID=getID(stationList[k])
	formName="station"+str(stationID)+"Form"
	if k>0:
		#这表明这个站点存在前一站
		prevStation=stationList[k-1]
		prevID=getID(prevStation)
		prevStartTime=timeList[4*k+2]
		prevEndTime=timeList[4*k+3]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(16)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
	if k<len(stationList)-1:
		#这表明这个站点存在后一站
		nextStation=stationList[k+1]
		nextID=getID(nextStation)
		nextStartTime=timeList[4*k]
		nextEndTime=timeList[4*k+1]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(16)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

#接下来我们处理其他的线路，这些线路几乎没有同一种格式的...
#我们首先处理7号线和9号线，这两条线的格式与前面基本类似，区别是顺序是反的...
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
myList=[6,17]
for i in myList:
	searchID="sub"+str(i)
	stationList=[]
	timeList=[]
	rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
	for j in rawBS:
		j=str(j.string).strip()
		stationList.append(j)
	rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
	for j in rawBS:
		j=str(j.string).strip()
		timeList.append(j)
	#现在我们开始处理我们接收到这些站点和时间，对于每个站点来说，除了首发站和尾站外它将得到两个邻站的信息
	for k in range(len(stationList)):
		stationID=getID(stationList[k])
		formName="station"+str(stationID)+"Form"
		if k>0:
			#这表明这个站点存在前一站
			prevStation=stationList[k-1]
			prevID=getID(prevStation)
			prevStartTime=timeList[4*k]
			prevEndTime=timeList[4*k+1]
			#把对应信息写到数据库的对应表格中
			reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(i)+")"
			dbConn.execute(reqStr)
			dbConn.commit()
		if k<len(stationList)-1:
			#这表明这个站点存在后一站
			nextStation=stationList[k+1]
			nextID=getID(nextStation)
			nextStartTime=timeList[4*k+2]
			nextEndTime=timeList[4*k+3]
			#把对应信息写到数据库的对应表格中
			reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(i)+")"
			dbConn.execute(reqStr)
			dbConn.commit()
	print("已经写好一条线路!")
dbConn.close()
'''

#接下来开始每个地铁站一张表
'''
#2号线是一个神奇的环线
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(1)
stationList=[]
timeList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList.append(j)
#现在我们开始处理我们接收到这些站点和时间
#我们需要单独处理西直门，积水潭和车公庄三个站，其余站的处理方法一致
for k in range(len(stationList)):
	stationID=getID(stationList[k])
	formName="station"+str(stationID)+"Form"
	#由于Python支持-1表示列表的最后一项，这里恰好不需要单独处理西直门站
	#这表明这个站点存在前一站
	prevStation=stationList[k-1]
	prevID=getID(prevStation)
	prevStartTime=timeList[6*k]
	#处理积水潭站的特殊之处
	if k!=1:
		prevEndTime=timeList[6*k+2]
	else:
		prevEndTime=timeList[7]
	#把对应信息写到数据库的对应表格中
	reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(1)+")"
	dbConn.execute(reqStr)
	dbConn.commit()
	#这表明这个站点存在后一站
	#处理车公庄站
	if k!=len(stationList)-1:
		nextStation=stationList[k+1]
	else:
		nextStation=stationList[0]
	nextID=getID(nextStation)
	nextStartTime=timeList[6*k+3]
	#处理西直门站
	if k!=0:
		nextEndTime=timeList[6*k+5]
	else:
		nextEndTime=timeList[4]
	#把对应信息写到数据库的对应表格中
	reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(1)+")"
	dbConn.execute(reqStr)
	dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

'''
#四号线的一部分的半程线路有更晚的末班车(安河桥北到公益西桥)
#我们这里对于四号线和大兴线不加区分，因为在网页中也无法看出这两条线的区别，实际操作中也没有意义
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(2)
stationList1=[]
stationList2=[]
timeList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
flag=0
for j in rawBS:
	j=str(j.string).strip()
	if flag%2==0:
		stationList1.append(j)
	else:
		stationList2.append(j)
	flag+=1
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList.append(j)	
#处理上行线路
for k in range(len(stationList1)-1):
	stationID=getID(stationList1[k])
	formName="station"+str(stationID)+"Form"
	nextStation=stationList1[k+1]
	nextID=getID(nextStation)
	nextStartTime=timeList[5*k]
	nextEndTime=timeList[5*k+1]
	#把对应信息写到数据库的对应表格中
	reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(2)+")"
	dbConn.execute(reqStr)
	dbConn.commit()
#处理下行路线
for k in range(len(stationList2)-1):
	stationID=getID(stationList2[k])
	formName="station"+str(stationID)+"Form"
	nextStation=stationList2[k+1]
	nextID=getID(nextStation)
	nextStartTime=timeList[5*k+2]
	#有半程地铁
	if k<=22:
		nextEndTime=timeList[5*k+4]
	#无半程地铁
	else:
		nextEndTime=timeList[5*k+3]
	#把对应信息写到数据库的对应表格中
	reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(2)+")"
	dbConn.execute(reqStr)
	dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

'''
#6号线也存在半程车
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(4)
stationList=[]
timeList=[]
#注意，由于通运门站和北运河东站不开放，为了契合我们对于表格的定义，我们这里认为他们上下相邻两站相邻
#例如，通运门的相邻两战为通州北关和北运河西，我们认为这两站是相邻的
#其做法为直接去掉通运门站和北运河东站
flag=0
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	if flag!=22 and flag!=24:
		j=str(j.string).strip()
		stationList.append(j)
	flag+=1
flag=0
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	if flag!=22 and flag!=24:
		j=str(j.string).strip()
		timeList.append(j)
	flag+=1
#现在我们开始处理我们接收到这些站点和时间，对于每个站点来说，除了首发站和尾站外它将得到两个邻站的信息
for k in range(len(stationList)):
	stationID=getID(stationList[k])
	formName="station"+str(stationID)+"Form"
	if k>0:
		#这表明这个站点存在前一站
		prevStation=stationList[k-1]
		prevID=getID(prevStation)
		prevStartTime=timeList[5*k]
		prevEndTime=timeList[5*k+1]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(4)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
	if k<len(stationList)-1:
		#这表明这个站点存在后一站
		nextStation=stationList[k+1]
		nextID=getID(nextStation)
		nextStartTime=timeList[5*k+2]
		#存在最后一班半程车
		if k<19:
			nextEndTime=timeList[5*k+4]
		#不存在最后一班半程车
		else:
			nextEndTime=timeList[5*k+3]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(4)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

#10号线是我觉得最变态的线路了，不仅是个环线还有若干线路...
#实测中发现，由于某种神奇的机理，惠新西街南口没有被程序读进去了，那里变成了None...
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(7)
stationList1=[]
stationList2=[]
timeList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
flag=0
for j in rawBS:
	j=str(j.string).strip()
	#处理这个神奇的bug
	if j=='None':
		j="惠新西街南口"
	if flag%2==0:
		stationList1.append(j)
	else:
		stationList2.append(j)
	flag+=1
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList.append(j)
#处理下行线路
#由于惠新西街南口的bug，前门的数据已经写入了，所以起始位置变了
for k in range(9,len(stationList1)):
	stationID=getID(stationList1[k])
	formName="station"+str(stationID)+"Form"
	if k!=len(stationList1)-1:
		nextStation=stationList1[k+1]
	else:
		nextStation=stationList1[0]
	nextID=getID(nextStation)
	nextStartTime=timeList[7*k]
	#成寿寺站是最末班车
	if k<25:
		nextEndTime=timeList[7*k+3]
	#巴沟站是最末班车
	else:
		nextEndTime=timeList[7*k+2]
	#把对应信息写到数据库的对应表格中
	reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(7)+")"
	dbConn.execute(reqStr)
	dbConn.commit()
#处理上行路线
for k in range(len(stationList2)):
	stationID=getID(stationList2[k])
	formName="station"+str(stationID)+"Form"
	nextStation=stationList2[k-1]
	nextID=getID(nextStation)
	nextStartTime=timeList[7*k+4]
	#不是车道沟站
	if k!=41:
		nextEndTime=timeList[7*k+6]
	#车道沟站
	else:
		nextEndTime=timeList[7*k+5]
	#把对应信息写到数据库的对应表格中
	reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(7)+")"
	dbConn.execute(reqStr)
	dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

#接下来是13号线，有半程车，奇怪的六栏格式...
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(8)
stationList=[]
timeList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList.append(j)
for k in range(len(stationList)):
	stationID=getID(stationList[k])
	formName="station"+str(stationID)+"Form"
	if k>0:
		#这表明这个站点存在前一站
		prevStation=stationList[k-1]
		prevID=getID(prevStation)
		prevStartTime=timeList[6*k]
		#不可以坐往回龙观站的末班车
		if k<8:
			prevEndTime=timeList[6*k+2]
		#可以坐往回龙观的末班车
		else:
			prevEndTime=timeList[6*k+5]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(8)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
	if k<len(stationList)-1:
		#这表明这个站点存在后一站
		nextStation=stationList[k+1]
		nextID=getID(nextStation)
		nextStartTime=timeList[6*k+1]
		#可以坐往霍营的末班车
		if k<8:
			nextEndTime=timeList[6*k+4]
		#不可以坐往霍营的末班车
		else:
			nextEndTime=timeList[6*k+3]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(8)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

#14号线有两个表格
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(9)
stationList1=[]
stationList2=[]
timeList1=[]
timeList2=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList1.append(j)
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList1.append(j)
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[1].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList2.append(j)
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[1].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList2.append(j)
#处理上半表格
for k in range(len(stationList1)):
	stationID=getID(stationList1[k])
	formName="station"+str(stationID)+"Form"
	if k>0:
		#这表明这个站点存在前一站
		prevStation=stationList1[k-1]
		prevID=getID(prevStation)
		prevStartTime=timeList1[5*k+2]
		#不可以坐半程车
		if k<3:
			prevEndTime=timeList1[5*k+3]
		#可以坐往回龙观的末班车
		else:
			prevEndTime=timeList1[5*k+4]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(9)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
	if k<len(stationList1)-1:
		#这表明这个站点存在后一站
		nextStation=stationList1[k+1]
		nextID=getID(nextStation)
		nextStartTime=timeList1[5*k]
		nextEndTime=timeList1[5*k+1]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(9)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
#处理下半表格，这个表格的格式和1号线类似
for k in range(len(stationList2)):
	stationID=getID(stationList2[k])
	formName="station"+str(stationID)+"Form"
	if k>0:
		#这表明这个站点存在前一站
		prevStation=stationList2[k-1]
		prevID=getID(prevStation)
		prevStartTime=timeList2[4*k+1]
		prevEndTime=timeList2[4*k+2]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(9)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
	if k<len(stationList2)-1:
		#这表明这个站点存在后一站
		nextStation=stationList2[k+1]
		nextID=getID(nextStation)
		nextStartTime=timeList2[4*k]
		nextEndTime=timeList2[4*k+1]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(9)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

'''
#15号线的特点是一个方向上有半程车
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(10)
stationList=[]
timeList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList.append(j)
for k in range(len(stationList)):
	stationID=getID(stationList[k])
	formName="station"+str(stationID)+"Form"
	if k>0:
		#这表明这个站点存在前一站
		prevStation=stationList[k-1]
		prevID=getID(prevStation)
		prevStartTime=timeList[5*k+3]
		prevEndTime=timeList[5*k+4]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(10)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
	if k<len(stationList)-1:
		#这表明这个站点存在后一站
		nextStation=stationList[k+1]
		nextID=getID(nextStation)
		nextStartTime=timeList[5*k]
		#可以坐往马泉营的末班车
		if k<8:
			nextEndTime=timeList[5*k+2]
		#不可以坐往马泉营的末班车
		else:
			nextEndTime=timeList[5*k+1]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(10)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

#昌平线的特点是首班车在前，末班车在后
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(12)
stationList=[]
timeList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("td")
for j in rawBS:
	j=str(j.string).strip()
	timeList.append(j)
for k in range(len(stationList)):
	stationID=getID(stationList[k])
	formName="station"+str(stationID)+"Form"
	if k>0:
		#这表明这个站点存在前一站
		prevStation=stationList[k-1]
		prevID=getID(prevStation)
		prevStartTime=timeList[5*k+1]
		prevEndTime=timeList[5*k+4]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(prevID)+", '"+prevStation+"', '"+prevStartTime+"', '"+prevEndTime+"', "+str(12)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
	if k<len(stationList)-1:
		#这表明这个站点存在后一站
		nextStation=stationList[k+1]
		nextID=getID(nextStation)
		nextStartTime=timeList[5*k]
		#可以坐往朱辛庄的末班车
		if k<9:
			nextEndTime=timeList[5*k+3]
		#不可以坐往马泉营的末班车
		else:
			nextEndTime=timeList[5*k+2]
		#把对应信息写到数据库的对应表格中
		reqStr="insert into '"+formName+"' (stationID, stationName, startTime, endTime, lineID) values("+str(nextID)+", '"+nextStation+"', '"+nextStartTime+"', '"+nextEndTime+"', "+str(12)+")"
		dbConn.execute(reqStr)
		dbConn.commit()
print("已经写好一条线路!")
dbConn.close()
'''

#最后修复一些bug
#定义一个函数来观察给定站名的地铁站情况
def displayStation(stationName):
	myID=getID(stationName)
	formName="station"+str(myID)+"Form"
	dbConn=sqlite3.connect('subwayInfo.db')
	myCursor=dbConn.execute("select * from '"+formName+"'")
	print(myCursor.fetchall())
	myCursor.close()
	dbConn.close()

#把7号线上的双井和垡头站去掉，这两站都不开
'''
dbConn=sqlite3.connect('subwayInfo.db')
myID=getID("双井")
formName="station"+str(myID)+"Form"
dbConn.execute("delete from '"+formName+"' where lineID=17")
dbConn.commit()
displayStation("双井")
displayStation("垡头")
myID=getID("垡头")
formName="station"+str(myID)+"Form"
dbConn.execute("delete from '"+formName+"' where lineID=17")
dbConn.commit()
displayStation("垡头")
dbConn.close()
'''

#相连函数
def letConnect(stationName1,stationName2,startStr1,startStr2):
	displayStation(stationName1)
	displayStation(stationName2)
	dbConn=sqlite3.connect('subwayInfo.db')
	myID1=getID(stationName1)
	myID2=getID(stationName2)
	formName1="station"+str(myID1)+"Form"
	formName2="station"+str(myID2)+"Form"
	reqStr="update '"+formName1+"' set stationID="+str(myID2)+", stationName='"+stationName2+"' where startTime='"+startStr1+"'"
	dbConn.execute(reqStr)
	dbConn.commit()
	reqStr="update '"+formName2+"' set stationID="+str(myID1)+", stationName='"+stationName1+"' where startTime='"+startStr2+"'"
	dbConn.execute(reqStr)
	dbConn.commit()
	displayStation(stationName1)
	displayStation(stationName2)

#让广渠门外和九龙山相连
#letConnect("广渠门外","九龙山","5:52","5:26")

#让欢乐谷景区和双合相连
#letConnect("欢乐谷景区","双合","6:07","5:12")

#处理16号线上农大南路站不开
def delStation(stationName, lineNum):
	displayStation(stationName)
	dbConn=sqlite3.connect('subwayInfo.db')
	myID=getID(stationName)
	formName="station"+str(myID)+"Form"
	dbConn.execute("delete from '"+formName+"' where lineID="+str(lineNum))
	dbConn.commit()
	displayStation(stationName)
	dbConn.close()

#delStation("农大南路",18)
#letConnect("西苑","马连洼","6:00","5:49")

#处理亦庄线上亦庄火车站不开
#delStation("亦庄火车站",13)

#删掉次渠到亦庄火车站的记录
'''
displayStation("次渠")
dbConn=sqlite3.connect('subwayInfo.db')
myID=getID("次渠")
formName="station"+str(myID)+"Form"
dbConn.execute("delete from '"+formName+"' where stationName='亦庄火车站'")
dbConn.commit()
displayStation("次渠")
'''

#这样一来我们终于录好了所有的首末班车时间！

#修正一下机场线的bug
#机场线是一个环线，而且回来时在某些站不停
'''
stationList=['东直门','三元桥','3号航站楼','2号航站楼']
for i in stationList:
	print(getID(i))
'''
#这个部分我用sqlite expert线下改掉
#注意根据爬虫的结果T3航站楼存储的时候写的是3号航站楼,T2也是如此，后面需要注意！

#现在写入distance的值，由于自己之前规划失误，现在考虑用distance表示两站间的时间间隔而非距离
#这个时间间隔由首末班车表进行计算

def getDistance(stationList, timeList,isCircle,lineID):
	#这个列表中stationList表示站名列表，timeList表示时间间隔列表,isCircle表示是否是环线
	#lineID表示线路号码
	if not isCircle and len(stationList)-len(timeList)!=1:
		print("wrong!")
		return False

	if isCircle and len(stationList)-len(timeList)!=0:
		print("wrong!")
		return False

	dbConn=sqlite3.connect('subwayInfo.db')
	for i in range(len(timeList)):
		stationName1=stationList[i]
		if isCircle and i==len(timeList)-1:
			stationName2=stationList[0]
		else:
			stationName2=stationList[i+1]
		stationID1=getID(stationName1)
		stationID2=getID(stationName2)
		formName1="station"+str(stationID1)+"Form"
		formName2="station"+str(stationID2)+"Form"
		reqStr="update '"+formName1+"' set distance="+str(timeList[i])+" where stationID="+str(stationID2)+" AND lineID="+str(lineID)
		dbConn.execute(reqStr)
		reqStr="update '"+formName2+"' set distance="+str(timeList[i])+" where stationID="+str(stationID1)+" AND lineID="+str(lineID)
		dbConn.execute(reqStr)
		dbConn.commit()
	dbConn.close()
	print("已经写好一条线路！")
	return True

#1号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(0)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[4,3,3,2,3,3,2,3,2,2,3,2,2,2,2,2,3,2,2,3,3,3]
a=getDistance(stationList, timeList,False,0)
'''

#2号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(1)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
stationList.remove("西直门")
stationList.append("西直门")
timeList=[2,3,2,3,2,2,3,2,3,2,3,1,2,3,3,2,2,3]
a=getDistance(stationList, timeList,True,1)
'''

#4号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(2)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
flag=0
for j in rawBS:
	j=str(j.string).strip()
	if flag%2==0:
		stationList.append(j)
	flag+=1
timeList=[2,3,3,2,2,2,2,2,3,6,3,1,2,2,3,2,3,2,1,2,2,2,3,2,2,3,2,3,1,2,2,3,2,1]
a=getDistance(stationList, timeList,False,2)
'''

#5号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(3)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[2,2,3,2,2,2,2,2,2,2,2,2,2,3,2,2,4,2,3,3,1,2]
a=getDistance(stationList, timeList,False,3)
'''

#6号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(4)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
stationList.remove("通运门")
stationList.remove("北运河东")
timeList=[2,3,2,3,2,3,2,3,4,2,3,2,3,2,3,3,2,3,3,3,3,4,4,3,2]
a=getDistance(stationList, timeList,False,4)
'''

#7号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(17)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
stationList.remove("双井")
stationList.remove("垡头")
timeList=[2,2,3,2,2,2,2,3,2,2,4,2,2,2,2,3,4,2]
a=getDistance(stationList, timeList,False,17)
'''

#8号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(5)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[3,3,3,3,3,2,3,4,4,2,3,2,2,2,3,2,2]
a=getDistance(stationList, timeList,False,5)
'''

#9号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(6)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[2,2,2,2,3,3,3,3,3,3,2,2]
a=getDistance(stationList, timeList,False,6)
'''

#10号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(7)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
flag=0
for j in rawBS:
	j=str(j.string).strip()
	if flag%2==0:
		if j!='None':
			stationList.append(j)
		else:
			stationList.append("惠新西街南口")
	flag+=1
timeList=[2,2,2,2,2,2,2,2,2,3,3,2,2,3,2,2,2,2,2,2,2,2,2,3,2,3,2,3,2,2,3,2,4,3,2,3,2,4,2,3,3,2,2,2]
a=getDistance(stationList, timeList,False,7)
'''

#13号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(8)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[4,3,2,6,4,5,2,3,6,3,7,3,3,2,2]
a=getDistance(stationList, timeList,False,8)
'''

#14号线第一个表格
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(9)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[1,5,3,3,3,1]
a=getDistance(stationList, timeList,False,9)
'''

#14号线第二个表格
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(9)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[1].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[3,2,3,2,3,4,4,3,3,2,3,3,2,4,2,2,3,2,2]
a=getDistance(stationList, timeList,False,9)
'''

#15号线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(10)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[3,2,4,5,3,3,4,5,3,3,3,3,3,3,2,3,2,3,2]
a=getDistance(stationList, timeList,False,10)
'''

#16号线
'''
stationList=['西苑','马连洼','西北旺','永丰南','永丰','屯佃','稻香湖路','温阳路','北安河']
timeList=[6,3,4,3,4,3,4,3]
a=getDistance(stationList, timeList,False,18)
'''

#八通线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(11)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[2,3,3,3,2,3,3,3,2,2,3,1]
a=getDistance(stationList, timeList,False,11)
'''

#昌平线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(12)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[2,4,3,3,3,5,3,3,4,3,5]
a=getDistance(stationList, timeList,False,12)
'''

#亦庄线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(13)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
stationList.remove("亦庄火车站")
timeList=[3,2,4,2,2,3,2,2,4,3,2,2]
a=getDistance(stationList, timeList,False,13)
'''

#房山线
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
searchID="sub"+str(15)
stationList=[]
rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
for j in rawBS:
	j=str(j.string).strip()
	stationList.append(j)
timeList=[2,6,5,3,3,3,2,3,2,2]
a=getDistance(stationList, timeList,False,15)
'''

#机场线手动完成
'''
stationList=['东直门','三元桥','3号航站楼','2号航站楼']
for i in stationList:
	print(getID(i))
'''

#这里检测一下是否每个表格中站名和id是正确的
'''
dbConn=sqlite3.connect('subwayInfo.db')
for i in range(294):
	formName="station"+str(i)+"Form"
	myCursor=dbConn.execute("select * from '"+formName+"'")
	myList=myCursor.fetchall()
	if len(myList)!=0:
		for j in myList:
			if j[0]!=getID(j[1]):
				print(formName+"里有错误发生！")
	myCursor.close()
print("都没有错误！")
dbConn.close()
'''

#出于网页的需要，这里还需要收集一下各个地铁站的信息
'''
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
#排除双栏的4号线和10号线，排除两个表格的14号线
myList=[0,1,3,4,5,6,8,10,11,12,13,15,16]
for i in myList:
	#创建地铁线表格，命名方式为line+id+Form，如line0Form
	formName="line"+str(i)+"Form"
	dbConn.execute("create table '"+formName+"' (stationID int, stationName varchar)")
	dbConn.commit()
	searchID="sub"+str(i)
	rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
	for j in rawBS:
		j=str(j.string).strip()
		#把站名添加到表格中
		dbConn.execute("insert into '"+formName+"' (stationID, stationName) values("+str(getID(j))+", '"+j+"')")
		dbConn.commit()
	print("已经写好一条线路！")
dbConn.close()
'''

'''
#再写双栏的4号线和10号线
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
#myList=[2,7]
#10号线上的惠新西街南口再次bug
myList=[7]
for i in myList:
	#创建地铁线表格，命名方式为line+id+Form，如line0Form
	formName="line"+str(i)+"Form"
	dbConn.execute("create table '"+formName+"' (stationID int, stationName varchar)")
	dbConn.commit()
	searchID="sub"+str(i)
	rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
	flag=0
	for j in rawBS:
		if flag%2==0:
			j=str(j.string).strip()
			if j=="None":
				j="惠新西街南口"
			#把站名添加到表格中
			dbConn.execute("insert into '"+formName+"' (stationID, stationName) values("+str(getID(j))+", '"+j+"')")
			dbConn.commit()
		flag+=1
	print("已经写好一条线路！")
dbConn.close()
'''

'''
#最后处理有两个表格的14号线
dbConn=sqlite3.connect('subwayInfo.db')
oBS=BS(strData,"html.parser")
myList=[9]
for i in myList:
	#创建地铁线表格，命名方式为line+id+Form，如line0Form
	formName="line"+str(i)+"Form"
	dbConn.execute("create table '"+formName+"' (stationID int, stationName varchar)")
	dbConn.commit()
	searchID="sub"+str(i)
	rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[0].find_all("th")
	for j in rawBS:
		j=str(j.string).strip()
		#把站名添加到表格中
		dbConn.execute("insert into '"+formName+"' (stationID, stationName) values("+str(getID(j))+", '"+j+"')")
		dbConn.commit()
	rawBS=oBS.find_all("",{"id":searchID})[0].find_all("tbody")[1].find_all("th")
	for j in rawBS:
		j=str(j.string).strip()
		#把站名添加到表格中
		dbConn.execute("insert into '"+formName+"' (stationID, stationName) values("+str(getID(j))+", '"+j+"')")
		dbConn.commit()
print("已经写好一条线路！")
dbConn.close()
'''

#所有数据库写入工作完成！
#eof