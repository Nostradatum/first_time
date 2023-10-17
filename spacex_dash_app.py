import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Read the airline data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Find the maximum and minimum payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Define Booster Version categories based on your criteria
booster_categories = ['v1.0', 'v1.1', 'FT', 'B4', 'B5']

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(id='site-dropdown', options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'CCAFS SLC 40', 'value': 'CCAFS SLC 40'},
        {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'},
        {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'}
    ],
    value='ALL',
    placeholder='Select a Launch Site here',
    searchable=True),
    
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # The pie chart will display Total Success Launches by Site
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    # TASK 3: Add a slider to select payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=spacex_df['Payload Mass (kg)'].min(),
                    max=spacex_df['Payload Mass (kg)'].max(),
                    step=1000,
                    marks={i: str(i) for i in range(int(spacex_df['Payload Mass (kg)'].min()), int(spacex_df['Payload Mass (kg)'].max())+1000, 1000)},
                    value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        df = spacex_df
        title = 'Total Success Launches by Site'
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Total Success Launches for {selected_site}'
    
    site_counts = df[df['class'] == 1]['Launch Site'].value_counts()
    
    pie_chart = px.pie(
        names=site_counts.index,
        values=site_counts.values,
        title=title,
        labels={'names': 'Launch Site'},
    )
    
    return pie_chart

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        df = spacex_df
        title = 'Payload vs. Launch Success for All Sites'
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Payload vs. Launch Success for {selected_site}'
    
    df = df[(df['Payload Mass (kg)'] >= payload_range[0]) & (df['Payload Mass (kg)'] <= payload_range[1])
    
    scatter_chart = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version', title=title)
    
    return scatter_chart

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
