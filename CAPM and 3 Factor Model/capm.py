#Author: illusion
#Date: 2017/9/18
#Description: code for assignment2 question3

import numpy as np
import csv
import pandas as pd
from sklearn import datasets, linear_model

#OLS regression function
#Some code is from http://python.jobbole.com/81215/
def ols(x_par,y_par):
	regr=linear_model.LinearRegression()
	regr.fit(x_par.reshape(-1,1),y_par)
	predictions={}
	predictions['intercept']=regr.intercept_
	predictions['coefficient']=regr.coef_
	return predictions

#Read the csv file
with open('Industry8_data_original.csv','r') as f:
	content=csv.reader(f)
	
	#extract all the excess return value
	i=0
	returnList=[]
	for row in content:
		tempList=[]
		if i>=1 and i<=510:
			for j in range(13,22):
				tempList.append(float(row[j]))
			returnList.append(tempList)
		i+=1
	
	#transpose it
	dataMatrix=np.mat(returnList).T

	#begin OLS Regression
	x_par=dataMatrix[0].getA()
	for i in range(1,9):
		y_temp=dataMatrix[i].tolist()
		y_par=y_temp[0]
		print(ols(x_par,y_par))

