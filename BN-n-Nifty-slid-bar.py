#! python3
# Libraries
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc, html, Input, Output, Dash
from datetime import datetime, timedelta
import numpy as np


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


my_date = (datetime.now().day)
ymy_date = (datetime.now().year)
mmy_date = (datetime.now().month)

dtsm = [dt.strftime('%H-%M') for dt in
        datetime_range(datetime(ymy_date, mmy_date, my_date, 9, 20), datetime(ymy_date, mmy_date, my_date, 16, 20),
                       timedelta(minutes=5))]

lst = list(range(1, 85))

res = {lst[i]: dtsm[i] for i in range(len(lst))}

range_marks = {1: "9:20", 7: "9:50", 13: "10:20", 19: "10:50", 25: "11:20", 31: "11:50", 37: "12:20", 43: "12:50", 49: "1:20",
               55: "1:50", 61: "2:20", 67: "2:50", 73: "3:00", 79: "3:20", 85: "3:50"}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Use the following function when accessing the value of 'my-slider'
# in callbacks to transform the output value to logarithmic

app.layout = html.Div([

    dcc.Slider(1, 85, 1, marks=range_marks,
               value=25,
               id='my-slider',

               updatemode='drag'

               ),
    html.Div(id='slider-output-container')
])

'''tooltip={"placement": "bottom",
                        "always_visible": False, },'''


@app.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value'))
def update_output(value):
    if value in res.keys():
        value = res[value]
        print(value)
        output = value
        file = open(
            "C:\\Users\\VJN\\Desktop\\Sunny-proj\\web-site-data\\time.txt", "w")
        file.write(output)
        file.close()
    else:
        print("no")
    return 'You have selected Time as:"{}"'.format(value)


if __name__ == '__main__':
    app.run_server()
