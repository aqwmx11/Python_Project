# coding: utf-8
# Author: illusion
# Date: March 14, 2017
# Discription: code for the last question

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

# Switch content from string to a list
contentList=list(contentFromFile)

# Count the frequency of each character using dict 
wordDict={}
for i in contentList:
	if is_chinese(i):
		if i not in wordDict:
			wordDict[i]=1
		else:
			wordDict[i]+=1

# Rank according to the value reversly
wordDict=sorted(wordDict.items(),key=lambda x:x[1], reverse=True)

# Print our result for the words
print ("Here are some examples of our result for the Chinese characters:")
print (wordDict[:10])

# Write the result to an excel sheet
import xlwt
f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
for i in range(len(wordDict)):
	sheet1.write(i,0,wordDict[i][0])
	sheet1.write(i,1,wordDict[i][1])
f.save("frequency.xls")
print ("Excel sheet successfully established.")

