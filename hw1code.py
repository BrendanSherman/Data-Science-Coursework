#Homework 1: Python/numpy prerequisites
#Writeup contains explanation of all code
#Author: Brendan Sherman 

import numpy as np 

#problem 1- smallest among the squares of list L 
def problem1(L):
	return min([L[n]**2 for n in range(len(L))])

#problem 2- second-from-last element (third highest index position) of the numpy array a.
def problem2(a):
	return a[-3]

#summation of n cubed between -50 and 10^4
def problem3():
	return sum([n**3 for n in range(-50, (10**4) + 1)])

#all nonnegative integers n < 100 such that n^4 > 500n
def problem4():
	return [n for n in range(100) if (n**4) > (500*n)]

#The number of entries in the dictionary D that do not have the value ’red’.
def problem5(D):
	return len([v for v in D.values() if v != "red"])

#largest possible integer m where 10^m < 1000m^6
def problem6():
	i = 1
	largest = 0
	while((10**i) < (1000 * (i**6))):
		largest = i
		i += 1
	return largest

#largest possible integer m where 1000-100m + 5*m^2 - (1/15)m^3 >= 500
def problem7():
	i = 37 
	while((1000 - 100*i + (5 * (i**2)) - ((1/15)*(i**3))) >= 500):
		i += 1
	return i-1

def main():
	L = [ 2, -1, 1, 4, 8]
	print(problem1(L))

	a = np.array([(5, 2, 3), (4, 3, 2), (5, 7, 8), (7, 9, 6)])
	print(problem2(a))

	print(problem3()) 

	print(problem4())

	D = {"color1" : "black", "color2" : "red", "color3" : "blue", "color4": "red"}
	print(problem5(D))

	print(problem6())

	print(problem7()) 

if __name__ == "__main__":
	main()