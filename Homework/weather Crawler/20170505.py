#Author: illusion
#Date: 2017/05/05
#Description: Restoring the link for each city

from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pickle
import sys

#Fetch the html from internet
dataFromWeb=request.urlopen("http://www.weather.com.cn/forecast/")
strData=dataFromWeb.read().decode("utf-8")

#Use beautiful soup to focus a bit more
oBS=BS(strData,"html.parser")
#Notice that Chinese city have id from maptabbox01-maptabbox07
linkDict={}
for i in range(1,8):
	searchID="maptabbox0"+str(i)
	#Find all the id in the searchList
	rawBS=oBS.find_all("",{"id":searchID})
	tempBS=rawBS[0].find_all("a")
	for ele in tempBS:
		linkDict[ele.string]=ele.attrs["href"]
#Now, we successfully store all the city and its corresponding link into our dict

#In order to save time, we use pickle to save our dict into a pkl
#Need to reset the recursion limit to avoid the potential bug here  
sys.setrecursionlimit(1000000)
op=open('data.pkl','wb')
pickle.dump(linkDict,op)
op.close()
