#Import libraries/dataset
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

contacts_file = ("contacts.tsv")
contacts = pd.read_csv(contacts_file, sep="\t")
searches_file = ("searches.tsv")
searches = pd.read_csv(searches_file, sep="\t")

#Find % of null values in datasets 
print('Contact')
print(contacts.isna().sum()/len(contacts), '\n')
print('Searche')
print(searches.isna().sum()/len(searches))


#Drop filter_neighborhoods column, from the previous result it has 96% null value
searches = searches.drop(columns=['filter_neighborhoods'])


#Manipulation of searches dataset

#Convert date column to datetime data type for easier analysis
searches['ds'] = pd.to_datetime(searches['ds'])
searches['ds_checkin'] = pd.to_datetime(searches['ds_checkin'])
searches['ds_checkout'] = pd.to_datetime(searches['ds_checkout'])

#Find out how soon they want the room
searches['length_preperation'] = searches['ds_checkin'] - searches['ds']

#Describe searches dataset

#Helps understand the dataset and its distribution of values within columns better
display(searches.describe())

#Calculate skewness in searches dataset
display(searches.skew(axis = 0, numeric_only = True, skipna = True))

#Distribution plot of n_guests_min and n_guests_max
sns.displot(searches, x = 'n_guests_min', color = 'blue', binwidth=0.8)
sns.displot(searches, x = 'n_guests_max', color = 'black', binwidth=0.8)
plt.show()

#When were searches conducted
ax = sns.displot(searches, x = 'ds', color = 'blue')
[plt.setp(ax.get_xticklabels(), rotation=90) for ax in ax.axes.flat]

#Percentage of dataset with a filter_price_max above 600
percentage = (len(searches[searches['filter_price_max'] > 600]) / len(searches['filter_price_max'])) * 100
formatted_percentage = round(percentage, 2)

print(formatted_percentage, '%')

#Distribution of filter_price_max of searches

#Removing the set upper limit
remove_upper_limit = searches[searches['filter_price_max'] <= 600]

#Show the price distribution of what price range people search for
sns.displot(x=remove_upper_limit["filter_price_max"], color = 'blue')
plt.show()

#Percentage of dataset with preparation length beyond 100 days
distribution = searches["length_preperation"] / np.timedelta64(1, 'D')
print(len(distribution[distribution > 100])/len(distribution)*100, '% \n')

#Remove data with preparation time beyond 100 days
distribution = distribution[distribution < 100]

#Print exact number for each preparation time range
price_distribution_1 = distribution[(distribution >= 0) & (distribution < 25)]
price_within_range_1 = (len(price_distribution_1) / len(distribution)) * 100

price_distribution_2 = distribution[(distribution >= 25) & (distribution < 50)]
price_within_range_2 = (len(price_distribution_2) / len(distribution)) * 100

price_distribution_3 = distribution[(distribution >= 50) & (distribution < 75)]
price_within_range_3 = (len(price_distribution_3) / len(distribution)) * 100

price_distribution_3 = distribution[(distribution >= 75) & (distribution <= 100)]
price_within_range_4 = (len(price_distribution_3) / len(distribution)) * 100

print(round(price_within_range_1, 2), '%')
print(round(price_within_range_2, 2), '%')
print(round(price_within_range_3, 2), '%')
print(round(price_within_range_4, 2), '%')

#Distribution plot of preparation time
sns.displot(x=distribution, color = 'blue')
plt.show()


#Distribution of nights people want to stay

#Percentage of dataset beyond 20 nights
print(len(searches[searches['n_nights'] > 20])/len(searches['n_nights'])*100, '% \n')
#Remove n_nights beyond 20 days
under_20N = searches[searches['n_nights'] < 20]

#Find distribution of nights people stay
nights_1_3 = (len(under_20N[(under_20N['n_nights'] >= 1) & (under_20N['n_nights'] <= 3)]) / len(searches)) * 100
nights_4_7 = (len(under_20N[(under_20N['n_nights'] >= 4) & (under_20N['n_nights'] <= 7)]) / len(searches)) * 100
nights_8_10 = (len(under_20N[(under_20N['n_nights'] >= 8) & (under_20N['n_nights'] <= 10)]) / len(searches)) * 100
nights_over10 = (len(under_20N[(under_20N['n_nights'] > 10)]) / len(searches)) * 100

print(round(nights_1_3, 2), '% \n')
print(round(nights_4_7, 2), '% \n')
print(round(nights_8_10, 2), '% \n')
print(round(nights_over10, 2), '% \n')

#Distribution plot of length_preperation column
plot = sns.displot(under_20N, x='n_nights', color = 'blue', binwidth=0.8)
plot.set_axis_labels('Number of Nights', 'Count')
plt.xticks(range(1, 21))
plt.show()

import calendar

# Distribution of months of ds_checkin of searches
checkin_month = pd.DatetimeIndex(searches['ds_checkin']).month

# Get the names of the months
month_names = [calendar.month_name[i] for i in range(1, 13)]

# Distribution plot of checkin_month
sns.displot(checkin_month, color='yellow', binwidth=0.8)
plt.xticks(range(1, 13), labels=month_names, rotation=45)
plt.show()

#Find top 15 countries where searches originate from

#Group by origin country and finding the count of each country
find_origin = searches.groupby("origin_country").agg({'origin_country' : 'count'})
find_origin.columns = ['count']

find_origin = find_origin.sort_values('count', ascending = False) 
largest_origin = find_origin.nlargest(15, 'count')

print(find_origin)




