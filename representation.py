from pprint import pprint

from beautifultable import BeautifulTable


def display_raw_data(df):
    """Displays dataframe raw data

    Args:
        (dataframe) df - Bikeshare dataframe
    
    Returns:
        None
    """
    start = 0
    end = 5
    choice = " "
    pprint(df.iloc[start:end].to_dict(orient="records"), indent=2)
    while True:
        choice = input("\nWould like to view more raw data? Enter yes or no.\n")
        while choice not in ["yes", "no"]:
            choice = input("\nWrong input, please try again? Enter yes or no.\n")

        if choice == "yes":
            start += 5
            end += 5
            pprint(df.iloc[start:end].to_dict(orient="records"), indent=2)
        else:
            return


def tabular_representation(column_headers, data=None):
    """Displays data in tabular format

    Args:
        (list) column_headers - Table column headers
        (dict) data - dataframe value counts
    
    Returns:
        BeautifulTable object
    """

    table = BeautifulTable()
    table.set_style(BeautifulTable.STYLE_BOX)

    t = table
    t.columns.headers = column_headers
    if data is not None:
        for key, value in data.items():
            t.rows.append([key, value])

    return t
