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

	country_max_deaths = {} #dictionary relating iso_code to max deaths for each country

	for i in range(iso_codes.size):
		country_rows = df[df['iso_code'] == iso_codes[i]] #extract all rows for given country
		max_deaths = country_rows['total_deaths_per_million'].max()
		key = q3a(iso_codes[i])

		country_max_deaths[key] = max_deaths

	#computing 25th and 75th percentiles for maximum deaths
	q1 = np.nanquantile(list(country_max_deaths.values()), .25)
	q3 = np.nanquantile(list(country_max_deaths.values()), .75)

	top_quarter = []
	low_quarter = []

	i = 0 
	for key, val in country_max_deaths.items():
		if(val >= q3 and not(np.isnan(val)) and len(iso_codes[i]) == 3):
			top_quarter.append(iso_codes[i])
		elif(val < q1 and not(np.isnan(val)) and len(iso_codes[i]) == 3):
			low_quarter.append(iso_codes[i])
		i += 1

	top_quarter = sorted(top_quarter)
	low_quarter = sorted(low_quarter)
	
	print("Countries within top quarter of maximum covid deaths (per million people):")
	print(top_quarter)
	print("Countries within bottom quarter of maximum covid deaths (per million people):")
	print(low_quarter)
	return [low_quarter, top_quarter]

#given a string s, remove quotation and whitespace characters
def strip_quotes_spaces(s):
	return s.strip("\" ")

#Q4a: Replace iso_code and latitude column data with stripped strings
def q4a(geo_df):
	stripped_iso_col = geo_df['Alpha-3 code'].apply(strip_quotes_spaces)
	stripped_lat_col = geo_df['Latitude (average)'].apply(strip_quotes_spaces)

	geo_df['Alpha-3 code'] = stripped_iso_col 
	geo_df['Latitude (average)'] = stripped_lat_col

#Q4b: Given a country (iso code), return its average latitude
def get_avg_lat(geo_df, iso):
	row = geo_df[geo_df['Alpha-3 code'].astype('str').str.fullmatch(iso)]
	avg_lat = float(row['Latitude (average)'].iat[0])

	if(not np.isnan(avg_lat)):
		return avg_lat
	else:
		return np.nan

#Q4b: create list of avg latitudes for low and high mortality countries (from q3)
def q4b(df, geo_df):
	q4a(geo_df)
	iso_lists = q3b(df)
	low_mortality_quarter = iso_lists[0]
	high_mortality_quarter = iso_lists[1]

	high_mortality_avg_lats = []
	low_mortality_avg_lats = []

	for i in high_mortality_quarter:
		high_mortality_avg_lats.append(get_avg_lat(geo_df, i))

	for i in low_mortality_quarter:
		low_mortality_avg_lats.append(get_avg_lat(geo_df, i))

	print("Average latitude of lower quartile COVID mortality countries:")
	print(low_mortality_avg_lats)
	print("Average latitude of higher quartile COVID mortality countries:")
	print(high_mortality_avg_lats)

	return [low_mortality_avg_lats, high_mortality_avg_lats]

#Q4c: Compute medians of both average latitude lists, evaluate significance
def q4c(df, geo_df):
	avg_lats = q4b(df, geo_df)

	print("Median latitutde for countries in lowest quartile: " + str(round(np.median(avg_lats[0]), 3)))
	print("Median latitutde for countries in highest quartile: " + str(round(np.median(avg_lats[1]), 3)))

	boxplot(avg_lats, notch=True)
	show()

def main(): 
	df = pd.read_csv('owid-covid-data.csv')
	geo_df = pd.read_csv("countries_codes_and_coordinates.csv")

	#print_labels(df)
	#q1(df)
	#q2(df)
	q4c(df, geo_df)

if __name__ == "__main__":
	main()

	