# coding: utf-8
# Author: illusion
# Date: March 9, 2017
# Discription: code file

# Read the text file
readingFromFile=open('50万人名名单.txt','r',encoding="utf-8",errors="ignore")
contentFromFile=readingFromFile.read()
readingFromFile.close()
nameList=contentFromFile.split("\n")

# Sort the name list according to their length
nameList.sort(key=lambda x:len(x))
del nameList[0] # Remove the first element, which is a blank

# Delete names with length more than 4
# Because we already sort the list by their length, we only need to find the first element to delete
first_index=0
while True:
	if len(nameList[first_index])>4:
		break
	first_index+=1
del nameList[first_index:]

# Create a newlist to store the last name
lastnameList=[]
for i in nameList:
	lastnameList.append(i[0])

# Count the frequency of each last name using dict 
lastnameDict={}
for i in lastnameList:
	if i not in lastnameDict:
		lastnameDict[i]=1
	else:
		lastnameDict[i]+=1

# Rank according to the value reversly
lastnameDict=sorted(lastnameDict.items(),key=lambda x:x[1], reverse=True)

# Print our result for the last name
print ("Here are some examples of our result for the last name:")
print (lastnameDict[:9])

# Create a newlist to store the first name
firstnameList=[]
for i in nameList:
	firstname=list(i[1:])
	firstnameList+=firstname

# Count the frequency of each first name using dict 
firstnameDict={}
for i in firstnameList:
	if i not in firstnameDict:
		firstnameDict[i]=1
	else:
		firstnameDict[i]+=1

# Rank according to the value reversly
firstnameDict=sorted(firstnameDict.items(),key=lambda x:x[1], reverse=True)

# Print our result for the first name
print ("Here are some examples of our result for the first name:")
print (firstnameDict[:9])

# Create a newlist to store the repeated characters
# Here, I only consider the simplist situation like 王丽丽
# For example, 欧阳阳光 is hard to judge even for a person because you cannot tell if the first name is 欧 or 欧阳
repeatList=[]
for i in nameList:
	if i[-1]==i[-2]:
		repeatwords=i[-1]+i[-2]
		repeatList.append(repeatwords)

# Count the frequency of each repeated characters using dict 
repeatDict={}
for i in repeatList:
	if i not in repeatDict:
		repeatDict[i]=1
	else:
		repeatDict[i]+=1

# Rank according to the value reversly
repeatDict=sorted(repeatDict.items(),key=lambda x:x[1], reverse=True)

# Print our result for the repeated words
print ("Here are some examples of our result for the repeated words:")
print (repeatDict[:9])

#eof