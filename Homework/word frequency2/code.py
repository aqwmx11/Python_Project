# Author: illusion
# Date: March 16, 2017
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
	rawList[-1]=rawList[-1][:-1] #Delete the "\n" in the end
	value=tuple(rawList[2:])
	myDict[key]=value

def printInfo(character):
	if character in myDict:
		print("The information of ",character," is ",myDict[character])
	else:
		print("No information for this character.")

printInfo("瑰")
		
# Delete the single character in the dict above
newDict=dict(filter(lambda x:len(x[0])>=2, myDict.items()))

# Create a new dict to store the single character
charDict={}
for i in newDict:
	tmpList=list(i)
	for j in tmpList:
		if j not in charDict:
			charDict[j]=1
		else:
			charDict[j]+=1

# Rank according to the value reversly
charList=[]
for (key,value) in charDict.items():
	charList.append((key,int(value))) # Default transformation will make value a string
charList.sort(key=lambda x:x[1], reverse=True)
print (charList[:10])

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
print (wordList[:10])

# Create a new dict to store the doule-character words
doubleDict={}
for i in newDict:
	tmplist=list(i)
	for j in range(0,len(tmplist)-1):
		doubleword=tmplist[j]+tmplist[j+1]
		if doubleword not in doubleDict:
			doubleDict[doubleword]=i
		else:
			doubleDict[doubleword]+=(' '+i)

# Print the double-character words according to the required format
# Here I will print 20 examples
i=1
for (key,value) in doubleDict.items():
	print(key,"在如下词中出现:",value)
	i+=1
	if i>20:
		break

#eof