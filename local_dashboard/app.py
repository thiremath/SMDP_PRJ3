from flask import Flask, render_template, jsonify
import pandas as pd
from dash import Dash, dcc, html

# Initialize Flask app
app = Flask(__name__)

# Load datasets
reddit_data = pd.read_csv('data/reddit_data.csv')
chan_data = pd.read_csv('data/chan_data.csv')
merged_data = pd.merge(reddit_data, chan_data, on='date', how='outer')

# Initialize Dash app
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Dash layout
dash_app.layout = html.Div([
    html.H1("Post Count Analysis", style={'text-align': 'center'}),
    dcc.Graph(
        id='time-series-chart',
        figure={
            'data': [
                {'x': merged_data['date'], 'y': merged_data['reddit_count'], 'type': 'line', 'name': 'Reddit'},
                {'x': merged_data['date'], 'y': merged_data['chan_count'], 'type': 'line', 'name': '4chan'},
            ],
            'layout': {'title': 'Posts Over Time'}
        }
    )
])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify(merged_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
