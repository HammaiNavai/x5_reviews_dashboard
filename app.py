from typing import Tuple
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc, dash_table
from dash.dependencies import Output, Input
import plotly.graph_objects as go

import pandas as pd 
from figures import get_map_shops, get_indicator, get_line_plots, get_top_topics_plot, get_count_topics_plot, get_best_indicators, get_worst_indicators
import config

app = dash.Dash(external_stylesheets=["html-components.css", dbc.themes.BOOTSTRAP])

main_header = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            html.Label(
                "X5// REVIEWS",
                style={
                    'font-size': config.fonts['header'],
                    'color': config.colors['header'],
                    'text-align': 'left',
                    'margin-left': '32px',
                    }
                )
            ]),
    ], style={
        'color': config.colors['card'], 
        'margin-top': '8px',

    }) 
], color = config.colors['card'], style={
    'border': '#FFFFFF',         
    'margin-bottom': '8px'})

filter_map = dbc.Col([
    dbc.Label(
        "Выберите магазины",
        html_for="map_filter_dropdown",
        style = {
            'font-size': config.fonts['text'], 
            'color': '#000000'
            }
        ),
    dcc.Dropdown(
        id="map_filter_dropdown",
        placeholder='Все магазины сети',
        value='Все магазины сети',
        options=['Все магазины сети', 'Пятёрочка', 'Перекрёсток'])
], style={
    'max-width': '100%',
    'color': '#000000'}
)

filter_city = dbc.Col([
    dbc.Label(
        "Выберите город",
        html_for="city_filter_dropdown",
        style = {
            'font-size': config.fonts['text'], 
            'color': '#000000'
            }
        ),
    dcc.Dropdown(
        id="city_filter_dropdown",
        placeholder='Санкт-Петербург',
        value='Санкт-Петербург',
        options=['Санкт-Петербург'])
], style={
    'max-width': '100%',
    'color': '#000000'}
)

filter_subject = dbc.Col([
    dbc.Label(
        "Выберите район",
        html_for="subject_filter_dropdown",
        style = {
            'font-size': config.fonts['text'], 
            'color': '#000000'
            }
        ),
    dcc.Dropdown(
        id="subject_filter_dropdown",
        placeholder='Центральный район',
        value='Центральный район',
        options=['Центральный район'])
], style={
    'max-width': '100%',
    'color': '#000000'}
)

indicator_header = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label(
                    "Изменения рейтинга",
                    style={
                        'font-size': config.fonts['h2'],
                        'color': '#000000',
                        'text-align': 'left'
                    }),
                html.Br(),
                html.Label(
                    "Самые значительные изменения по категориям за неделю",
                    style={
                        'font-size': config.fonts['text'],
                        'text-align': 'left',
                        'color': '#000000'
                    },
                ),
            ], width=6),
            dbc.Col(filter_city, width=2),
            dbc.Col(filter_subject, width=2),
            dbc.Col(filter_map, width=2),
        ]),
    ], style={
        'height': '6rem',
        'color': '#FFFFFF',
    }) 
], color = '#FFFFFF', style={'border': '#FFFFFF'})

ind_header_row = dbc.Row([
    dbc.Col([indicator_header], width=12)
], style={'marginLeft': '9px', 'margin-bottom': '16px'})

indicators1 = dbc.Card([
    dcc.Graph(
        id='indicators1',
        style={
            'height':220
            }),
    dcc.Graph(
        id='indicators2',
        style={
            'height':220
            })
], style={'border': '#135c11', 'margin-left': '32px'})

indicator = dbc.Card([
    dcc.Graph(
        id='indicator',
        style={'height': 180, 'width': 410})
], style={'border': '#000000', 'margin-left': '16px'})

plot_plot = dbc.Card([
    dcc.Graph(
        id='lines_plot',
        style={
            'height': 250, 
            'width': 410})
], style={'border': '#135c11', 'margin-left': '16px'})

indicators_card = dbc.Row([
            dbc.Col([indicators1
            ], width=8),
            dbc.Col([
                dbc.Row([indicator]),
                dbc.Row([plot_plot])
            ], width=4),
        ])


map_header = dbc.Card([
    dbc.CardBody([
                html.Label(
                    "Рейтинг магазинов сети на карте по каждой категории",
                    style={
                        'font-size': config.fonts['h2'],
                        'color': '#000000',
                        'text-align': 'left'
                    }),
                html.Br(),
                html.Label(
                    "Ниже отображены магазины сети на карте, цвет магазина зависит от его рейтинга в выбранной категории",
                    style={
                        'font-size': config.fonts['text'],
                        'text-align': 'left',
                        'color': '#000000'
                    },
                ),
    ], style={
        'height': '6rem',
        'color': '#FFFFFF',
    }) 
], color = '#FFFFFF', style={'border': '#FFFFFF'})

def get_labels(label: str, column_name: str) -> dict:
    """ Создание лейблов для фильтров """
    return {'label': label, 'value': column_name}

topics = [get_labels(config.translation_dict[key], key) for key in config.translation_dict.keys()] 

topics_filter = dbc.Col([
    dbc.Label(
        "Выберите категорию",
        html_for="topics_dropdown",
        style = {
            'font-size': config.fonts['text'], 
            'color': '#000000'
        }
        ),
    dcc.Dropdown(
        id="topics_dropdown",
        placeholder='Категории',
        value='Cleanliness',
        options=topics),
], style={
    'max-width': '100%',
    'color': '#000000'}
)

addresses_df = pd.read_csv('data/data_week2.csv')
addresses = addresses_df['address'].unique()

address_filter = dbc.Col([
    dbc.Label(
        "Ввведите адрес магазина",
        html_for="address_dropdown",
        style = {
            'font-size': config.fonts['text'], 
            'color': '#000000'
        }
        ),
    dcc.Dropdown(
        id="address_dropdown",
        multi=True,
        placeholder='Адрес магазинов'),
], style={
    'max-width': '100%',
    'color': '#000000'}
)
map_header_row = dbc.Row([
    dbc.Col([map_header], width=6),
    dbc.Col([topics_filter], width=3),
    dbc.Col([address_filter], width=3)
], style={'marginLeft': '16px', 'margin-bottom': '16px', 'margin-right': '16px'})

map_plot = dbc.Card([
    dcc.Graph(
        id='map',
        style={
            'height':580
            })
], style={'border': '#135c11', 'margin-left': '32px', 'margin-right': '8px'})

topic_table = dbc.Card([
    dash_table.DataTable(
        id='topic_data',
        sort_action='native',
        fixed_rows={'headers': True},
        style_table={'overflowY': 'auto', 'minWidth': '100%'},
        style_data={'font-family': config.fonts['family']},
        style_header={
            'font-family': config.fonts['family'],
            'backgroundColor': '#f0f0f0',
            'font_color': '#000000',
            'font_size': 13,
            'border': '10px #333333',
            'height': 50,
            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
            },
        fixed_columns={'headers': True, 'data': 1},
        style_cell={
            'height': 50,
            'minWidth': '50px', 'width': '150px', 'maxWidth': '150px',
            'whiteSpace': 'normal',
            'font_size': 13,
        },
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Рейтинг магазина,%} > 0 && {Рейтинг магазина,%} < 50',
                    'column_id': 'Рейтинг магазина,%'
                },
                'backgroundColor': '#ff6038',
                'color': 'white',
                'font_size': 13
            },
            {
                'if': {
                    'filter_query': '{Рейтинг магазина,%} > 49 && {Рейтинг магазина,%} < 70',
                    'column_id': 'Рейтинг магазина,%'
                },
                'backgroundColor': '#f79525',
                'color': 'white',
                'font_size': 13
            },
            {
                'if': {
                    'filter_query': '{Рейтинг магазина,%} > 69 && {Рейтинг магазина,%} < 101',
                    'column_id': 'Рейтинг магазина,%'
                },
                'backgroundColor': '#7ba346',
                'color': 'white',
                'font_size': 13
            },
            {
                'if': {
                'column_type': 'text'  
            },
            'textAlign': 'left'
            },
            {
                'if': {
                'column_type': 'numeric' 
            },
            'textAlign': 'center'
            }
        ]
        ),
], style={'margin-left': '8px', 'margin-right': '32px'})

map_plot_card = dbc.Row([
            dbc.Col([map_plot], width=6),
            dbc.Col([topic_table], width=6)
        ])

competitor_header = dbc.Card([
    dbc.CardBody([
                html.Label(
                    "Сравнение с конкурентами рядом",
                    style={
                        'font-size': config.fonts['h2'],
                        'color': '#000000',
                        'text-align': 'left'
                    }),
                html.Br(),
                html.Label(
                    "Ниже отображены магазины сети на карте, цвет магазина зависит от его рейтинга в выбранной категории",
                    style={
                        'font-size': config.fonts['text'],
                        'text-align': 'left',
                        'color': '#000000'
                    },
                ),
    ], style={
        'height': '6rem',
        'color': '#FFFFFF',
    }) 
], color = '#FFFFFF', style={'border': '#FFFFFF'})

competitor_header_row = dbc.Row([
    dbc.Col([competitor_header], width=12),
], style={'marginLeft': '16px', 'margin-bottom': '16px', 'margin-right': '16px'})

# competitor_filter = dbc.Col([
#     dbc.Label(
#         "Выберите конкурента",
#         html_for="сompetitor_filter_dropdown",
#         style = {
#             'font-size': config.fonts['text'], 
#             'color': '#000000'
#             }
#         ),
#     dcc.Dropdown(
#         id="сompetitor_filter_dropdown",
#         placeholder='Выберите конкурента',
#         value='',
#         clearable=True,
#         options=['Все конкуренты', 'Магнит', 'Дикси'])
# ], style={
#     'max-width': '100%',
#     'color': '#000000'}
# )

# comparing_header = dbc.Card([
#     dbc.CardBody([
#         dbc.Row([
#             dbc.Col([
#                 html.Label(
#                     "Краткая сводка и сравнение с конкурентами",
#                     style={
#                         'font-size': config.fonts['h2'],
#                         'color': '#000000',
#                         'text-align': 'left'
#                     }),
#                 html.Br(),
#                 html.Label(
#                     "Здесь можно увидеть, что больше всего нравится и не нравится покупателям",
#                     style={
#                         'font-size': config.fonts['text'],
#                         'text-align': 'left',
#                         'color': '#000000'
#                     },
#                 ),
#             ], width=8),
#             dbc.Col(competitor_filter, width=4),
#         ]),
#     ], style={
#         'height': '6rem',
#         'color': '#FFFFFF',
#     }) 
# ], color = '#FFFFFF', style={'border': '#FFFFFF'})

# comparing_header_row = dbc.Row([
#     dbc.Col([comparing_header], width=12)
# ], style={'marginLeft': '9px', 'margin-bottom': '16px'})

comparing_plot1 = dbc.Card([
    dcc.Graph(
        id='comparing_plot1',
        style={
            'height':500
            })
], style={'border': '#135c11', 'margin-left': '32px'})

comparing_plot2 = dbc.Card([
    dcc.Graph(
        id='comparing_plot2',
        style={
            'height':500
            })
], style={'border': '#135c11', 'margin-left': '32px'})

comparing_plot_card = dbc.Row([
            dbc.Col([comparing_plot1], width=6),
            dbc.Col([comparing_plot2], width=6),
            # dbc.Col([comparing_plot2], width=6),
        ])


analytics = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label(
                    "Сравнение с конкурентами рядом",
                    style={
                        'font-size': config.fonts['h2'],
                        'color':  '#000000',
                        'text-align': 'left'
                    },
                    ),
                html.Br(),
                html.Label(
                    "Здесь можно увидеть скор магазинов сети",
                    style={
                        'font-size': config.fonts['text'],
                        'text-align': 'left',
                        'color': '#000000'
                    },
                ),
            ], width=8, style={'margin-left': '16px'}),
            dbc.Col([], width=4)
        ]),
    ], style={
        'height': '6rem',
        'color': '#FFFFFF',
    }) 
], color ='#FFFFFF', style={'border': '#FFFFFF'})

table = dbc.Row([
    dash_table.DataTable(
        id='data',
        sort_action='native',
        fixed_rows={'headers': True},
        style_table={'overflowY': 'auto', 'minWidth': '100%'},
        style_data={'font-family': config.fonts['family']},
        style_header={
            'font-family': config.fonts['family'],
            'backgroundColor': '#f0f0f0',
            'font_color': '#000000',
            'font_size': 13,
            'border': '10px #333333',
            'height': 60,
            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
            },
        fixed_columns={'headers': True, 'data': 1},
        style_cell={
            'height': 60,
            'minWidth': '50px', 'width': '150px', 'maxWidth': '150px',
            'whiteSpace': 'normal',
            'font_size': 13,
        },
        # style_data_conditional=[{
        #     'if': {'column_id': 'Номер скважины'},
        #     'backgroundColor': '#f0f0f0',
        # }],
        ),
], style={'margin-top': '16px', 'margin-left': '16px', 'margin-right': '16px', 'margin-bottom': '16px'})



app.layout = html.Div(
    style={
        'margin-left': '0px',
        'margin-right': '0px',
        'margin-top': '0px',
        'margin-bottom': '0px',
        'font-family': config.fonts['family'],
        'backgroundColor': '#ffffff'}, 
    children=[
        dbc.Row([main_header]),
        ind_header_row,
        indicators_card,
        map_header_row,
        map_plot_card,
        competitor_header_row,
        # comparing_plot_card,
        dbc.Row([analytics]),
        table,
        
        dbc.Row([
            dbc.Col([], width = 9),
            dbc.Col([], width=3)
        ], style = {'margin-bottom': '0px'}),
        ]
    )

#============================================================================================================================
# CALL_BACKS

@app.callback(
    Output('indicators1', 'figure'),
    Output('indicators2', 'figure'),

    Input('map_filter_dropdown', 'value')
)
def indicators(shops: list):

    fig1 = get_best_indicators(shops)
    fig2 = get_worst_indicators(shops)

    return fig1, fig2

@app.callback(
    Output('indicator', 'figure'),
    Output('lines_plot', 'figure'),

    Input('map_filter_dropdown', 'value')
)
def shops_map(shops: list):


    indicator = get_indicator(shops)
    fig = get_line_plots(shops)

    return indicator, fig

@app.callback(
    Output('comparing_plot1', 'figure'),
    Output('comparing_plot2', 'figure'),

    Input('map_filter_dropdown', 'value'),
    Input('сompetitor_filter_dropdown', 'value')
)
def comparing_plots(shops, competitor):

    fig1 = get_top_topics_plot(shops, competitor)
    fig2 = get_count_topics_plot(shops, competitor)

    return fig1, fig2


@app.callback(
    Output('data', 'data'),

    Input('map_filter_dropdown', 'value'),
)
def table(shops: str):
    data = pd.read_csv('data/best_worst.csv')
    data = data[data['Магазин'].isin(config.shops[shops])]
    data = data.to_dict('records')
    
    return  data

@app.callback(
    Output('map', 'figure'),

    Input('map_filter_dropdown', 'value'),
    Input('topics_dropdown', 'value'),
    Input('address_dropdown', 'value'),
)
def map_plot(shops, topic, address):
    
    fig = go.Figure()
    map = get_map_shops(shops, topic, fig, address)
    
    return map
    
@app.callback(
    Output('address_dropdown', 'options'),

    Input('topics_dropdown', 'value'),
    Input('map_filter_dropdown', 'value'),
)
def exist_wells(topic, shops) -> go.Figure:
    adresss = pd.read_csv(f'topic_data_{topic}.csv')
    adresss = adresss[adresss['Название'].isin(config.shops[shops])]
    adresss = adresss['Адрес'].unique()
    
    return  adresss

@app.callback(
    Output('topic_data', 'data'),

    Input('topics_dropdown', 'value'),
    Input('map_filter_dropdown', 'value'),
    Input('address_dropdown', 'value'),
)
def table(topic, shops, address):
    if address == None or address == []:
        data_week2 = pd.read_csv(f'topic_data_{topic}.csv')
        topic_data = data_week2.copy()
        topic_data = topic_data[topic_data['Название'].isin(config.shops[shops])]
    else:    
        data_week2 = pd.read_csv(f'topic_data_{topic}.csv')
        topic_data = data_week2.copy()
        topic_data = topic_data[topic_data['Название'].isin(config.shops[shops])]
        topic_data = topic_data[topic_data['Адрес'].isin(address)]
        
    topic_data = topic_data.fillna(0)
    topic_data = topic_data[['Название', 'Адрес', 'Рейтинг магазина,%', 'Количество отзывов']]
    topic_data = topic_data[topic_data['Количество отзывов']!=0]
    topic_data = topic_data.sort_values(by='Адрес')
    topic_data = topic_data.to_dict('records')
    
    return  topic_data

app.config['suppress_callback_exceptions'] = True

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
