from helper_functions import (
    get_filters,
    load_data,
    time_stats,
    station_stats,
    trip_duration_stats,
    user_stats,
)
from representation import display_raw_data


def main():
    while True:
        filter_, city, month, day = get_filters()
        df = load_data(city, month, day)

        print("#" * 20)
        print(f"Data Filter By: {filter_.title()}")
        print("#" * 20)

        time_stats(df, filter_)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        choice = input("\nWould like to view raw data? Enter yes or no.\n")
        while choice not in ["yes", "no"]:
            choice = input("\nWrong input, please try again? Enter yes or no.\n")
        if choice == "yes":
            display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
