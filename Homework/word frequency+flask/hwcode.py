# Author: illusion
# Date: March 30, 2017
# Discription: code file

# Read the txt file
readingFromFile=open('CorpusWordlist.txt','r',encoding='utf-8',errors='ignore')
contentFromFile=readingFromFile.readlines()
readingFromFile.close()

# Delete the first element
del contentFromFile[0]

# Create a dict based on the list above
myDict={}
for i in contentFromFile:
    rawList=i.split(',')
    key=rawList[1]
    rawList[-1]=rawList[-1][:-1]
    value=tuple(rawList[2:])
    myDict[key]=value
            
# Delete the single character in the dict above
newDict=dict(filter(lambda x:len(x[0])>=2, myDict.items()))

# Create a new dict to store the single character
wordDict={}
for i in newDict:
    frequency=list(newDict[i])[0]
    tmpList=list(i)
    for j in tmpList:
            if j not in wordDict:
                    wordDict[j]=frequency
            else:
                    wordDict[j]+=frequency

# Rank according to the value reversly
wordList=[]
for (key,value) in wordDict.items():
    wordList.append((key,int(value))) # Default transformation will make value a string
wordList.sort(key=lambda x:x[1], reverse=True)

from flask import Flask
app=Flask(__name__,static_url_path="",static_folder="")

@app.route("/")
def first():
    # Print the first 100 words
    content=""
    for i in range(100):
        content+=str(wordList[i])+" "
    return content

@app.route("/check/<char>")
def printInfo(char):
	if char in myDict:
		return "该汉字的出现次数、频率百分比和累计频率百分比分别为"+str(myDict[char])
	else:
		return "没有该汉字的使用信息"

@app.route("/info")
def charSearch():
	return app.send_static_file("charSearch.html")

if __name__=="__main__":
	app.run(host='0.0.0.0',port=80,debug=True)

#eof
