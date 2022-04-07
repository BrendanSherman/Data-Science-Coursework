#Brendan Sherman
#Homework 7 Question 2: Monte Carlo Analysis
#Writeup contains all output/explanations of code

import numpy as np 

#Problem 2A: Write a function that provides a Monte Carlo estimate of the probability
# that the sum of three fair die rolls will be 10 or larger. 
def q2a(sample_size):
	successes = 0
	#Run 'N' trials
	for i in range(sample_size):
		vals = np.random.randint(1, 7, 3) #simulate 3 die rolls
		if(np.sum(vals) >= 10):
			successes += 1

	return successes / sample_size

def q2

def main():
	print(q2a(100))

if __name__ == "__main__":
	main()