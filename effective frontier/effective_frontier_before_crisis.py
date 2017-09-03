#Author: illusion
#Date: 2017/9/2
#Description: code file for assignment 1-3-1

import numpy as np
import csv
import matplotlib.pyplot as plt

#Read the csv file
with open('Industry8_data_original.csv','r') as f:
	content=csv.reader(f)
	
	#extract all the excess return value
	i=0
	returnList=[]
	for row in content:
		tempList=[]
		if i>=1 and i<=396:
			for j in range(14,22):
				tempList.append(float(row[j]))
			returnList.append(tempList)
		i+=1
	
	#transpose it
	dataMatrix=np.mat(returnList).T
	
	#create the return vector
	tempList=[]
	for i in range(0,8):
		tempList.append(np.mean(dataMatrix[i])*12+0.01)
	muMatrix=np.mat(tempList).T
	
	#create the variance matrix
	varMatrix=np.mat(np.cov(dataMatrix,bias=1)*12)
	#calculate the reverse of the variance matrix to save time
	invarMatrix=varMatrix.I
	
	#create the "1" matrix
	oneMatrix=np.mat([[1],[1],[1],[1],[1],[1],[1],[1]])
	#calculate the transpose of it to save time
	troneMatrix=oneMatrix.T
	
	#create the omega1 and omegaR matrix
	omega1=invarMatrix*muMatrix/float(troneMatrix*invarMatrix*muMatrix)
	omegaR=invarMatrix*oneMatrix/float(troneMatrix*invarMatrix*oneMatrix)

	#calculate the mean of omega1 and omegaR
	mu1=float(omega1.T*muMatrix)
	muR=float(omegaR.T*muMatrix)
	
	muList=[]
	stdList=[]
	bestSharpe=0
	bestStd=0
	bestOmega=np.mat([[0],[0],[0],[0],[0],[0],[0],[1]])
	bestMu=0

	for i in range(1,501):
		mu=0+float(i)/1000
		muList.append(mu)
		alpha=(mu-mu1)/(muR-mu1)
		omegaStar=alpha*omegaR+(1-alpha)*omega1
		varStar=float(0.5*omegaStar.T*varMatrix*omegaStar)
		stdStar=np.sqrt(varStar)
		stdList.append(stdStar)

		sharpeStar=(mu-0.01)/stdStar
		if sharpeStar>bestSharpe:
			bestSharpe=sharpeStar
			bestOmega=omegaStar
			bestStd=stdStar
			bestMu=mu
	
	tanX=[0]
	tanX.append(bestStd)
	tanY=[0.01]
	tanY.append(bestMu)
	plt.plot(stdList,muList)
	plt.plot(tanX,tanY)
	plt.axis([0, 0.5, 0.01, 0.5])
	plt.show()

	print(bestSharpe)
	print(bestOmega)
	


