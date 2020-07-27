import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

from data import DAYS
from helper_functions import load_data


app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("BIKESHARE PROJECT DATA ANALYSIS FOR CITIES OF NEWYORK, CHICAGO, WASHINGTON", style={"text-align": "center"}),
    html.Hr(),
    html.H2("Data filter by: City, Month, and Day"),
    html.Hr(),

    html.H4("Select city from dropdown:"),
    dcc.Dropdown(id="slct_city",
                 options=[
                     {"label": "Chicago", "value": "chicago"},
                     {"label": "New York City", "value": "new york city"},
                     {"label": "Washington", "value": "washington"},
                 ],
                 multi=False,
                 value="chicago",
                 style={"width": "40%"}
    ),

    html.H4("Select Month (January - June):"),
    dcc.Dropdown(id="slct_month",
                 options=[
                     {"label": "January", "value": "january"},
                     {"label": "February", "value": "february"},
                     {"label": "March", "value": "march"},
                     {"label": "April", "value": "april"},
                     {"label": "May", "value": "may"},
                     {"label": "June", "value": "june"},
                     {"label": "All", "value": "all"},
                 ],
                 multi=False,
                 value="all",
                 style={"width": "40%"}
    ),

    html.H4("Select Day (Monday - Sunday):"),
    dcc.Dropdown(id="slct_day",
                 options=[
                     {"label": "Monday", "value": "Mon"},
                     {"label": "Tuesday", "value": "Tue"},
                     {"label": "Wednesday", "value": "Wed"},
                     {"label": "Thursday", "value": "Thu"},
                     {"label": "Friday", "value": "Fri"},
                     {"label": "Saturday", "value": "Sat"},
                     {"label": "Sunday", "value": "Sun"},
                     {"label": "All", "value": "all"},
                 ],
                 multi=False,
                 value="all",
                 style={"width": "40%"}
    ),
    html.Hr(),

    html.Div(id="output_container", children=[]),
    html.Br(),

    dcc.Graph(id="trip_graph", figure={})
    
])


@app.callback(
    [Output(component_id="output_container", component_property="children"),
     Output(component_id="trip_graph", component_property="figure")],
    [Input(component_id="slct_city", component_property="value"),
     Input(component_id="slct_month", component_property="value"),
     Input(component_id="slct_day", component_property="value")]
)
def update_data_selection(city, month, day):
    container = f"Select city: {city.capitalize()}, Month of {month.capitalize()} and Day of Week: {DAYS.get(day, 'All')}"

    # import csv data into pandas
    df = load_data(city, "all", "all")
    df["Start - End Stations"] = df["Start Station"] + " and " + df["End Station"]
    
    # Group data by month and days of the week and find mean trip duration.
    dff = df.copy()
    dff = dff.groupby(["month", "day_of_week"])[["Trip Duration"]].mean()
    dff.reset_index(inplace=True)

    if day != 'all':
        day = DAYS[day.title()]
        dff = dff[dff["day_of_week"] == day]

    # Plotly express
    fig = px.bar(
        data_frame=dff,
        x="month",
        y="Trip Duration",
        hover_data=["day_of_week", "Trip Duration"],
        labels={"day_of_week": "Day", "month": "Month", "Trip Duration": "Mean Trip Duration"},
        template="seaborn",
        title="City Average Trip Durations in Six Months",
    )

    return container, fig


if __name__ == "__main__":
    app.run_server(debug=True)
