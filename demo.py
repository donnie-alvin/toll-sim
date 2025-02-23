import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import random
import datetime
import numpy as np
from dash.dependencies import Input, Output

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the dataset (or generate synthetic data)
url = "https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv"
df = pd.read_csv(url)

# Sample Data Generation for Revenue (you can replace it with actual data)
time_series = [datetime.datetime.now() - datetime.timedelta(minutes=i * 10) for i in range(144)]
revenue_series = np.cumsum(np.random.randint(5, 20, size=144))  # Simulated cumulative revenue
df_revenue = pd.DataFrame({"Time": time_series, "Revenue": revenue_series})

# Sample Vehicle Type Data
vehicle_types = ["Car", "Truck", "Bus", "Motorcycle"]
vehicle_counts = [random.randint(20, 100) for _ in vehicle_types]

# App Layout
app.layout = html.Div([
    html.H1("Live Traffic and Revenue Dashboard"),
    dcc.Interval(id="interval-update", interval=5000, n_intervals=0),  # Updates every 5 seconds

    # Live Traffic Count Display
    html.Div([
        html.H3("Current Traffic Volume"),
        html.H2(id="live-traffic", style={"color": "blue"}),
    ], style={"textAlign": "center", "margin": "20px"}),

    # Revenue vs. Time Line Chart
    dcc.Graph(id="revenue-chart"),

    # Vehicle Type Distribution Pie Chart
    dcc.Graph(id="vehicle-pie-chart"),

    # Traffic Heatmap by Hour
    dcc.Graph(id="traffic-heatmap"),
])

# Live Traffic Counter (Random for Demo)
@app.callback(
    Output("live-traffic", "children"),
    Input("interval-update", "n_intervals")
)
def update_traffic(n):
    return f"{random.randint(100, 500)} vehicles/hour"

# Revenue vs. Time Line Chart (Dynamic)
@app.callback(
    Output("revenue-chart", "figure"),
    Input("interval-update", "n_intervals")
)
def update_revenue_chart(n):
    fig = px.line(df_revenue, x="Time", y="Revenue", title="Revenue Over Time")
    fig.update_xaxes(rangeslider_visible=True)
    return fig

# Vehicle Type Distribution (Dynamic Pie Chart)
@app.callback(
    Output("vehicle-pie-chart", "figure"),
    Input("interval-update", "n_intervals")
)
def update_vehicle_chart(n):
    vehicle_counts = [random.randint(20, 100) for _ in vehicle_types]
    fig = px.pie(names=vehicle_types, values=vehicle_counts, title="Vehicle Type Distribution")
    return fig

# Traffic Heatmap (Dynamic)
@app.callback(
    Output("traffic-heatmap", "figure"),
    Input("interval-update", "n_intervals")
)
def update_heatmap(n):
    hours = list(range(24))
    traffic_counts = np.random.randint(50, 500, size=24)
    fig = px.imshow([traffic_counts], labels={"x": "Hour of Day", "y": "Traffic Volume"},
                    x=hours, y=["Traffic"])
    fig.update_layout(title="Traffic Volume by Hour")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
