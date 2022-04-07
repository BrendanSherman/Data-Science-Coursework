#Brendan Sherman
#Homework 5 Question 4: Nonlinear feature extraction
#Writeup contains all output/explanations of code

import numpy as np 
import random
from sklearn.datasets import fetch_openml
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from q2_regression import impute

#Q4a: Transform dataset using quadratic features, expanded on in writeup
def q4a(ds):
	impute(ds) #Handle missing data values
	poly = PolynomialFeatures(degree=2)
	transformed = poly.fit_transform(ds.data)
	
	return (transformed, ds.data.shape, transformed.shape)

#Q4b: Train linear regression model on transformed dataset
def q4b(ds, ds_t):
	model = LinearRegression(fit_intercept=True)
	model.fit(ds_t, ds.target) #using entire dataset
	r_sq = model.score(ds_t, ds.target)

	#split dataset into training, test portions
	indices = list(range(0, ds.data.shape[0])) 
	r_sqs = np.empty((0,))
	for i in range(100):
		random.shuffle(indices)
		training_indices = indices[0:202]
		test_indices = indices[202:]

		training_data = ds_t[training_indices, :]
		test_data = ds_t[test_indices, :]
		training_targets = ds.target[training_indices]
		test_targets = ds.target[test_indices]

		training_model = LinearRegression().fit(training_data, training_targets)
		score = training_model.score(test_data, test_targets)
		r_sqs = np.append(r_sqs, score)
	
	return (r_sq, r_sqs)

def main():
	ds = fetch_openml(name="cholesterol", version=1)
	results = q4a(ds)
	print("Size of original non-target data matrix: " + str(results[1]))
	print("Size of transformed non-target data matrix: " + str(results[2]))
	results = q4b(ds, results[0]) 
	print("r-squared (for transformed dataset): " + str(round(results[0], 2)))
	print("mean r-squared value on test portion (across 100 trials): " 
		+ str(round(np.mean(results[1]), 2)))


if __name__ == '__main__':
	main()