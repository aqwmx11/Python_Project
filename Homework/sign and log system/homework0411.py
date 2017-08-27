#author:illusion
#date:2017/04/11
#description:python code file

from flask import Flask,render_template,request
import pickle

webApp=Flask(__name__,static_url_path="",static_folder="")
@ webApp.route("/signup",methods=["GET","POST"])
def signUp():
	signUpInfo=None

	# Get the data from html file
	if request.method=="POST":
		newUserName=request.form["newusername"]
		newPassword=request.form["newpassword"]
		newPassword2=request.form["newpassword2"]

		# Use pickle to read old username and password and make them a dict
		record=open('data.pkl','rb')
		oldDict=pickle.load(record)
		record.close()

		if newPassword!=newPassword2:
			signUpInfo="对不起，您输入的两次密码不相同，请重新输入."
		elif newUserName in oldDict:
			signUpInfo="对不起，您选择的用户名已被注册，请重新输入或登录."
		else:
			signUpInfo="恭喜您，注册成功！"

			# Write the new username and password to the data file
			oldDict[newUserName]=newPassword
			record=open('data.pkl','wb')
			pickle.dump(oldDict,record)
			record.close()

	return render_template("signUp.html",signUpInfo=signUpInfo)

@ webApp.route("/login",methods=["GET","POST"])
def logIn():
	logInInfo=None

	# Get the data from html file
	if request.method=="POST":
		oldUserName=request.form["oldusername"]
		oldPassword=request.form["oldpassword"]

		# Use pickle to read old username and password and make them a dict
		record=open('data.pkl','rb')
		oldDict=pickle.load(record)
		record.close()

		if oldUserName not in oldDict:
			logInInfo="对不起，该用户名没有被注册过，请重新输入或注册."
		elif oldDict[oldUserName] != oldPassword:
			logInInfo="对不起，密码输入错误，请重新输入."
		else:
			logInInfo="恭喜您，登陆成功！"


	return render_template("logIn.html",logInInfo=logInInfo)

if __name__=="__main__":
	# Adding "threaded=True" significantly boosts the speed of the program on my laptop
	webApp.run(host='0.0.0.0',port=80,debug=True,threaded=True)

#eof