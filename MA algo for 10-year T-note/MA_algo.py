#Author: illusion
#Date: 2017/10/4
#Description: code file for assignment 6

import csv
import numpy as np

#Trading signal generator
#Input: shortList: short MA; longList: long MA
#Output: buyList: dates to buy, sellList: dates to sell

def signalGenerator(shortList,longList):
	listNum=len(shortList)
	buyList=[]
	sellList=[]
	for i in range(1,listNum):
		if shortList[i-1]<longList[i-1] and shortList[i]>=longList[i] and shortList[i]>shortList[i-1] and longList[i]>longList[i-1]:
			buyList.append(i)
		elif shortList[i-1]>=longList[i-1] and shortList[i]<longList[i] and shortList[i]<shortList[i-1] and longList[i]<longList[i-1]:
			sellList.append(i)
	return (buyList,sellList)

#Value list generator
#Input: buyList, sellList: buy and sell signal list; priceList: price of the asset
#Output: valueList: a list of portfolio value (cash+asset)

def valueGenerator(buyList,sellList,priceList):
	myPosition=0
	totalDay=len(priceList)
	#Because there is no trading in the first day, we have no asset and cash
	assetList=[0]
	#Assume we have the money to buy one share
	cashList=[priceList[0]]
	valueList=[priceList[0]]
	for i in range(1,totalDay):

		#Check whether we need to trade today
		#Note we observe the trading signal at the end of a trading day
		#Therefore we can only execute corresponding trading in the next day

		if (i-1) in buyList:
			cashList.append(cashList[i-1]-priceList[i])
			myPosition+=1

		elif (i-1) in sellList:
			cashList.append(cashList[i-1]+priceList[i])
			myPosition-=1

		else:
			cashList.append(cashList[i-1])

		#assetList is rather easy to compute, just position*price
		assetList.append(myPosition*priceList[i])

		#valueList is the sum of assetList and cashList
		valueList.append(assetList[i]+cashList[i])
	
	return valueList

#Use this function to judge the performance of a strategy
#Input: valueList of the strategy as time passes
#Output: No output

def performance(valueList):
 
    #Calculate the number of days in your strategy
    N=len(valueList)
    totalreturnrate=valueList[-1]/valueList[0]-1
    print ("Total return rate=",totalreturnrate)
    annualizedrate=(valueList[-1]/valueList[0]-1)/N*252.0
    print ("Annualized rate of return=",annualizedrate)
    dailyreturn=[]
    for i in range(N-1):
        dailyreturn.append(valueList[i+1]/valueList[i]-1)
    dailyreturn=np.array(dailyreturn)
    volatility=dailyreturn.std()*np.sqrt(252)
    print ("Annualized volatility=",volatility)
    sharperatio=annualizedrate/volatility
    print ("Sharpe ratio=",sharperatio)
    tempratio=[]
    for i in range(1,N):
        tempratio.append(1-valueList[i]/max(valueList[0:i]))
    maxdrawdown=max(tempratio)
    print ("Max drawdown=",maxdrawdown)
    return 0

#Read the csv file
with open('10Y_T_Note.csv','r') as f:
	content=csv.reader(f,delimiter="\t")

	#We only care about the date and the price column
	i=0
	priceList=[]
	for row in content:
		if i>=1 and i<=1993:
			priceList.append(float(row[1]))
		i+=1
	
	#Now, we need to reverse the lists to make them order as time passes
	priceList.reverse()

	#Now, construct the moving average for 30 days
	#In order to make comparison, we will only start from the 30th element
	num=len(priceList)
	ma30=[]
	for i in range(29,num):
		ma30.append(np.mean(priceList[i-29:i+1]))
	
	#Construct the moving average for 10 days
	#Still, in order to make comparison, we will only start from the 30th element
	ma10=[]
	for i in range(29,num):
		ma10.append(np.mean(priceList[i-9:i+1]))

	#Construct the moving average for 5 days
	#Still, in order to make comparison, we will only start from the 30th element
	ma5=[]
	for i in range(29,num):
		ma5.append(np.mean(priceList[i-4:i+1]))
	
	#In order for me not to make mistake in the future, 
	#I will delete all price data which have no moving average available
	priceList=priceList[29:]
	
	#Generate all the trading signal
	(buy5_10,sell5_10)=signalGenerator(ma5,ma10)
	(buy5_30,sell5_30)=signalGenerator(ma5,ma30)
	(buy10_30,sell10_30)=signalGenerator(ma10,ma30)
	buys_l=set(buy5_10)|set(buy5_30)|set(buy10_30)
	sells_l=set(sell5_10)|set(sell5_30)|set(sell10_30)
	
	#Generate all the value list
	value5_10=valueGenerator(buy5_10,sell5_10,priceList)
	value5_30=valueGenerator(buy5_30,sell5_30,priceList)
	value10_30=valueGenerator(buy10_30,sell10_30,priceList)
	values_l=valueGenerator(buys_l,sells_l,priceList)
	
	#We find that only value5_10 is making money!
	#Check the performance of 5 - 10 MA algo
	performance(value5_10)
