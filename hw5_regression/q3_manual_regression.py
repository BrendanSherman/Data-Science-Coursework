#Brendan Sherman
#Homework 5 Question 3: Linear regression model (manual)
#Writeup contains all output/explanations of code

import numpy as np 
from sklearn.datasets import fetch_openml
from sklearn.linear_model import LinearRegression
from q2_regression import q2a, impute

#Q3: Compute linear regression fit from q2, manually doing matrix calculations 
def q3(ds):
	#Instantiate imputer to replace missing values within dataset
	impute(ds)

	#Preprocessing: add column of 1s to dataset (for constant term)
	attributes = np.empty((ds.data.shape[0], ds.data.shape[1]+1))
	attributes[:, 0] = 1
	attributes[:, 1:] = ds.data

	#Determining coefficient vector (using normal equations)
	c = np.empty((ds.data.shape[1]+1, 1))
	x_t = np.transpose(attributes) 
	c = np.linalg.pinv(x_t.dot(attributes)) #psuedoinverse
	c = c.dot(x_t).dot(ds.target) #normal equations, minimize coefs wrt MSE 

	#Accessing correlation, intercept values from problem 2
	prev = q2a(ds)
	c_prev = prev[2]
	c_prev = np.insert(c_prev, 0, prev[3])

	return [c, c_prev, c-c_prev]

def main():
	ds = fetch_openml(name="cholesterol", version=1)
	result = q3(ds)
	
	print("Coefficient Vector (manually computed): ")
	print(result[0])
	print("Coefficient Vector (using SKL): " )
	print(result[1])
	print("Difference between vectors (element-wise): ")
	print(result[2])

if __name__ == "__main__":
	main()