#Author: illusion
#Date: 2017/9/18
#Description: code for assignment2 question4

import numpy as np
import csv
import pandas as pd
from sklearn import datasets, linear_model

#OLS regression function
#Some code is from http://python.jobbole.com/81215/
def ols(x_par,y_par):
	regr=linear_model.LinearRegression()
	regr.fit(x_par,y_par)
	predictions={}
	predictions['intercept']=regr.intercept_
	predictions['coefficient']=regr.coef_
	return predictions

#Read the csv file
with open('Industry8_data_withFactors.csv','r') as f:
	content=csv.reader(f)
	
	#extract all the excess return value
	i=0
	returnList=[]
	for row in content:
		tempList=[]
		if i>=1 and i<=510:
			for j in range(13,24):
				tempList.append(float(row[j]))
			returnList.append(tempList)
		i+=1
	
	#transpose it
	dataMatrix=np.mat(returnList).T

	#begin OLS Regression
	x1_par=dataMatrix[0].getA().flatten()
	x2_par=dataMatrix[1].getA().flatten()
	x3_par=dataMatrix[2].getA().flatten()
	x_par=np.column_stack((x1_par,x2_par,x3_par))
	for i in range(3,11):
		y_temp=dataMatrix[i].tolist()
		y_par=y_temp[0]
		print(ols(x_par,y_par))