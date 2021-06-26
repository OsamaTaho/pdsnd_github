import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """ 

    city = chech_for_city()
    month = check_for_month()
    day = check_for_day()

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
    df['hour']=df['Start Time'].dt.hour

    if month != 13:
        df = df[df['month']==month]
    if day.lower() != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
                                                                                                            
    print('\nCalculating The Most Frequent Times of Travel...\n')                                           
    start_time = time.time()                                                                               

    print('The most common month\t\t',months[df['month'].mode()[0]])
    print('The most common day of the week\t',df['day_of_week'].mode()[0])
    print('The most common hour\t\t',str(df['hour'].mode()[0]))
    
    end_time=time.time() - start_time
    print("\nThis took %s seconds." % round(end_time,4))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('The most commonly used start station\t',df['Start Station'].mode()[0])
    print('The most commonly used end station\t',df['End Station'].mode()[0])
    print('The most frequent combination\t\t',(df['Start Station']+' and '+df['End Station']).mode()[0])

    end_time=time.time() - start_time
    print("\nThis took %s seconds." % round(end_time,4))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('The total travel time\t\t',str(round(df['Trip Duration'].sum()/3600,2)),' Hours')
    print('The mean travel time\t\t',str(round(df['Trip Duration'].mean()/60,2)),' Minutes')

    end_time=time.time() - start_time
    print("\nThis took %s seconds." % round(end_time,4))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        print('The count of user types\nSubscriber\t\t\t',str(df['User Type'].value_counts()[0]),'\nCustomer\t\t\t\t',str(df['User Type'].value_counts()[1]))
        print('\nThe count of gender\nMale\t\t\t\t',str(df['Gender'].value_counts()[0]),'\nFemale\t\t\t\t',str(df['Gender'].value_counts()[1]))
        eyof=str(int(df['Birth Year'].max()))
        ryof=str(int(df['Birth Year'].min()))
        cyof=str(int(df['Birth Year'].mode()[0]))
        print('\nEarliest year of birth\t\t '+eyof+'\nRecent year of birth\t\t '+ryof+'\nMost common year of birth\t\t '+cyof)
    except:
        print(txt[7])

    end_time=time.time() - start_time
    print("\nThis took %s seconds." % round(end_time,4))
    print('-'*40)

def rawdata_check(df):
    """Displays the 5 row raw data if the user want to see"""
    
    
    c=5
    pd.set_option('display.max_columns',200)
    while True:
        rawdata = input(txt[5]).lower()
        if rawdata in ['yes','yea','y','yeah','no','nah','n']:
            break
        else:
            print(txt[2],f'{rawdata} wasn\'t the answer i was looking for\nPlease pick again')
            
    while rawdata in ['yes','yea','y','yeah']:
        if c==5:
            print(df.head(c))
        else:
            print(df.head(c).tail())
        while True:
            rawdata = input(txt[6]).lower()
            if rawdata in ['yes','yea','y','yeah','no','nah','n']:
                break
            else:
                print(txt[2],f'{rawdata} wasn\'t the answer i was looking for\nPlease pick again')
        c+=5
    print('-'*40)
                        

def main():
    print(txt[0])
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rawdata_check(df)
        
        while True:
            restart = input('\nWould you like to restart? Enter yes to keep going or no to eliminate:\n')
            if restart in ['yes','yea','y','yeah','no','nah','n']:
                break
            else:
                print(txt[2],f'{restart} wasn\'t the answer i was looking for\nPlease pick again')
        if restart.lower() not in ['yes','yea','y','yeah']:
            break
    
    


txt= ['Hello! Let\'s explore some US bikeshare data!','Which city you want to explore? (Chicago 1, New york city 2, Washington 3) Enter either name or number:\n','\nWhoops, hummm... how can i say this!\n','Which month my good fine sir? (all, Jan 1, Feb 2, Mar 3,...) Enter either shortcut(first three chars) name or number:\n','which day of the week are talking about? (all, Monday 1, Tuesday 2, Wednesday 3,...) Enter either name or number:\n','\nWould you like to see raw data? Enter yes to keep going or no to eliminate:\n','if you\'d like to see more Enter yes or no to eliminate:\n','Weeeelp... There\'s no more data for this city!']



def chech_for_city():
    """This method check for city input and return the designated format"""
    
    while True:
        city=input(txt[1]).lower().strip()
        if city.lower() in ['chicago','new york city','washington','1','2','3']:
            break
        else:
            print(txt[2]+f'{city} doesn\'t seem like a city we have data for\n'+'You should only type what was provided in the question\n (i.e) chicago or 1')
    
    if city =='1':
        city='chicago'
    elif city=='2':
        city='new york city'
    elif city=='3':
        city='washington'
    return city    

def check_for_month():
    """This method check for month input and return the designated format"""
    
    while True:
        month=input(txt[3]).lower().strip()
        if month in ['jan','feb','mar','apr','may','jun','1','2','3','4','5','6','all']:
            break
        elif month in ['jul','aug','sep','oct','nov','dec','7','8','9','10','11','12']:
            print('Well.... how can i say this, It seems that there are no data for the chosen month. Sorry\nPlease pick again from (jan to jun) or (1 to 6)')
        else:
            print(txt[2]+f'seems like {month} came from a calender we don\'t support!\n'+'You should only type what was provided in the question\n (i.e) feb or 2')
    if month in ['1','jan']:
        month='1'
    elif month in ['2','feb']:
        month='2'
    elif month in ['3','mar']:
        month='3'
    elif month in ['4','apr']:
        month='4'
    elif month in ['5','may']:
        month='5'
    elif month in ['6','jun']:
        month='6'
    #elif month in ['7','jul']:                                 # Because the datasets don't have
    #    month='7'                                                any month past June, so we had 
    #elif month in ['8','aug']:                                   to force to choosing one of the
    #    month='8'                                                provided months :)
    #elif month in ['9','sep']:
    #    month='9'
    #elif month in ['10','oct']:
    #    month='10'
    #elif month in ['11','nov']:
    #    month='11'
    #elif month in ['12','dec']:
    #    month='12'
    elif month =='all':
        month='13'
    return int(month)
        
    
def check_for_day():
    """This method check for day input and return the designated format"""
    
    while True:
        day=input(txt[4]).lower().strip()
        if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','1','2','3','4','5','6','7','all']:
            break
        else:
            print(txt[2]+f'{day} is a new week day to me, nonetheless it\'s not available in our dataset\n'+'You should only type what was provided in the question\n (i.e) thursday or 4')
    if day =='1':
        day='Monday'
    elif day=='2':
        day='Tuesday'
    elif day=='3':
        day='Wednesday'
    elif day=='4':
        day='Thursday'
    elif day=='5':
        day='Friday'
    elif day=='6':
        day='Saturday'
    elif day=='7':
        day='Sunday'
    return day.title()

months={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}


if __name__ == "__main__":
	main()

    