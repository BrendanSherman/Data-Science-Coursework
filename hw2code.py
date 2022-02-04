#Homework 2: data analysis/visualization
#Writeup contains explanation of all code
#Author: Brendan Sherman 

import numpy as np
from matplotlib.pyplot import boxplot, scatter, show, xlabel, ylabel
import timeit

#problem 1A; iterative and vectorized methods of element-wise operations
#vectorized operations made possible with numpy arrays
def problem1vectorized(arr):
	return arr ** .5

#typical python syntax
def problem1iterative(arr):
	return [n**.5 for n in arr]

#Timing comparison of the previous 2 methods
def problem1B():
	sample = np.random.random((10**4)) #one-dimensional array of size 10^4

	start = timeit.default_timer()
	for i in range (0, 1000):
		problem1iterative(sample)
	iterative_time = timeit.default_timer() - start

	start = timeit.default_timer()
	for i in range (0, 1000):
		problem1vectorized(sample)
	vectorized_time = timeit.default_timer() - start

	ratio = iterative_time / vectorized_time

	iterative_time = round(iterative_time, 3)
	vectorized_time = round(vectorized_time, 3)
	ratio = round(ratio, 3)

	print("Total time for 1000 calls (iterative approach): " + str(iterative_time))
	print("Total time for 1000 calls (vectorized approach):" + str(vectorized_time))
	print("Ratio of iterative time to vectorized time: " + str(ratio))

x = np.random.normal(3, 1, 1000) #loc 3, scale 1, size 1000 (for problem 2)

#computes mean and std of "x" using numpy functions
def problem2A():
	std = round(np.std(x), 3)
	mean = round(np.mean(x), 3)

	print("Mean: " + str(mean))
	print("Standard Deviation: " + str(std))

#standardizes "x", verifies standardized mean and std (0, 1)
def problem2B():
	xStand = (x - np.mean(x)) / np.std(x)
	meanStand = round(np.mean(xStand), 3)
	stdStand = round(np.std(xStand), 3)

	print("Standardized Mean: " + str(meanStand))
	print("Standardized Standard Deviation: " + str(stdStand))	

#boxplot of [u^2 | u is in x]
def problem2C():
	boxplot(x**2)
	show()

#Calculate the numerical location of the three line segments from above plot
def problem2D():
	squares = x**2
	median = np.median(squares) #value of middle line (median)
	first_q = np.percentile(squares, 25) #value of bottom line (Q1)
	third_q = np.percentile(squares, 75) #value of top line (Q3)

	print("Bottom line (Q1): " + str(round(first_q, 3)))
	print("Middle line (Median): " + str(round(median, 3)))
	print("Top line (Q3): " + str(round(third_q, 3)))

#import breast cancer dataset using numpy
def problem3A():
	global data #allows access to data for all problems 
	data = np.loadtxt("data.csv", delimiter=",", skiprows=1)
	print("Numpy array shape: " + str(data.shape))

#scatter plot using mean radius and mean texture attributes as coordinates 
def problem3B():
	scatter(data[:, 2], data[:, 3])
	xlabel("Mean radius")
	ylabel("Mean texture")
	show()

#grouped scatter plot based on target attribute (diagnosis)
def problem3C():
	diagnosis = data[:, 1] #isolates diagnosis column into 1D array

	#divides data into malignant and benign diagnosises
	malig = data[diagnosis == 1]
	benign = data[diagnosis == 0]

	#creates and outputs grouped scatter plot
	scatter(malig[:, 2], malig[:, 3], c="r")
	scatter(benign[:, 2], benign[:, 3], c="g")
	xlabel("Mean radius")
	ylabel("Mean texture")
	show()	

#computing geometric distance between mean vectors for increasing sample sizes
def problem4A():
	sample_sizes = [10 * (2**p) for p in [0, 1, 2, 3, 4, 5]]
	data_means = np.mean(data[:, 2:], axis=0) #population mean vector
	avg_norms = []

	for n in sample_sizes:
		total_norms = 0
		for i in range(10000):
			rows = np.random.choice(569, size=n) #picks N row indices for the sample
			sample = data[rows, 2:] #generates sample from given rows
			sample_means = np.mean(sample, axis=0) #sample mean vector 
			total_norms += np.linalg.norm(sample_means - data_means)

		#store the mean of 10000 norm values for each sample size  
		avg_norms.append(total_norms / n)

	#Print output
	for i in range(len(sample_sizes)):
		avg_norms[i] = round(avg_norms[i], 3)
		print("N: " + str(sample_sizes[i]) + ", Mean norm value: " + str(avg_norms[i]))


def main():
	#arr = np.array([64, 25, 1, 25, 16, 36, 49])
	#print(problem1iterative(arr))
	#print(problem1vectorized(arr))
	#problem1B()
	#problem2A()
	#problem2B()
	#problem2C()
	#problem2D()
	problem3A()
	#problem3B()
	#problem3C()
	problem4A()

if __name__ == "__main__":
	main()