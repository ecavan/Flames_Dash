import dash
import dash_core_components as dcc
import dash_html_components as html
#from hockey_rink import NHLRink, IIHFRink, NWHLRink
from dash.dependencies import Input, Output
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd 
import os 
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


#fig = px.density_heatmap(df, x="X Coordinate", y="Y Coordinate", color = "Team")

app = dash.Dash()
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
    
    html.Div(children='''Analytics to help Creators grow their engagements'''),
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown2',
        options=[{'label': k, 'value': k} for k in available_teams],
        value=['Olympic (Women) - Canada'],
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
    
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown3',
        options=[{'label': k, 'value': k} for k in available_teams],
        value=['Olympic (Women) - Canada'],
        multi=True
    ),
        
    html.Hr(),
    dcc.Graph(id='display-selected-values3')]),
    
    
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown4',
        options=[{'label': k, 'value': k} for k in available_teams],
        value=['Olympic (Women) - Canada'],
        multi=True
    ),
        
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown5',
        options=[{'label': k, 'value': k} for k in available_dates],
        value=['2018-02-11'],
        multi=True
    ),

    html.Hr(),
    dcc.Graph(id='display-selected-values4')])
    
]),
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
    dash.dependencies.Input('year-slider', 'value')])

def update_output(value,value2):
    ts = df[(df["Team"].isin(value))&(df.Event == 'Shot')&(df.Period == value2)]
    fig = px.scatter(ts, x="X Coordinate", y="Y Coordinate", color = "Team", title = 'Shot Plot For Each Period')
    return fig


@app.callback(
    dash.dependencies.Output('display-selected-values2', 'figure'),
    [dash.dependencies.Input('demo-dropdown2', 'value'),
    dash.dependencies.Input('year-slider2', 'value')])


def update_output(value,value2 ):
    ts = df[(df["Team"].isin(value))&(df.Event == 'Play')&(df.Period == value2)]
    ts = ts.dropna(subset = ["X Coordinate 2"])
    fig = px.density_heatmap(ts, x="X Coordinate 2", y="Y Coordinate 2", title = 'Pass Plot Heatmap')
    return fig

@app.callback(
    dash.dependencies.Output('display-selected-values3', 'figure'),
    [dash.dependencies.Input('demo-dropdown3', 'value')])

def update_output(value):
#     df.loc[(df.Event == 'Shot')&(df['Detail 2'] == 'On Net')&(df.Team == df['Home Team']), 'home_shot'] = 1
#     df.loc[(df.Event == 'Shot')&(df['Detail 2'] == 'On Net')&(df.Team == df['Away Team']), 'away_shot'] = 1

#     df.loc[(df.Team == df['Home Team']), 'shots'] = df['home_shot']
#     df.loc[(df.Team == df['Away Team']), 'shots'] = df['away_shot']
    
    df.loc[(df['Home Team'] == 'Olympic (Women) - Canada'), 'goals'] = df['Home Team Goals']
    df.loc[( df['Home Team'] == 'Olympic (Women) - Canada'), 'goals'] = df['Away Team Goals']
    
    df_c = df[df.Team == 'Olympic (Women) - Canada']

#    df_c['SOG'] = df_c.groupby(['Team'])['shots'].transform('sum')


    df_shot = df_c[df_c.Event == 'Shot']


#    gb = (df_shot.groupby(['Team', 'Detail 1'])['goals'].sum())/df_shot.groupby(['Team', 'Detail 1'])['SOG'].sum()
#    gb = gb.reset_index(name = 'Shooting %')
    #gb_team = gb[gb.Team == value]
    
#    df_shot = df_shot.merge(gb, on = ['Team', 'Detail 1'])
    
    df_shot = df_shot[df_shot.Team == 'Olympic (Women) - Canada']
    
    fig = px.sunburst(df_shot, path=['Detail 1', 'Detail 2'], values='goals', title="Shooting Profile by Shot Type")
    return fig
    
    
@app.callback(
    dash.dependencies.Output('display-selected-values4', 'figure'),
    [dash.dependencies.Input('demo-dropdown4', 'value'),
    dash.dependencies.Input('demo-dropdown5', 'value')])


def update_output(value,value2):
    df_cm = df[(df.Event == 'Shot')&(df['Detail 2'] == 'On Net')&(df.Team == 'Olympic (Women) - Canada')&(df.game_date == '2018-02-11')]
    df_cm.loc[(df_cm.Event == 'Shot')&(df_cm['Detail 2'] == 'On Net'), 'shot'] = 1
    df_cm = df_cm.sort_values('time')

    df_cm['Shots on Goal'] = df_cm['shot'].cumsum()
    fig = px.line(df_cm, x='time', y="Shots on Goal", title="Culmative Shots over Time")
    
    return fig


@app.callback(
    dash.dependencies.Output('display-selected-values5', 'figure'),
    [dash.dependencies.Input('demo-dropdown6', 'value'),
    dash.dependencies.Input('demo-dropdown7', 'value'),
    dash.dependencies.Input('year-slider3', 'value')])


def update_output(value,value2, value3):
    ts = df[(df.Event == 'Puck Recovery')&(df.Team == 'Olympic (Women) - Canada')&(df.Period == value3)&(df.game_date == '2018-02-11')]
    ts2 = df[(df.Event == 'Takeaway')&(df.Team == 'Olympic (Women) - Canada')&(df.Period == value3)&(df.game_date == '2018-02-11')]
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ts["X Coordinate"],
            y=ts["Y Coordinate"],
            mode='markers',
            name = 'Puck Recovery'
        ))

    fig.add_trace(
        go.Scatter(
            x=ts2["X Coordinate"],
            y=ts2["Y Coordinate"],
            mode='markers',
            name = 'Takeaways'
        ))
    fig.update_layout(title = 'Recoveries/ Takeaways by Team')
    return fig

if __name__ == '__main__':
    #app.run_server(host='0.0.0.0', port=8050, debug=False)
    app.run_server(debug=True)
