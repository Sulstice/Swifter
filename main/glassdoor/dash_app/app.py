# -*- coding: utf-8 -*-
#
# Start scraping data.
#
# ------------------------------------------------

# imports
# -------
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

def generate_table(dataframe, max_rows=1000):

    """

    Arguments:
        dataframe (Pandas DF): the dataframe of the collected data

    Return:
        html (object): runs the html
    """
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def company_data_converison(dataframe):
    """

    Arguments
        dataframe (Pandas DF): scraped job data
    Returns:
        job_frequency_dataframe (Object): dataframe of most frequent companies posting for job listing.

    """

    # dropna handles any weird edges cases in the data that is "Null, NaN, or None"
    job_frequency_dataframe = dataframe['Company'].value_counts(dropna=False)

    return job_frequency_dataframe

if __name__ == '__main__':
    df = pd.read_csv(
        '/local/Swifter/main/jobs.csv')

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    dataframe = company_data_converison(df)
    print (dataframe)

    # Parse the Dash App to only use local files TODO: download that css file labeled above
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets,  requests_pathname_prefix='/dash/')
    app.config.requests_pathname_prefix = ""
    app.scripts.config.serve_locally = True
    app.css.config.serve_locally = True

    app.layout = html.Div([
        dcc.Graph(
            id='job_postings',
            figure={
                'data': [
                    go.Scatter(
                        x=dataframe['Company'],
                        y=dataframe['Length'],
                        text=dataframe['Company'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df['Company'].unique()
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Number of Positions'},
                    yaxis={'title': 'Company'},
                    hovermode='closest'
                )
            }
        )
    ])

    app.run_server(debug=True, threaded=True)
