# Author: illusion
# Date: March 20, 2017
# Discription: code file for 红楼梦

# A small function to tell whether it is a Chinese character
# Code source: http://www.cnblogs.com/mfryf/p/4553684.html
def is_chinese(uchar):
	if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
		return True
	else:
		return False

# Read the text file
readingFromFile=open('红楼梦.txt','r',encoding="utf-8",errors="ignore")
contentFromFile=readingFromFile.read()
readingFromFile.close()

# Make all the Chinese character to a list
characterList=[]
for i in contentFromFile:
	if is_chinese(i):
		characterList.append(i)

# Create a new dict to store the doule-character words
doubleDict={}
for i in range(len(characterList)-1):
	current_word=characterList[i]+characterList[i+1]
	if current_word not in doubleDict:
		doubleDict[current_word]=1
	else:
		doubleDict[current_word]+=1

# Rank according to the value reversly
doubleList=[]
for (key,value) in doubleDict.items():
	doubleList.append((key,int(value))) # Default transformation will make value a string
doubleList.sort(key=lambda x:x[1], reverse=True)

# Write the result to an excel sheet
import xlwt
f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
for i in range(200): # In order to delete some that are not words, I print 200 words to select top 100
	sheet1.write(i,0,doubleList[i][0])
f.save("frequency.xls")
print ("Excel sheet successfully established.")

#eof
