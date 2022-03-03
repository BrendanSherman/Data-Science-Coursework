#Brendan Sherman
#Homework 5 Question 2: Machine learning linear regression model
#Writeup contains all output/explanations of code

import numpy as np 
import random
from sklearn.datasets import fetch_openml
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression

#Filters dataset, trains and evaluates linear regression model
def q2a(ds):	
	#Instantiate imputer to replace missing values within dataset
	imp = SimpleImputer(missing_values = np.nan, strategy="mean")
	imp = imp.fit(ds.data) 
	ds.data = imp.transform(ds.data)

	#Fit a linear regression model to the data, using actual target values 
	model = LinearRegression(fit_intercept=True).fit(ds.data, ds.target) 

	#Evaluate model performance by "goodness of fit"
	r_sq = model.score(ds.data, ds.target)

	#Evaluate model performance by % of exactly correct predictions
	predictions = model.predict(ds.data)
	prop_correct = ((predictions[predictions[:] == ds.target[:]].size)) 
	
	return [r_sq, prop_correct]

#Split dataset into training, test regions to estimate out of sample performance 
def q2b(ds):
	#Randomly split indices into two groups (2:1 ratio)
	indices = list(range(0, ds.data.shape[0])) 
	random.shuffle(indices)
	training_indices = indices[0:202]
	test_indices = indices[202:]

	#Use above indices to split datset into training, target sections
	training_data = ds.data[training_indices, :]
	test_data = ds.data[test_indices, :]
	training_targets = ds.target[training_indices]
	test_targets = ds.target[test_indices]

	#Use training data to train regression model
	model = LinearRegression().fit(training_data, training_targets)

	#Evaluate model against training, test data
	return(model.score(training_data, training_targets), model.score(test_data, test_targets))

def main(): 	
	ds = fetch_openml(name="cholesterol", version=1)
	
	scores = q2a(ds)
	print("r-squared value: " + str(round(scores[0], 2)))
	print("percentage of exactly correct predictions: " + str(round(scores[1], 2)))

	r_sqs = q2b(ds)
	print("r-squared value (Training instances): " + str(round(r_sqs[0], 2)))
	print("r-squared value (Test instances): " + str(round(r_sqs[1], 2)))

if __name__ == "__main__":
	main()