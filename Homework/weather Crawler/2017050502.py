#Author: illusion
#Date: 2017/05/05
#Description: Data analysis and web page

import pickle
from urllib import request
from bs4 import BeautifulSoup as BS
from flask import Flask 

# Use pickle to read city name and their corresponding links
record=open('data.pkl','rb')
linkDict=pickle.load(record)
record.close()

webApp=Flask(__name__,static_url_path="",static_folder="")

# Make a html to show weather condition for whole cities
# According to my laptop, this condition takes about a minute
@webApp.route("/temp")
def wholeCity():
	content="数据排列顺序：城市 早间气温 晚间气温 早间天气 晚间天气"+"<br>"
	i=0
	for (key,val) in linkDict.items():
		# Use Beautiful soup to find min and max temp, mor. and eve. weather
		dataFromWeb=request.urlopen(val)
		strData=dataFromWeb.read().decode("utf-8")
		oBS=BS(strData,"html.parser")

		# Find min and max temp
		rawBS=oBS.find_all("",{"class":["tem"]})
		maxTemp=rawBS[0].get_text()
		minTemp=rawBS[1].get_text()

		# Find mor. and eve. weather
		raw2BS=oBS.find_all("",{"class":["wea"]})
		morWea=raw2BS[0].string
		eveWea=raw2BS[1].string

		content+=key+' '+minTemp+' '+maxTemp+' '+morWea+' '+eveWea+' '
		# Jump lines every two cities seems the best
		if i%2==1:
			content+="<br>"
		i+=1
	return content

# Make a html to show weather condition for whole cities
# In this part, we will add the automatic refresh function
@webApp.route("/")
def root():
	return webApp.send_static_file("whole.html")

if __name__=="__main__":
	# Adding "threaded=True" significantly boosts the speed of the program on my laptop
	webApp.run(host='0.0.0.0',port=80,debug=True,threaded=True)

#eof
