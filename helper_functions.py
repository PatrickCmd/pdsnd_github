import sys
import time

import pandas as pd

from data import CITY_DATA, DAYS, MONTHS
from representation import tabular_representation


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    while True:
        try:
            city = input(
                "Enter the city (chicago, new york city, washington) for which you like to explore.\n"
            )
            CITY_DATA[city]

            month, day = "all", "all"
            filter_ = input(
                "Would you like to filter the data by month, day, both or not at all? Type 'none' for no filter.\n"
            )
            while filter_ not in ["both", "day", "month", "none"]:
                filter_ = input(
                    "Wrong filter, please filter the data by month, day, both or not at all? Type 'none' for no filter.\n"
                )

            if filter_ == "both":
                month = input(
                    "Which month? January, February, March, April, May, or June?\n"
                )
                MONTHS.index(month.lower())

                day = input(
                    "Which day of the week? (Mon, Tue, Wed, Thu, Fri, Sat, Sun)\n"
                )
                day = DAYS[day.title()]
                break

            elif filter_ == "day":
                day = input(
                    "Which day of the week? (Mon, Tue, Wed, Thu, Fri, Sat, Sun)\n"
                )
                day = DAYS[day.title()]
                break

            elif filter_ == "month":
                month = input(
                    "Which month? January, February, March, April, May, or June?\n"
                )
                MONTHS.index(month.lower())
                break
            else:
                break
        except ValueError:
            print("Please choose a month from January through June?\n")
        except KeyError:
            print(
                "Worng value entered for city or day of week, please follow instructions."
            )
        except KeyboardInterrupt:
            print(" KeyboardInterrupt. Please you can repeat again.")
            sys.exit(0)

    print("-" * 40)
    return filter_, city, month, day


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

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name

    # filter by month if applicable
    if month != "all":
        month = MONTHS.index(month.lower()) + 1

        # filter by month to create new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df, filter_):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    table = tabular_representation(
        ["Most Frequent Times of Travel", "Month/Day/Hour", "Count"]
    )

    # Display the most common month
    if filter_ == "none" or filter_ == "day":
        month_counts = df["month"].value_counts().to_dict()
        common_month = df["month"].mode()[0]
        month = MONTHS[common_month - 1].title()
        count = month_counts[MONTHS.index(month.lower()) - 1]
        table.append_row(["Month", month, count])

    # Display the most common day of week
    if filter_ == "none" or filter_ == "month":
        day_counts = df["day_of_week"].value_counts()
        common_day_of_week = df["day_of_week"].mode()[0]
        count = day_counts[common_day_of_week]
        table.append_row(["Day of week", common_day_of_week, count])

    # Display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    start_hour_counts = df["hour"].value_counts()
    popular_hour = df["hour"].mode()[0]
    count = start_hour_counts[popular_hour]
    table.append_row(["Start hour", popular_hour, count])
    print(table)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()
    table = tabular_representation(
        ["Most Popular Stations and Trip", "Station", "Count"]
    )

    # Display most commonly used start station
    start_station_counts = df["Start Station"].value_counts().to_dict()
    common_start_station = df["Start Station"].mode()[0]
    table.append_row(
        [
            "Start Station",
            common_start_station,
            start_station_counts[common_start_station],
        ]
    )

    # Display most commonly used end station
    end_station_counts = df["End Station"].value_counts().to_dict()
    common_end_station = df["End Station"].mode()[0]
    table.append_row(
        ["End Station", common_end_station, end_station_counts[common_end_station]]
    )

    # Display most frequent combination of start station and end station trip
    df["station_comb"] = df["Start Station"] + " and " + df["End Station"]
    most_common_start_end_station_comb = df["station_comb"].mode()[0]
    comb_counts = df["station_comb"].value_counts().to_dict()
    table.append_row(
        [
            "Trip",
            most_common_start_end_station_comb,
            comb_counts[most_common_start_end_station_comb],
        ]
    )
    print(table)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(f"Total travel time: {total_travel_time}")

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(f"Average travel time: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    print("User Types Breakdown")
    user_types = df["User Type"].value_counts().to_dict()
    table = tabular_representation(["User Types", "Count"], data=user_types)
    print(table)
    print()

    if city != "washington":
        # Display counts of gender
        print("Gender Breakdown")
        gender_count = df["Gender"].value_counts().to_dict()
        table = tabular_representation(["Gender", "Count"], data=gender_count)
        print(table)
        print()

        # Display earliest, most recent, and most common year of birth
        print(f"Earliest Year of Birth: {df['Birth Year'].min()}")
        print(f"Most Recent Year of Birth: {df['Birth Year'].max()}")
        print(f"Most Common Year of Birth: {df['Birth Year'].mode()[0]}")

        print("\nThis took %s seconds." % (time.time() - start_time))
        print("-" * 40)
    else:
        print("\nNo gender and birth year data available")
