import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #asking the user to enter the city name and recording it as input
    city = input("Please type a city(chicago, new york city, washington) : ").title()

    #a flag to set an open loop

    flag = 0   

    #looping through input until it gets the right answer

    while flag == 0:
        if city in ['Chicago','New York City','Washington']:
            break
        else:
            city = input("Wrong input, Please type a city(chicago, new york city, washington) : ").title()    

    #asking the user to enter the month name and recording it as input

    month = input("Please type a month(january, february, ... , june) or all : ").title()

    #looping through input until it gets the right answer
    
    while flag == 0:
        if month in ['January','February','March','April','May','June','All']:
            break
        else:
            month = input("Wrong input, Please type a month(january, february, ... , june) or all : ").title()    


    #asking the user to enter the day name and recording it as input

    day = input("Please type a day(monday, tuesday, ... sunday) or all : ").title()

    #looping through input until it gets the right answer
    
    while flag == 0:
        if day in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']:
            break
        else:
            day = input("Wrong input, Please type a day(monday, tuesday, ... sunday) or all : ").title()    


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #reading the .csv file of the selected city

    df = pd.read_csv(CITY_DATA[city])
    
    #converting Start Time column to datetime type

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #converting End Time column to datetime type

    df['End Time'] = pd.to_datetime(df['End Time'])

    #creating a new column of the month name of the start time

    df['Month'] = df['Start Time'].dt.month_name()

    #creating a new column of the day name of the start time

    df['Day'] = df['Start Time'].dt.day_name()

    #creating a new column of the hours of the start time
    
    df['Hour'] = df['Start Time'].dt.hour

    #creating a new column in wich start and end stations are compined for each trip
        
    df["Start / End Stations"] = df["Start Station"] + "  /  " + df ["End Station"]
    
    #creating a new column of trip's time

    df["Travel Time"] = df["End Time"] - df["Start Time"]
    
    #converting the travel time column of the trips into seconds

    df["Travel Time"] = df["Travel Time"].dt.total_seconds()
    
    #if condition to check if the user did not choose all months to filter dataframe by selection 

    if month != "All":
        df = df[df["Month"] == month]
    
    #if condition to check if the user did not choose all days to filter dataframe by selection 

    if day != "All":
        df = df[df["Day"] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #printing the most common month
    
    print("The most common month:" , df["Month"].mode()[0])

    #printing the most common day of week
    
    print("The monst common day:" , df["Day"].mode()[0])


    #printing the most common start hour
    
    print("The most common day:" , df["Hour"].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #printing the most commonly used start station
    
    print("The monst common used start station:" , df["Start Station"].mode()[0])


    #printing the most commonly used end station
    
    print("The monst common used end station:" , df["End Station"].mode()[0])


    #printing the most frequent combination of start station and end station trip
    print("The monst frequent combination of start station and end station trip:" , df["Start / End Stations"].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #printing total travel time in seconds
    
    print("Total travel time:" , df["Travel Time"].sum() , "seconds")

    #printing the average travel time in seconds
    
    print("The mean of travel time :" , df["Travel Time"].mean() , "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #printing the counts of User Type


    print("Types of users:")
    print(df['User Type'].value_counts())
    
    #checking if the data contains the birthdat column to do analysis on it or not
    
    if "Birth Year" in df.columns:
        
        #printing the counts of Gender
        print("Types of genders:")
        print(df['Gender'].value_counts())

        #printing the earliest, most recent, and most common year of birth

        print(" The earliest year of birth:", int(df["Birth Year"].min()) , "\n" , "The most recent year of birth:" , int(df["Birth Year"].max()) , "\n" , "The most common year of birth:" , int(df["Birth Year"].mode()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
