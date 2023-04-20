# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                            options=[{'label': 'All Sites', 'value': 'ALL'}]+[{'label': site, 'value': site} for site in set(spacex_df['Launch Site'])],
                                            value='ALL',
                                            placeholder="Select Site",
                                            searchable=True),
                            
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={ 0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                                        2500: {'label': '2500'},
                                                        5000: {'label': '5000'},
                                                        7500: {'label': '7500'},
                                                        10000: {'label': '10000', 'style': {'color': '#f50'}},},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(filtered_df, 
        names='Launch Site',
        title='Total Success Launches by All Sites')
    else:
        # return the outcomes piechart for a selected site
        site_data = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(site_data,
        names='class', 
        title='Total Success Launches by '+entered_site)
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site, entered_range):
    if entered_site == 'ALL':
        low, high = entered_range
        all_sites = spacex_df
        inrange = (all_sites['Payload Mass (kg)'] > low) & (all_sites['Payload Mass (kg)'] < high)
        fig = px.scatter(all_sites[inrange], x='Payload Mass (kg)', y='class', title = 'Correlation Between Payload and Success for All Sites',
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)'])
    else:
        low, high = entered_range
        all_sites = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        inrange = (all_sites['Payload Mass (kg)'] > low) & (all_sites['Payload Mass (kg)'] < high)
        fig = px.scatter(all_sites[inrange], x='Payload Mass (kg)', y='class', title = 'Correlation Between Payload and Success for the Site '+entered_site,
                color="Booster Version Category",
                size='Payload Mass (kg)',
                hover_data=['Payload Mass (kg)'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
