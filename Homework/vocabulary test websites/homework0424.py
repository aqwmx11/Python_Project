#author:illusion
#date:2017/04/24
#description:python code file

from flask import Flask,render_template,request
import pickle
import random

webApp=Flask(__name__,static_url_path="",static_folder="")

# This html is used to input english words and their Chinese meaning
@ webApp.route("/InputWord",methods=["GET","POST"])
def submit():
	submitInfo=None

	# Get the data from html file
	if request.method=="POST":
		eng=request.form["engWord"]
		chn=request.form["chnWord"]
		
		# Use pickle to read old english and chinese words and make them a dict
		record=open('data.pkl','rb')
		oldDict=pickle.load(record)
		record.close()

		if eng in oldDict:
			submitInfo="该单词已经存在，您的修改已成功."
		else:
			submitInfo="已成功向词库中添加该单词"

		# Write the new english and chinese words to the data file
		oldDict[eng]=chn
		record=open('data.pkl','wb')
		pickle.dump(oldDict,record)
		record.close()

	return render_template("InputWord.html",submitInfo=submitInfo)

# This html is used to show all the words and their meanings in the database
@ webApp.route("/OutputWord")
def showWord():

	# Use pickle to read old english and chinese words and make them a dict
	record=open('data.pkl','rb')
	oldDict=pickle.load(record)
	record.close()

	# Print all the english and chinese words
	content=""
	for (key,val) in oldDict.items():
		content+=key+","+val+"\n"

	return content

# This html is used to randomly choose 20 words from the database
@ webApp.route("/RandomSelect")
def twentyWords():
	
	# Use pickle to read old english and chinese words and make them a dict
	record=open('data.pkl','rb')
	oldDict=pickle.load(record)
	record.close()

	# Randomly select 20 words from the Dict
	oldList=list(oldDict)
	randomList=random.sample(oldList,20)
	
	# Print the result on the html page
	content=""
	for i in randomList:
		content+=i+","+oldDict[i]+","
	
	return content

# This html is used to realize the exam function described in the homework
@ webApp.route("/myExam")
def exam():
	return webApp.send_static_file("exam.html")


if __name__=="__main__":
	# Adding "threaded=True" significantly boosts the speed of the program on my laptop
	webApp.run(host='0.0.0.0',port=80,debug=True,threaded=True)

#eof