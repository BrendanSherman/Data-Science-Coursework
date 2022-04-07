#Homework 6
#Writeup contains explanation of all code
#Author: Brendan Sherman 

import numpy as np 
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

#Instantiate imputer to replace missing values within given dataset
def impute(df):
	df.replace('?', np.nan, inplace = True) #replace string, allowing mean calculation
	imp = SimpleImputer(missing_values = np.nan) 
	idf = pd.DataFrame(imp.fit_transform(df)) 
	idf.columns = df.columns 
	idf.index = df.index
	return idf

#Standardize given data 
def standardize(df):
	scaler = StandardScaler()
	s_data = pd.DataFrame(scaler.fit_transform(df)) 
	s_data.columns = df.columns
	s_data.index = df.index
	return s_data

#Preprocess data, train and evaluate logistic regression model 
def q1a(df):
	#Preprocessing
	idf = impute(df) #Handle missing data
	target = idf["class"]
	data = idf.loc[:, "lepton_pT":"m_wwbb"]
	s_data = standardize(data)
	
	#Training logistic model on data
	model = LogisticRegression()
	model.fit(s_data, target)

	#Returns mean accuracy of prediction across examples
	return model.score(s_data, target)

#Use cross validation to estimate generalization accuracy
def q1b(df):
	#Preprocessing
	idf = impute(df) 
	target = idf["class"]
	data = idf.loc[:, "lepton_pT":"m_wwbb"]
	s_data = standardize(data)

	#Use cross validation w/ 10 folds to evaluate logistic model
	model = LogisticRegression()
	scores = cross_val_score(model, s_data, target, cv=10)
	mean = np.mean(scores)
	std = np.std(scores, ddof=1)

	return [scores, mean, std]

def main():
	df = pd.read_csv('higgs.csv')
	answers = q1b(df)

	print("Accuracy values: ", end = "")
	for i in answers[0]:
		print(str(round(i, 3)), end = " ")
	print("\n" + "Mean: " + str(round(answers[1], 3)))
	print("Standard Deviation: " + str(round(answers[2], 3)))
	
if __name__ == "__main__":
	main()