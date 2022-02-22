#Homework 4: COVID data analysis (Pandas, MPL, numpy)
#Writeup contains explanation of all code
#Author: Brendan Sherman 

from matplotlib.pyplot import show, scatter, xlabel, ylabel, boxplot
import numpy as np
import pandas as pd

#for reference, prints all column labels in dataset
def print_labels(df):
	print(df.columns.values)

#Problem 1 - Correlation between vaccination rate and covid-related deaths
def q1(df):
	iso_codes = np.unique(df['iso_code']) #1D array of unique countries

	#cleans rows with 'nan' values under specified columns
	df = df.dropna(subset=['total_deaths_per_million', 'people_fully_vaccinated_per_hundred'])
	arr = np.empty((0, 2))

	for j in range(iso_codes.size):
		country_rows = df[df['iso_code'] == iso_codes[j]] #array of data for given country
		max_deaths = country_rows['total_deaths_per_million'].max()
		max_vaccination_rate = country_rows['people_fully_vaccinated_per_hundred'].max()
		
		#append paired maximum values, given that data is present
		#also accounts for erroneous percentages (>100)
		if((not np.isnan(max_vaccination_rate)) and (not np.isnan(max_deaths)) 
		and max_vaccination_rate <= 100):
			arr = np.append(arr, np.array([[max_vaccination_rate, max_deaths]]), axis=0)
	
	scatter(arr[:, 0], arr[:, 1])
	xlabel("Maximum Percentage Fully Vaccinated")
	ylabel("Maximum Total Deaths (per million people)")
	show()

	r = np.corrcoef(arr[:, 0], arr[:, 1])
	print("Pearson Correlation Coefficient: " + str(round(r[0,1], 3)))

#Problem 2- Continuing problem 1 analysis, now considering time granularity
def q2(df):
	iso_codes = np.unique(df['iso_code']) #1D array of unique countries
	corrs = np.empty((0, 2))

	for i in range(iso_codes.size):
		country_rows = df[df['iso_code'] == iso_codes[i]] #all data for given country
		
		#time-indexing data 
		index = pd.DatetimeIndex(country_rows['date'])
		timed_vaccination_rate = pd.Series(country_rows['people_fully_vaccinated_per_hundred'].values, index=index)
		timed_new_deaths = pd.Series(country_rows['new_deaths_smoothed_per_million'].values, index=index)

		#computing correlation between time series 
		corr = timed_vaccination_rate.corr(timed_new_deaths)
		corrs = np.append(corrs, [corr])

	#use boolean indexing to clear 'nan' values (missing data)
	corrs = corrs[~np.isnan(corrs)]

	print("Median Correlation Value: " + str(round(np.median(corrs), 3)))
	boxplot(corrs, notch=True)
	show()

#given a string s, return corresponding integer value in base 256 
def q3a(s):
	s_reverse = s[::-1] 
	val = 0
	i = 0
	for c in s_reverse:
		val += (ord(c) * (256**i))
		i += 1

	return val

#Countries in lowest and highest quartiles for total COVID deaths
def q3b(df):
	iso_codes = np.unique(df['iso_code']) #1D array of unique countries

	country_max_deaths = {} #dictionary relating iso_code to max deaths for that country

	for i in range(iso_codes.size):
		country_rows = df[df['iso_code'] == iso_codes[i]] #extract all rows for given country
		max_deaths = country_rows['total_deaths_per_million'].max()
		key = q3a(iso_codes[i])

		country_max_deaths[key] = max_deaths

	print(country_max_deaths)




	
def main(): 
	df = pd.read_csv('owid-covid-data.csv')

	#print_labels(df)
	#q1(df)
	#q2(df)
	#print(q3a("CAN"))
	q3b(df)
	

if __name__ == "__main__":
	main()