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
find_origin.nlargest(15, 'count')
print(find_origin)



#Datatypes of contacts dataset
contacts.dtypes

#Manipulation of contacts dataset

#Convert date columns to datetime data type 
contacts['ts_contact_at'] = pd.to_datetime(contacts['ts_contact_at'])
contacts['ts_reply_at'] = pd.to_datetime(contacts['ts_reply_at'])
contacts['ts_accepted_at'] = pd.to_datetime(contacts['ts_accepted_at'])
contacts['ts_booking_at'] = pd.to_datetime(contacts['ts_booking_at'])
contacts['ds_checkin'] = pd.to_datetime(contacts['ds_checkin'])
contacts['ds_checkout'] = pd.to_datetime(contacts['ds_checkout'])
contacts['accepted'] = np.where(np.isnan(contacts['ts_accepted_at']), False, True)

contacts['stay_length'] = contacts['ds_checkout'] - contacts['ds_checkin']

#Understand dataset with describe function
display(contacts.describe())

#Calculate skewness in contacts dataset
display(contacts.skew(axis = 0, numeric_only = True, skipna = True))

from scipy.stats import boxcox

# Apply Box-Cox transformation to skewed columns
skewed_columns = ['n_guests', 'n_messages']
for col in skewed_columns:
    contacts[col], _ = boxcox(contacts[col] + 1)  # Adding 1 to handle zero values

# Now you can check the skewness again to see if it has improved
new_skewness = contacts.skew(axis=0, numeric_only=True, skipna=True)
display(new_skewness)

# The direction of skewness is given by the sign.
# The coefficient compares the sample distribution with a normal distribution. The larger the value, the larger the distribution differs from a normal distribution.
# A value of zero means no skewness at all.
# A large negative value means the distribution is negatively skewed.
# A large positive value means the distribution is positively skewed.


#Number of guests stayed, I choose 8 because less than 2%(1.46%) of the contacts dataset has 8 or more guests
contacts_less8 = contacts[contacts['n_guests'] < 8]
sns.displot(contacts_less8, x = 'n_guests', hue = 'accepted', multiple="dodge", binwidth=0.3)
plt.show()

#Conversion rate from accepting to booking
contacts['ts_booking_at'].count()/contacts['ts_accepted_at'].count()

#Timeframe of when guests or accepted vs rejected

contacts['month_checkin'] = contacts['ds_checkin'].dt.month #Extract month from checkin date
contacts_checkin = contacts[contacts['month_checkin'] > 9] #Use only peak season months (Oct, Nov, Dec)

#Distribution of checkin among October, November, and December and split by acceptance
sns.displot(contacts_checkin, x='month_checkin', hue = 'accepted', multiple="dodge", binwidth=0.3)
plt.xticks([10, 11, 12])
plt.show()

#Merge datasets for more analysis
merged_datasets = contacts.merge(searches, left_on='id_guest', right_on='id_user')

#Check difference between prices searched between accepted/rejected applicants
merged_pricemax_filter = merged_datasets.loc[(merged_datasets['filter_price_max'] <= 600)]
sns.displot(merged_pricemax_filter, x="filter_price_max", hue="accepted", multiple="dodge")
plt.show()

#Classify dataset based on filter_price_max

def label_price (row):
    if (row['filter_price_max'] >= 0) & (row['filter_price_max'] < 100):
        return '0-100'
    
    elif (row['filter_price_max'] >= 100) & (row['filter_price_max'] < 200):
        return '100-200'

    elif (row['filter_price_max'] >= 200) & (row['filter_price_max'] < 300):
        return '200-300'
    
    elif (row['filter_price_max'] >= 300) & (row['filter_price_max'] < 400):
        return '300-400'

    elif (row['filter_price_max'] >= 400) & (row['filter_price_max'] < 500):
        return '400-500'
    
    elif (row['filter_price_max'] >= 500) & (row['filter_price_max'] < 600):
        return '500-600'
    
    else:
        return '600+'

merged_datasets['classification_max_price'] = merged_datasets.apply(lambda row: label_price(row), axis=1)

merged_datasets.groupby('classification_max_price').agg({'accepted': 'mean'})

#Find the acceptance rate by country

dataset_country = merged_datasets[['origin_country', 'accepted']]

#Find acceptance count by country and accepted
accepted_count = dataset_country.groupby(['origin_country', 'accepted']).agg({'origin_country':'count'})
accepted_count.columns = ['count_accepted']

#Find acceptance count by country
country_count = dataset_country.groupby(['origin_country']).agg({'origin_country':'count'})
country_count.columns = ['count_country']

#Merge datasets for easier manipulation 
acceptance_country = pd.merge(dataset_country, accepted_count,  how='left', on=['origin_country','accepted']) #Merge accepted count
acceptance_country = acceptance_country.drop_duplicates()

acceptance_country = pd.merge(acceptance_country, country_count, how='left', on=['origin_country']) #Merge total country count
acceptance_country = acceptance_country.sort_values(['count_country', 'accepted'], ascending = [False, True])
acceptance_country = acceptance_country[acceptance_country['count_country'] >= 100] #100 is used so there is a good amount of data to make assumptions
acceptance_country = acceptance_country[acceptance_country['accepted'] == True]

#Divide count_accepted column by count_country column to find acceptance rate by country
acceptance_country['acceptance_rate'] = acceptance_country['count_accepted']/acceptance_country['count_country']
acceptance_country.sort_values(['acceptance_rate'], ascending = True)