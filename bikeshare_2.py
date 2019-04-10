import time
import pandas as pd

CITY_DATA = {'Chicago': 'chicago.csv',
             'New york city': 'new_york_city.csv',
             'Washington': 'washington.csv'}
CITY_OPTIONS = ['', 'Chicago', 'New york city', 'Washington']
MONTH_OPTIONS = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
DAY_OPTIONS = ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Sets user input for which city, month, and day to analyze.

    Returns:
        (int) city_index - index of the city to analyze
        (int) month_index - index of the month to filter by, or "all" to apply no month filter
        (int) day_index - index of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city_index = get_user_input('city', CITY_OPTIONS, range(1, len(CITY_OPTIONS)))

    # get user input for month (all, january, february, ... , june)
    month_index = get_user_input('month', MONTH_OPTIONS, range(len(MONTH_OPTIONS)))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_index = get_user_input('day of week', DAY_OPTIONS, range(len(DAY_OPTIONS)))

    print('-'*40)
    return city_index, month_index, day_index


def get_user_input(data_category, data_options, options_range):
    """
    Asks user to specify a city, month, and day to analyze.

    Args:
        (str) data_category - category of data to be explored. For example, 'city'
        (list) data_options - options for data to be explored. For example, 'chicago', 'new_york_city'
        (range) options_range - range of numbers for indentifying the options

    Returns:
        (int) city_index - index of the city to analyze
        (int) month_index - index of the month to filter by, or "all" to apply no month filter
        (int) day_index - index of the day of week to filter by, or "all" to apply no day filter
    """
    # while loop ensures a valid user input and handles all errors
    while True:
        print("\nChoose a {} to explore. (Example: Enter 1 to choose {})".format(data_category, data_options[1]))
        # display options
        for number in options_range:
            print("{}. {}".format(number, data_options[number]))
        try:
            choice = int(input("Choice: "))
            if choice in options_range:
                return choice
            else:
                print("\nInvalid choice. Try again")
        except:
            print("\nInvalid input. Try again")


def load_data(city_index, month_index, day_index):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (int) city_index - index of the city to analyze
        (int) month_index - index of the month to filter by, or "all" to apply no month filter
        (int) day_index - index of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load a city's data file into a dataframe
    df = pd.read_csv(CITY_DATA[CITY_OPTIONS[city_index]])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract data from Start Time column to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    # filter dataframe by month and day as applicable
    if month_index > 0 and day_index == 0:
        df = df[df['Month'] == month_index]
    elif month_index == 0 and day_index > 0:
        df = df[df['Day of week'] == DAY_OPTIONS[day_index]]
    elif month_index > 0 and day_index > 0:
        df = df[(df['Month'] == month_index) & (df['Day of week'] == DAY_OPTIONS[day_index])]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month:\n{}\n".format(MONTH_OPTIONS[df['Month'].mode()[0]]))

    # display the most common day of week
    print("Most common day of week:\n{}\n".format(df['Day of week'].mode()[0]))

    # display the most common start hour
    print("Most common start hour:\n{}\n".format(df['Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station:\n{}\n".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("Most commonly used end station:\n{}\n".format(df['End Station'].mode()[0]))

    #combine start station and end station trip
    df['Trip'] = "FROM: " + df['Start Station'] + "\nTO: " + df['End Station']

    # display most frequent combination of start station and end station trip
    print("Most frequent trip:\n{}\n".format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time:\n{} seconds\n".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("Mean travel time:\n{} seconds\n".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n{}\n".format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df.columns:
        print("Counts of gender:\n{}\n".format(df['Gender'].value_counts()))
    else:
        print("This city has no record for gender\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Earliest year of birth:\n{}\n".format(df['Birth Year'].min()))
        print("Most recent year of birth:\n{}\n".format(df['Birth Year'].max()))
        print("Most common year of birth:\n{}\n".format(df['Birth Year'].mode()[0]))
    else:
        print("This city has no record for year of birth\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    city, month, day = get_filters()
    df = load_data(city, month, day)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)

    # while loop ensures a valid user input and handles all errors
    while True:
        print("\nWould you like to restart? (Example: Enter 1 to choose Yes)")
        print("1. Yes\n2. No")
        try:
            choice = int(input("Choice: "))
            if choice == 1:
                print('-'*40)
                break
            elif choice == 2:
                break
            else:
                print("\nInvalid choice. Try again")
        except:
            print("\nInvalid input. Try again")

    if choice == 1:
        main() # restart program

if __name__ == "__main__":
	main()
