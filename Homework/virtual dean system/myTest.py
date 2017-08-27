#Author: illusion
#Date: 2017/05/19
#Description: test file for some functions in flask

# you don't need to run this file

from flask import Flask, redirect
webApp=Flask(__name__,static_url_path="",static_folder="")

@webApp.route("/")
def root():
	return redirect("/hello")

@webApp.route("/hello")
def hello():
	return "hello world!"

if __name__=="__main__":
	# Adding "threaded=True" significantly boosts the speed of the program on my laptop
	webApp.run(host='0.0.0.0',port=80,debug=True,threaded=True)

#eof