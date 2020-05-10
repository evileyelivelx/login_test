import warnings
# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app

# -----

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import dash

warnings.filterwarnings("ignore")

df = pd.read_csv('complexsite_ext.csv')

sub_set = df.set_index('Location')

sub_set = sub_set.loc[
    ['site1', 'site2', 'site3', 'site4', 'facility1', 'facility2', 'facility3', 'facility4', 'facility5']]

db_site1 = sub_set[sub_set.index == 'site1']
db_site2 = sub_set[sub_set.index == 'site2']
db_facility1 = sub_set[sub_set.index == 'facility1']

trace_total_site1 = go.Bar(
    x=df['Date'],
    y=db_site1['Total'],
    name='Total Number',
    marker_color='rgb(55, 83, 109)'
)

trace_positive_site1 = go.Bar(
    x=df['Date'],
    y=db_site1['Result'],
    name='Positive Number',
    marker_color='rgb(26, 118, 255)'
)

trace_total_site2 = go.Bar(
    x=df['Date'],
    y=db_site2['Total'],
    name='Total',
    marker_color='rgb(55, 83, 109)'
)
trace_positive_site2 = go.Bar(
    x=df['Date'],
    y=db_site2['Result'],
    name='Positive Number',
    marker_color='rgb(26, 118, 255)'
)

trace_positive_facility1 = go.Bar(
    x=df['Date'],
    y=db_facility1['Result'],
    name='Positive Number',
    marker_color='rgb(26, 118, 255)',
)

trace_total_facility1 = go.Bar(
    x=df['Date'],
    y=df['Total'],
    name='Total',
    marker_color='rgb(55, 83, 109)'
)

data_site1 = [trace_positive_site1, trace_total_site1]
data_site2 = [trace_positive_site2, trace_total_site1]
data_facility1 = [trace_positive_facility1, trace_total_facility1]

layout_site1 = dict(title="Site 1 result trend from 2018 January to June",
                    showlegend=True)
layout_site2 = dict(title="Site 2 result trend from 2018 January to June",
                    showlegend=True)
layout_facility1 = dict(title="Facility 1 result trend from 2018 January to June",
                        showlegend=True)

fig_site1 = dict(data=data_site1, layout=layout_site1)
fig_site2 = dict(data=data_site2, layout=layout_site2)
fig_facility1 = dict(data=data_facility1, layout=layout_facility1)

sunburst_df = sub_set[sub_set['Date'] == '2018-06']
fig_sunburst = px.sunburst(sunburst_df, path=['Home', 'Subhome'],
                           color='Result', values='Total', color_continuous_scale='RdBu',
                           color_continuous_midpoint=np.average(sunburst_df['Result'], weights=sunburst_df['Total'])
                           )

treemap_df = sub_set[sub_set['Date'] == '2018-06']
fig_treemap = px.treemap(treemap_df, path=['Home', 'Subhome'],
                         color='Result', color_continuous_scale='RdBu',
                         color_continuous_midpoint=np.average(treemap_df['Result'], weights=treemap_df['Total']))

GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/evileyelivelx/dashapp_microbiology",
)

layout_x = go.Layout(
    showlegend=True,
    autosize=True,
    xaxis=go.XAxis(showticklabels=False),
    yaxis=go.YAxis(showticklabels=False),
    margin=dict(l=10, r=10, b=50, t=20),
    images=[dict(
        source="assets/factorysite.png",
        # positon='middle center',
        xref="x",
        yref="y",
        x=0.75,
        y=35,
        sizex=50,
        sizey=50,
        xanchor='left',
        yanchor='top',
        sizing="contain",
        opacity=1,
        layer="below",

    )])

# Create success layout
layout = html.Div(children=[
    dcc.Location(id='url_login_success', refresh=True),
    html.Div([
        html.Div([
            html.H1(children='Dash - Data Analysis and Visualization for XXX Company',
                    className='nine columns'),
            html.Img(
                src='assets/cawthronlogo.png',
                className='three columns',
                style={
                    'height': '16%',
                    'width': '16%',
                    'float': 'right',
                    'position': 'relative',
                    'padding-top': 12,
                    'padding-right': 0
                }
            ),

            # html.Div(children='''
            #         Data visualization for a site plan with mock data.
            # ''',
            #          className='nine columns')
            html.Div([
                html.H6(
                    "This Dash app is a simple demonstration of the result performance of the production facility in XXX company. "
                    "The dataset consists of 120 observations in the last six months, representing the positive number from "
                    "individual facility. Drag the slider to view the number of positive result in each facility over the last six months, the larger "
                    "circle means the more positive result has been detected. The right side the line chart is representing the trend "
                    "for each site or facility from January 2018 to June 2018."),
            ], className='six columns')
        ], className="row"),

        # Selectors
        html.Div([
            html.Div([
                dcc.Slider(
                    id='dateslider',
                    min=df['Number'].min(),
                    max=df['Number'].max(),
                    value=df['Number'].min(),
                    # marks={str(num): str(num) for num in df['Number'].unique()},
                    marks={
                        0: "2018-Jan",
                        2: "2018-Feb",
                        4: "2018-Mar",
                        6: "2018-Apr",
                        8: "2018-May",
                        10: "2018-Jun"
                    },
                    step=None
                )
            ], className='six columns'),

            html.Div([
                html.P('Select Facility:'),
                dcc.Dropdown(
                    id='site',
                    options=[{'label': str(item),
                              'value': str(item)}
                             for item in set(df['Location'])],
                    multi=True,
                    value=list(set(df['Location']))
                )
            ], className='five columns',
                style={'margin-top': '10'})
        ], className='row'),

        # Site plan + Line chart
        html.Div([
            html.Div([
                dcc.Graph(id='siteplan',
                          animate=True,
                          config={'displayModeBar': True},
                          style={'background': '#0a0000', 'padding-bottom': '10px',
                                 'padding-left': '10px', 'padding-right': '20px',
                                 'height': '60vh', "padding-top": '50px'})
            ], className='six columns'),

            html.Div([
                dcc.Graph(id='linechart',
                          style={'background': '#0a0000', 'padding-bottom': '10px',
                                 'padding-left': '10px', 'padding-right': '20px',
                                 'height': '60vh', "padding-top": '50px'})
            ], className='six columns')
        ]),

        html.Div([
            html.Div([
                dcc.Graph(figure=fig_site1,
                          style={'background': '#0a0000', 'padding-bottom': '10px',
                                 'padding-left': '10px', 'padding-right': '20px',
                                 'height': '60vh', "padding-top": '50px'}),
            ], className='six columns'),

            html.Div([
                dcc.Graph(figure=fig_site2,
                          style={'background': '#0a0000', 'padding-bottom': '10px',
                                 'padding-left': '10px', 'padding-right': '20px',
                                 'height': '60vh', "padding-top": '50px'}),
            ], className='six columns')
        ]),

        html.Div(
            html.Div(
                className="text-padding",
                children=[
                    " *Only site 1 and site 2 present in this dashboard, other sites and facilities' results can be shown as needed"
                ]
            )
        ),

        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='pie-chart',
                        style={'background': '#0a0000', 'padding-bottom': '10px',
                               'padding-left': '10px', 'padding-right': '20px',
                               'height': '60vh', "padding-top": '50px'}
                    ),

                    dcc.Slider(
                        id='pie-slider',
                        min=df['Number'].min(),
                        max=df['Number'].max(),
                        value=4,
                        marks={
                            0: "2018-Jan",
                            2: "2018-Feb",
                            4: "2018-Mar",
                            6: "2018-Apr",
                            8: "2018-May",
                            10: "2018-Jun"
                        },
                        step=None,
                    )

                ], className='seven columns'),

                html.Div([
                    html.P(
                        """Pie Chart shows the positive result on each site or facility from January 2018 to June 2018.\n
                        Select any of the points on the date slider to section data by time. """
                    )
                ], className="four columns div-user-controls")

            ], className="row"),
        ]),

        html.Div(
            className="row",
            children=[
                html.Div(
                    className="text-padding",
                    children=[
                        "Treemap chart"
                    ]
                ),
                html.Div(
                    className="four columns div-user-controls",
                    # children=[
                    #     dcc.Graph(
                    #         figure=fig_sunburst,
                    #     )
                    # ]
                    children=[
                        html.P(
                            # """The Sunburst chart shows hierarchical data for a dataframe,
                            # the parent sites of sunburst sectors (high levels of the hierarchy)
                            # and their daughter facilities (low levels of the hiearchy) in June 2018.
                            # Each daughter facility/site belongs to its parent site.
                            # Move mouth on each sector to see the details."""
                            """The treemap chart shows hierarchical data for a dataframe, 
                            the parent sites of treemap sectors (high level of the hierarchy)
                            and their daughter facilities (low levels of the hiearchy) in June 2018.
                            Each daughter facility/site belongs to its parent site.
                            Move mouth on each sector to see the details"""
                        )
                    ],
                ),
                html.Div(
                    className="seven columns",
                    children=[
                        dcc.Graph(
                            # figure=fig_sunburst,
                            figure=fig_treemap,
                        )
                    ]
                )
            ]),

        html.Div([
            html.Div([
                html.H6("For more information please contact: \ "
                        "Steven.Liu@cawthron.org.nz"),
            ], className='nine columns'),

            html.Div([
                html.A(
                    "View on Steven Liu's GitHub",
                    href=GITHUB_LINK
                )
            ], className='nine columns')
        ])
    ])
])


# Create callbacks
@app.callback(Output('url_login_success', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'


@app.callback(
    Output('siteplan', 'figure'),
    [Input('dateslider', 'value')]
)
def update_figure(selected_num):
    filtered_df = df[df['Number'] == selected_num]
    traces = []
    # fig.add_trace(go.Image(z=img), 1, 1)

    for i in filtered_df['Location'].unique():
        df_location = filtered_df[filtered_df['Location'] == i]
        traces.append(dict(
            x=df_location['Lat'],
            y=df_location['Lon'],
            text=df_location['Result'],
            mode='markers',
            marker={
                'size': df_location['Result'] * 4,
                'color': df_location['Color']
            },
            name=i,
        )
        )

    return {
        'data': traces,
        'layout': layout_x
    }


@app.callback(
    Output('linechart', 'figure'),
    [Input('site', 'value')]
)
def build_linechart(site):
    site_df = df[df['Location'].isin(site)]
    fig = px.line(site_df, x='Date', y='Result', color='Location')
    fig.update_layout(yaxis={'title': 'Positive Result'},
                      title={'text': 'Positive result data in different sites & facilities'})

    return fig


@app.callback(
    Output("pie-chart", 'figure'),
    [Input('pie-slider', 'value')]
)
def update_pie(selected_number):
    return {
        "data": [go.Pie(labels=df['Location'].unique().tolist(),
                        values=df[df['Number'] == selected_number]['Result'].tolist(),
                        hole=0.3,
                        marker={'colors': [df['Color']]})],
        "layout": go.Layout(title=f"Pie Chart Result by Different Zones 2018.01-2019.12",
                            legend={'x': 1,
                                    'y': 0.7},

                            margin={"l": 50, "r": 20},

                            )
    }


