#Brendan Sherman
#Homework 7 Question 1: Random Variables
#Writeup contains all output/explanations of code

from scipy.stats import geom, binom 

#Problem 1A: probability that the lowest-index example misclassified by  
# model w/ 0.3 error probability has index 4. 
def q1a():
	return geom.pmf(5, .3) 

#Problem 1B: probability of 12 or more misclassifications in 50 trials 
# (given classification accuracy of .8)
def q1b():
	return binom.cdf(38, 50, .8)

def main():
	print("1A answer: " + str(round(q1a(), 3)))
	print("1B answer: " + str(round(q1b(), 3)))

if __name__ == "__main__":
	main()