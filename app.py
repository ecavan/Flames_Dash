import dash
import dash_core_components as dcc
import dash_html_components as html
#from hockey_rink import NHLRink, IIHFRink, NWHLRink
from dash.dependencies import Input, Output
import plotly.express as px
#import matplotlib.pyplot as plt
import pandas as pd 
#import os 
import plotly.graph_objs as go


df = pd.read_csv('olympic_womens_dataset.csv')

df['time'] = df['Clock'].str.split(':')
df['time'] = df['time'].str[0].astype(int)*60 + df['time'].str[1].astype(int)

df.loc[df['Period'] == 1, 'time'] = 3600 - df['time'] 
df.loc[df['Period'] == 2, 'time'] = 3600 - df['time'] + 20*60
df.loc[df['Period'] == 3, 'time'] = 3600 - df['time'] + 20*60*2  
df.loc[df['Period'] == 4, 'time'] = 4500 - df['time'] + 20*60*3 

df.loc[(df['Period'] == 1)&(df.Team == df['Away Team']), 'X Coordinate'] = 200 - df['X Coordinate']
df.loc[(df['Period'] == 3)&(df.Team == df['Away Team']), 'X Coordinate'] = 200 - df['X Coordinate']
df.loc[(df['Period'] == 2)&(df.Team == df['Home Team']), 'X Coordinate'] = 200 - df['X Coordinate']

df.loc[(df['Period'] == 1)&(df.Team == df['Away Team']), 'X Coordinate 2'] = 200 - df['X Coordinate 2']
df.loc[(df['Period'] == 3)&(df.Team == df['Away Team']), 'X Coordinate 2'] = 200 - df['X Coordinate 2']
df.loc[(df['Period'] == 2)&(df.Team == df['Home Team']), 'X Coordinate 2'] = 200 - df['X Coordinate 2']

available_teams = df['Team'].unique()
available_dates = df['game_date'].unique()

app = dash.Dash()
server = app.server

app.layout = html.Div(children=[
    
    html.H1(children='Calgary Flames Hockey Analytics Dashboard!'),
    
    html.Div(children='''This plot enables us to see the shots each team has taken depending on the Period'''),
    
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[{'label': k, 'value': k} for k in available_teams],
        value=['Olympic (Women) - Canada'],
        multi=True
    ),
        
    dcc.Dropdown(
        id='demo-dropdownd',
        options=[{'label': k, 'value': k} for k in available_dates],
        value=['2018-02-11'],
        multi=True
    ),

        
    dcc.Slider(
        id='year-slider',
        min=df['Period'].min(),
        max=df['Period'].max(),
        value=df['Period'].min(),
        marks={
        1: '1st Period',
        2: '2nd Period',
        3: '3rd Period',
        4: 'OT'
    },
        step=None
    ),

    html.Hr(),
    dcc.Graph(id='display-selected-values'),

]),
    
    html.Div(children='''This plots shows the X,Y Coordinates where Passes Happen most often'''),
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown2',
        options=[{'label': k, 'value': k} for k in available_teams],
        value=['Olympic (Women) - Canada'],
        multi=True
    ),
        
    dcc.Dropdown(
        id='demo-dropdownd2',
        options=[{'label': k, 'value': k} for k in available_dates],
        value=['2018-02-11'],
        multi=True
    ),
        
    dcc.Slider(
        id='year-slider2',
        min=df['Period'].min(),
        max=df['Period'].max(),
        value=df['Period'].min(),
        marks={
        1: '1st Period',
        2: '2nd Period',
        3: '3rd Period',
        4: 'OT'
    },
        step=None
    ),

    html.Hr(),
    dcc.Graph(id='display-selected-values2')]),
    
    html.Div(children='''This plots shows which shot types are optimal for each team'''),
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown3',
        options=[{'label': k, 'value': k} for k in available_teams],
        value=['Olympic (Women) - Canada'],
        multi=True
    ),
        
    html.Hr(),
    dcc.Graph(id='display-selected-values3')]),
    
    html.Div(children='''This plots shows the X,Y Coordinates where Takeaways/Puck Recoveries Happen'''),
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown6',
        options=[{'label': k, 'value': k} for k in available_teams],
        value=['Olympic (Women) - Canada'],
        multi=True
    ),
        
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown7',
        options=[{'label': k, 'value': k} for k in available_dates],
        value=['2018-02-11'],
        multi=True
    ),
        
    dcc.Slider(
        id='year-slider3',
        min=df['Period'].min(),
        max=df['Period'].max(),
        value=df['Period'].min(),
        marks={
        1: '1st Period',
        2: '2nd Period',
        3: '3rd Period',
        4: 'OT'
    },
        step=None
    ),

    html.Hr(),
    dcc.Graph(id='display-selected-values5')])
    
])
])

@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value'),
     dash.dependencies.Input('demo-dropdownd', 'value'),
    dash.dependencies.Input('year-slider', 'value')])

def update_output(value,value2,value3):
    ts = df[(df["Team"].isin(value))&(df.Event == 'Shot')&(df.Period == value3)]
    ts = ts[ts.game_date.isin(value2)]
    
    ts2 = df[(df["Team"].isin(value))&(df.Event == 'Goal')&(df.Period == value3)]
    ts2 = ts2[ts2.game_date.isin(value2)]
    fig = px.scatter(ts, x="X Coordinate", y="Y Coordinate", color = "Team", title = 'Shot Plot For Each Period')
    fig.add_scatter(x=ts2["X Coordinate"], y=ts2["Y Coordinate"], mode='markers', name="Goals")
    
    return fig


@app.callback(
    dash.dependencies.Output('display-selected-values2', 'figure'),
    [dash.dependencies.Input('demo-dropdown2', 'value'),
    dash.dependencies.Input('year-slider2', 'value'),
    dash.dependencies.Input('demo-dropdownd2', 'value')])


def update_output(value,value2,value3):
    ts = df[(df["Team"].isin(value))&(df.Event == 'Play')&(df.Period == value2)]
    ts = ts[ts.game_date.isin(value3)]
    ts = ts.dropna(subset = ["X Coordinate 2"])

    fig1 = px.line(ts, x="X Coordinate", y="Y Coordinate")
    fig4 = px.line(ts, x="X Coordinate 2", y="Y Coordinate 2")
    fig2 = px.scatter(ts, x="X Coordinate", y="Y Coordinate", color_discrete_sequence=['red'])
    fig3 = px.scatter(ts, x="X Coordinate 2", y="Y Coordinate 2", color_discrete_sequence=['red'])
    
    fig = go.Figure(data=fig1.data + fig2.data + fig3.data + fig4.data)
    fig.update_layout(title = 'Pass Plot by Period', xaxis_title="X Coordinate",
    yaxis_title="Y Coordinate")

    return fig

@app.callback(
    dash.dependencies.Output('display-selected-values3', 'figure'),
    [dash.dependencies.Input('demo-dropdown3', 'value')])

def update_output(value):    
    df.loc[(df['Home Team'].isin(value)), 'goals'] = df['Home Team Goals']
    df.loc[( df['Home Team'].isin(value)), 'goals'] = df['Away Team Goals']
    
    df_c = df[df.Team.isin(value)]

    df_shot = df_c[df_c.Event == 'Shot']
    
    df_shot = df_shot[df_shot.Team.isin(value)]
    
    fig = px.sunburst(df_shot, path=['Detail 1', 'Detail 2'], values='goals', title="Shooting Profile by Shot Type")
    return fig
    


@app.callback(
    dash.dependencies.Output('display-selected-values5', 'figure'),
    [dash.dependencies.Input('demo-dropdown6', 'value'),
    dash.dependencies.Input('demo-dropdown7', 'value'),
    dash.dependencies.Input('year-slider3', 'value')])


def update_output(value,value2, value3):
    
    ts = df[(df.Event == 'Puck Recovery')&(df.Team.isin(value))&(df.Period == value3)]
    ts = ts[ts.game_date.isin(value2)]
    
    ts2 = df[(df.Event == 'Takeaway')&(df.Team.isin(value))&(df.Period == value3)]
    ts2 = ts2[ts2.game_date.isin(value2)]

    fig = px.scatter(ts, x="X Coordinate", y="Y Coordinate", color = "Team", title = 'Recoveries/ Takeaways by Team')
    fig.add_scatter(x=ts2["X Coordinate"], y=ts2["Y Coordinate"], mode='markers', name="Takeaway",  text=ts2["Team"])
    
    return fig

if __name__ == '__main__':
    app.run_server()
