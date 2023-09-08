import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

import config

data = pd.read_csv('data/data.csv')

layout_params = {
    'font_color': '#000000',
    'font_family': 'Avenir Next',
    'font_size': 12,
    'paper_bgcolor': '#ffffff', 
    'plot_bgcolor': '#f0f0f0'
}

def get_map_shops(shops: list, topic: str, fig, address) -> px.scatter_mapbox:

    data_plot = pd.read_csv(f'topic_data_{topic}.csv')
    print(address)
    data_plot = data_plot[data_plot['Название'].isin(config.shops[shops])]
    data_plot['Название'] = data_plot['Название'] + ', ' + data_plot['Адрес']
    data_plot = data_plot.rename(columns={'Рейтинг магазина,%':'Рейтинг, %'})
    if address == None or address == []:
        data_plot_1 = data_plot
    else:
        data_plot_1 = data_plot[data_plot['Адрес'].isin(address)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['1', '2'], y=[1,1]))

    fig = px.scatter_mapbox(
        data_plot_1, 
        lat="Широта", 
        lon="Долгота",
        hover_name='Название',
        color='Рейтинг, %', size="Количество отзывов",
        size_max=30,
        range_color=[data_plot['Рейтинг, %'].min(), data_plot['Рейтинг, %'].max()],
        color_continuous_scale = [(0, '#f0f0f0'),(0.01, '#000000'),(0.6, '#FF3705'), (0.8, '#60A802'), (1, '#60A802')],
        zoom=10, height=500,
    )

    # fig.update_layout(**layout_params).update_layout(
    #     mapbox_style="open-street-map", 
    #     margin={'l': 0, 'r': 40, 't': 0, 'b': 40}, 
    #     hoverlabel=dict(
    #         bgcolor="white",
    #         font_size=12,
    #         font_family="Avenir Next"),
    #     height=500)
    
    # fig = go.Figure()
    
    # fig.add_trace(go.Scattermapbox(
    #         lat=data_plot['Широта'],
    #         lon=data_plot['Долгота'],
    #         mode='markers',
    #         marker=go.scattermapbox.Marker(
    #             size=data_plot['Количество отзывов']/3, color=data_plot['Рейтинг магазина,%'],
    #             colorscale = [(0, '#f0f0f0'),(0.01, '#000000'),(0.6, '#FF3705'), (0.8, '#60A802'), (1, '#60A802')],
    #             ),
            
    #         text=data_plot['Название'],
    #     ))
    fig.update_traces(cluster=dict(enabled=False))
    # fig.add_trace(go.Scattergeo(
    #     lat=data_plot['Широта'],
    #     lon=data_plot['Долгота'],
    #     text=data_plot['name'],
    #     marker = dict(
    #         # size = data_plot['Количество отзывов']/50,
    #         color = data_plot['Рейтинг'],
    #         # size_max=30
    #         # color_continuous_scale = [(0, 'red'), (1, 'green')],
    #     )))

    fig.update_layout(**layout_params).update_layout(
        hovermode='closest',
        mapbox_style="open-street-map", 
        mapbox=dict(
            zoom=10,
            center=go.layout.mapbox.Center(
            lat=data_plot_1['Широта'].mean(),
            lon=data_plot_1['Долгота'].mean()
            ),
        ),
        margin={'l': 0, 'r': 40, 't': 0, 'b': 40}, 
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Avenir Next"),
        
        height=580)
    

    return fig


def get_indicator(name):

    data_week1 = pd.read_csv('data/data_week1.csv')
    data_week2 = pd.read_csv('data/data_week2.csv')

    topics = config.translation_dict.keys()

    grouped_data = data_week1[data_week1['name'].isin(config.shops[name])]
    grouped_data['name'] = name

    values = {}
    for col in topics:
        if len(grouped_data[col].dropna()):
            value = grouped_data[col].dropna().astype('int').mean()
            values[col] = value

    counts = {}
    for col in values.keys():
        if len(grouped_data[f'count_{col}'].dropna()):
            value = grouped_data[f'count_{col}'].dropna().astype('int').sum()
            counts[col] = value
            
    df_plot = pd.DataFrame(columns=['topic', 'value', 'count'])
    df_plot['topic'] = values.keys()
    df_plot['value'] = values.values()
    df_plot['count'] = counts.values()
    df_plot['topic'] = df_plot['topic'].map(config.translation_dict)

    df_plot = df_plot.sort_values('count', ascending=False).reset_index(drop=True)
    df_plot = df_plot.head(20)
    df_plot = df_plot.sort_values(by='value')
    df_plot1  = df_plot 

    grouped_data = data_week2[data_week2['name'].isin(config.shops[name])]
    grouped_data['name'] = name

    values = {}
    for col in topics:
        if len(grouped_data[col].dropna()):
            value = grouped_data[col].dropna().astype('int').mean()
            values[col] = value

    counts = {}
    for col in values.keys():
        if len(grouped_data[f'count_{col}'].dropna()):
            value = grouped_data[f'count_{col}'].dropna().astype('int').sum()
            counts[col] = value
            
    df_plot = pd.DataFrame(columns=['topic', 'value', 'count'])
    df_plot['topic'] = values.keys()
    df_plot['value'] = values.values()
    df_plot['count'] = counts.values()

    df_plot = df_plot.sort_values('count', ascending=False).reset_index(drop=True)
    df_plot = df_plot.head(20)
    df_plot = df_plot.sort_values(by='value')
    df_plot['topic'] = df_plot['topic'].map(config.translation_dict)

    df = df_plot.merge(df_plot1, on='topic', how='outer', suffixes=['1', '2'])
    df.dropna(inplace=True)
    df['change'] = df['value1'] - df['value2']
    
    # df['count2'] = df['count2'].apply(lambda x: x if x < 1000 else int(x / 100))
    # df['count1'] = df['count1'].apply(lambda x: x if x < 1000 else int(x / 100))
    
    value = df['count2'].sum() / 10
    delta = int(value * 0.87)
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        number={'font_color':'black', 'font_size':65},
        value = value,
        title='Новые отзывы за неделю',
        ))

    fig.update_layout(
        
        font_family = 'Avenir Next', font_size=11, 
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        template = {'data' : {'indicator': [{
            'delta' : {'reference': delta, 'increasing': {'color': '#60A802'}, 'decreasing': {'color': '#FF3705'}}}]}})
        
    return fig


def get_line_plots(shops):
    
    dates = pd.date_range(start='09-03-2023', end='09-09-2023', freq='D')  
    positive = config.plot_reviews[shops]['positive']
    negative = config.plot_reviews[shops]['negative']
    neutral = config.plot_reviews[shops]['neutral']
    df = pd.DataFrame(columns=['day', 'p', 'n', 'ne'])
    df['day'], df['p'], df['n'], df['ne'] = dates, positive, negative, neutral
    df['p'] = df['p'] * 11
    df['n'] = df['n'] * 11
    df['ne'] = df['ne'] * 11

    # '#4bbd64''#004f11'
    plot = go.Figure()
    plot.add_trace(
        go.Bar(x=df['day'], y=df['n'], marker_color='#FF3705', name='Негативные', 
    ))
    plot.add_trace(
        go.Bar(x=df['day'], y=df['ne'], marker_color='grey', name='Нейтральные', 
    ))
    plot.add_trace(
        go.Bar(x=df['day'], y=df['p'], marker_color='#60A802', name='Позитивные', 
    ))


    plot.update_layout(**layout_params).update_layout(
        barmode='stack',
        margin={'l': 0, 'r': 0, 't': 10, 'b': 10},
        title={
        'text': 'Динамика за неделю',
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font_size=12,
        legend=dict(orientation="h"),
        )
    
    return plot


def get_top_topics_plot(shops, competitor):
    if competitor == '' or competitor == None:
        data_plot = data.copy()
        topics, topics_count = [], []
        for i in range(len(data_plot)):
            for key in eval(data_plot['topics_rating'][i]).keys():
                topics.append(key)
            
        for i in range(len(data_plot)):
            for key in eval(data_plot['topics_count'][i]).keys():
                topics_count.append(key)
                
        topics, topics_count = set(topics), set(topics_count)
        for col in topics:
            data_plot[col] = data_plot[col].fillna(0)
            data_plot[col] = data_plot[col].astype('int')
            
        name = shops
        grouped_data = data_plot[data_plot['name'].isin(config.shops[name])]
        grouped_data['name'] = name

        grouped_data = grouped_data[['name']+list(topics)].groupby('name').mean().reset_index()
        grouped_data = grouped_data.T
        grouped_data.columns = grouped_data.iloc[0]
        grouped_data = grouped_data.drop(grouped_data.index[0])
        grouped_data = grouped_data[grouped_data[name]!=0]
        grouped_data = grouped_data.reset_index()
        grouped_data[name] = grouped_data[name].astype('float')
        grouped_data = grouped_data.sort_values(by=name)
        grouped_data = grouped_data.tail(10)
        
        fig=go.Figure()
        fig.add_trace(
            go.Bar(
                y=grouped_data['index'], 
                x=grouped_data[name], 
                orientation='h', 
                text=round(grouped_data[name], 2), 
                marker = dict(color=grouped_data[name], colorscale = [(0, '#FF3705'), (0.6, '#64B002'), (1, '#64B002')]),
                name=name
                ))
        fig.update_layout(**layout_params).update_layout(
        title='Что понравилось покупателям, %', 
        height=500, font_size=11,
        margin={'t':40, 'l':30, 'r': 0, 'b': 0},
        plot_bgcolor= '#ffffff',
        legend=dict(orientation="h")
        )
        
    else:
        data_plot = data.copy()
        topics, topics_count = [], []
        for i in range(len(data_plot)):
            for key in eval(data_plot['topics_rating'][i]).keys():
                topics.append(key)
            
        for i in range(len(data_plot)):
            for key in eval(data_plot['topics_count'][i]).keys():
                topics_count.append(key)
                
        topics, topics_count = set(topics), set(topics_count)
        for col in topics:
            data_plot[col] = data_plot[col].fillna(0)
            data_plot[col] = data_plot[col].astype('int')
            
        name = shops
        grouped_data = data_plot[data_plot['name'].isin(config.shops[name])]
        grouped_data['name'] = name

        grouped_data = grouped_data[['name']+list(topics)].groupby('name').mean().reset_index()
        grouped_data = grouped_data.T
        grouped_data.columns = grouped_data.iloc[0]
        grouped_data = grouped_data.drop(grouped_data.index[0])
        grouped_data = grouped_data[grouped_data[name]!=0]
        grouped_data = grouped_data.reset_index()
        grouped_data[name] = grouped_data[name].astype('float')
        grouped_data = grouped_data.sort_values(by=name)
        grouped_data = grouped_data.tail(10)
        
        grouped_competitor = data_plot[data_plot['name'].isin(config.competitors[competitor])]
        grouped_competitor['name'] = competitor

        grouped_competitor = grouped_competitor[['name']+list(topics)].groupby('name').mean().reset_index()
        grouped_competitor = grouped_competitor.T
        grouped_competitor.columns = grouped_competitor.iloc[0]
        grouped_competitor = grouped_competitor.drop(grouped_competitor.index[0])
        grouped_competitor = grouped_competitor[grouped_competitor[competitor]!=0]
        grouped_competitor = grouped_competitor.reset_index()
        grouped_competitor[competitor] = grouped_competitor[competitor].astype('float')
        grouped_competitor = grouped_competitor[grouped_competitor['index'].isin(grouped_data['index'])]

        fig=go.Figure()
        fig.add_trace(
            go.Bar(
                y=grouped_data['index'], 
                x=grouped_data[name], 
                orientation='h', 
                text=round(grouped_data[name], 2), 
                marker = dict(color=grouped_data[name], colorscale = [(0, '#FF3705'), (0.6, '#64B002'), (1, '#64B002')]),
                name=name
                ))

        fig.add_trace(
        go.Bar(
            y=grouped_competitor['index'], 
            x=grouped_competitor[competitor], 
            orientation='h', 
            text=round(grouped_competitor[competitor], 2), 
            name=competitor,
            marker = dict(color='#182859')
            ))
        fig.update_layout(**layout_params).update_layout(
            title='Что понравилось покупателям, %', 
            height=500, font_size=11,
            margin={'t':40, 'l':30, 'r': 0, 'b': 0},
            plot_bgcolor= '#ffffff',
            legend=dict(orientation="h")
            )
    
    return fig


def get_count_topics_plot(shops, competitor):
    if competitor == '' or competitor == None:
        data_plot = data.copy()
        topics, topics_count = [], []
        for i in range(len(data_plot)):
            for key in eval(data_plot['topics_rating'][i]).keys():
                topics.append(key)
            
        for i in range(len(data_plot)):
            for key in eval(data_plot['topics_count'][i]).keys():
                topics_count.append(key)
                
        topics, topics_count = set(topics), set(topics_count)
        for col in topics:
            data_plot[col] = data_plot[col].fillna(0)
            data_plot[col] = data_plot[col].astype('int')
    
        name = shops
        grouped_data = data_plot[data_plot['name'].isin(config.shops[name])]
        grouped_data['name'] = name

        grouped_data = grouped_data[['name']+list(topics_count)].drop_duplicates().groupby('name').sum().reset_index()
        grouped_data = grouped_data.T
        grouped_data.columns = grouped_data.iloc[0]
        grouped_data = grouped_data.drop(grouped_data.index[0])
        grouped_data = grouped_data[grouped_data[name]!=0]
        grouped_data = grouped_data.reset_index()
        grouped_data[name] = grouped_data[name].astype('float')
        grouped_data = grouped_data.sort_values(by=name)
        grouped_data = grouped_data.tail(10)
        
        fig=go.Figure()
        fig.add_trace(
            go.Bar(
                y=grouped_data['index'], 
                x=grouped_data[name], 
                orientation='h', 
                text=round(grouped_data[name], 2), 
                marker = dict(color='#AAFA43'),
                name=name
                ))
        
        fig.update_layout(**layout_params).update_layout(
        title='Количество отзывов в каждом топике', 
        height=500, font_size=11,
        margin={'t':40, 'l':30, 'r': 0, 'b': 0},
        plot_bgcolor= '#ffffff',
        legend=dict(orientation="h")
        )
        
    else: 
        data_plot = data.copy()
        topics, topics_count = [], []
        for i in range(len(data_plot)):
            for key in eval(data_plot['topics_rating'][i]).keys():
                topics.append(key)
            
        for i in range(len(data_plot)):
            for key in eval(data_plot['topics_count'][i]).keys():
                topics_count.append(key)
                
        topics, topics_count = set(topics), set(topics_count)
        for col in topics:
            data_plot[col] = data_plot[col].fillna(0)
            data_plot[col] = data_plot[col].astype('int')
    
        name = shops
        grouped_data = data_plot[data_plot['name'].isin(config.shops[name])]
        grouped_data['name'] = name

        grouped_data = grouped_data[['name']+list(topics_count)].drop_duplicates().groupby('name').sum().reset_index()
        grouped_data = grouped_data.T
        grouped_data.columns = grouped_data.iloc[0]
        grouped_data = grouped_data.drop(grouped_data.index[0])
        grouped_data = grouped_data[grouped_data[name]!=0]
        grouped_data = grouped_data.reset_index()
        grouped_data[name] = grouped_data[name].astype('float')
        grouped_data = grouped_data.sort_values(by=name)
        grouped_data = grouped_data.tail(10)
        
        grouped_competitor = data_plot[data_plot['name'].isin(config.competitors[competitor])]
        grouped_competitor['name'] = competitor

        grouped_competitor = grouped_competitor[['name']+list(topics)].groupby('name').sum().reset_index()
        grouped_competitor = grouped_competitor.T
        grouped_competitor.columns = grouped_competitor.iloc[0]
        grouped_competitor = grouped_competitor.drop(grouped_competitor.index[0])
        grouped_competitor = grouped_competitor[grouped_competitor[competitor]!=0]
        grouped_competitor = grouped_competitor.reset_index()
        grouped_competitor[competitor] = grouped_competitor[competitor].astype('float')
        grouped_competitor = grouped_competitor[grouped_competitor['index'].isin(grouped_data['index'])]

        fig=go.Figure()
        fig.add_trace(
            go.Bar(
                y=grouped_data['index'], 
                x=grouped_data[name], 
                orientation='h', 
                text=round(grouped_data[name], 2), 
                marker = dict(color='#AAFA43'),
                name=name
                ))
        fig.add_trace(
            go.Bar(
                y=grouped_competitor['index'], 
                x=grouped_competitor[competitor], 
                orientation='h', 
                text=round(grouped_competitor[competitor], 2), 
                name=competitor,
                marker = dict(color='#022CA8')
                ))
        fig.update_layout(**layout_params).update_layout(
            title='Количество отзывов в каждом топике', 
            height=500, font_size=11,
            margin={'t':40, 'l':30, 'r': 0, 'b': 0},
            plot_bgcolor= '#ffffff',
            legend=dict(orientation="h")
            )

    return fig


def get_worst_indicators(name):

    data_week1 = pd.read_csv('data/data_week1.csv')
    data_week2 = pd.read_csv('data/data_week2.csv')

    topics = config.translation_dict.keys()

    grouped_data = data_week1[data_week1['name'].isin(config.shops[name])]
    grouped_data['name'] = name

    values = {}
    for col in topics:
        if len(grouped_data[col].dropna()):
            value = grouped_data[col].dropna().astype('int').mean()
            values[col] = value

    counts = {}
    for col in values.keys():
        if len(grouped_data[f'count_{col}'].dropna()):
            value = grouped_data[f'count_{col}'].dropna().astype('int').sum()
            counts[col] = value
            
    df_plot = pd.DataFrame(columns=['topic', 'value', 'count'])
    df_plot['topic'] = values.keys()
    df_plot['value'] = values.values()
    df_plot['count'] = counts.values()
    df_plot['topic'] = df_plot['topic'].map(config.translation_dict)

    df_plot = df_plot.sort_values('count', ascending=False).reset_index(drop=True)
    df_plot = df_plot.head(20)
    df_plot = df_plot.sort_values(by='value')
    df_plot1  = df_plot 

    grouped_data = data_week2[data_week2['name'].isin(config.shops[name])]
    grouped_data['name'] = name

    values = {}
    for col in topics:
        if len(grouped_data[col].dropna()):
            value = grouped_data[col].dropna().astype('int').mean()
            values[col] = value

    counts = {}
    for col in values.keys():
        if len(grouped_data[f'count_{col}'].dropna()):
            value = grouped_data[f'count_{col}'].dropna().astype('int').sum()
            counts[col] = value
            
    df_plot = pd.DataFrame(columns=['topic', 'value', 'count'])
    df_plot['topic'] = values.keys()
    df_plot['value'] = values.values()
    df_plot['count'] = counts.values()

    df_plot = df_plot.sort_values('count', ascending=False).reset_index(drop=True)
    df_plot = df_plot.head(20)
    df_plot = df_plot.sort_values(by='value')
    df_plot['topic'] = df_plot['topic'].map(config.translation_dict)

    df = df_plot.merge(df_plot1, on='topic', how='outer', suffixes=['1', '2'])
    df.dropna(inplace=True)
    df['change'] = df['value1'] - df['value2']
    df['change_count'] = df['count1'] - df['count2']

    worst = df.sort_values('change').head(4).reset_index(drop=True)
    worst['change'] = round(worst['change'], 2)

    fig = go.Figure()
    for i in range(len(worst)):
        topic = worst.loc[i, 'topic']
        change = worst.loc[i, 'change']
        count = abs(int(worst.loc[i, 'count2']))
        if count > 1000:
            count /= 10
            count = int(count)
        
        fig.add_trace(
            go.Indicator(
            mode = "number",
            number={'font_color':'#FF3705', 'font_size':50, 'suffix': "%"},
            value = change,
            title = {"text": f"<span style='font-size:1em;color:black'>{topic}</span><br><span style='font-size:0.8em;color:black'>{count} новых отзывов</span>"},
            domain = {'row': 0, 'column': i}
            ))

    fig.update_layout(
        # paper_bgcolor="#f0f0f0",
        grid = {'rows': 1, 'columns': 4, 'pattern': "independent"},
        height=220,
        font_family= 'Avenir Next', font_size=11, 
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        template = {'data' : {'indicator': [{
            'delta' : {'increasing': {'color': '#000000', 'symbol': ''}, 'decreasing': {'color': '#000000', 'symbol': ''}}}]}}
        )
    
    return fig


def get_best_indicators(name):

    data_week1 = pd.read_csv('data/data_week1.csv')
    data_week2 = pd.read_csv('data/data_week2.csv')

    topics = config.translation_dict.keys()

    grouped_data = data_week1[data_week1['name'].isin(config.shops[name])]
    grouped_data['name'] = name

    values = {}
    for col in topics:
        if len(grouped_data[col].dropna()):
            value = grouped_data[col].dropna().astype('int').mean()
            values[col] = value

    counts = {}
    for col in values.keys():
        if len(grouped_data[f'count_{col}'].dropna()):
            value = grouped_data[f'count_{col}'].dropna().astype('int').sum()
            counts[col] = value
            
    df_plot = pd.DataFrame(columns=['topic', 'value', 'count'])
    df_plot['topic'] = values.keys()
    df_plot['value'] = values.values()
    df_plot['count'] = counts.values()
    df_plot['topic'] = df_plot['topic'].map(config.translation_dict)

    df_plot = df_plot.sort_values('count', ascending=False).reset_index(drop=True)
    df_plot = df_plot.head(20)
    df_plot = df_plot.sort_values(by='value')
    df_plot1  = df_plot 

    grouped_data = data_week2[data_week2['name'].isin(config.shops[name])]
    grouped_data['name'] = name

    values = {}
    for col in topics:
        if len(grouped_data[col].dropna()):
            value = grouped_data[col].dropna().astype('int').mean()
            values[col] = value

    counts = {}
    for col in values.keys():
        if len(grouped_data[f'count_{col}'].dropna()):
            value = grouped_data[f'count_{col}'].dropna().astype('int').sum()
            counts[col] = value
            
    df_plot = pd.DataFrame(columns=['topic', 'value', 'count'])
    df_plot['topic'] = values.keys()
    df_plot['value'] = values.values()
    df_plot['count'] = counts.values()

    df_plot = df_plot.sort_values('count', ascending=False).reset_index(drop=True)
    df_plot = df_plot.head(20)
    df_plot = df_plot.sort_values(by='value')
    df_plot['topic'] = df_plot['topic'].map(config.translation_dict)

    df = df_plot.merge(df_plot1, on='topic', how='outer', suffixes=['1', '2'])
    df.dropna(inplace=True)
    df['change'] = df['value1'] - df['value2']
    df['change_count'] = df['count1'] - df['count2']

    best = df.sort_values('change', ascending=False).head(4).reset_index(drop=True)
    best['change'] = round(best['change'], 2)
    fig = go.Figure()
    for i in range(len(best)):
        topic = best.loc[i, 'topic']
        change = best.loc[i, 'change']
        count = abs(int(best.loc[i, 'count2']))
        if count > 1000:
            count /= 10
            count = int(count)
        fig.add_trace(
            go.Indicator(
            mode = "number",
            number={'font_color':'#60A802', 'font_size':50, 'suffix': "%", 'prefix': "+"},
            value = change,
            title = {"text": f"<span style='font-size:1em;color:black'>{topic}</span><br><span style='font-size:0.8em;color:black'>{count} новых отзывов</span>"},
            domain = {'row': 0, 'column': i}
            ))

    fig.update_layout(
        # paper_bgcolor="#f0f0f0",
        grid = {'rows': 1, 'columns': 4, 'pattern': "independent"},
        height=220,
        font_family= 'Avenir Next', font_size=12, 
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        template = {'data' : {'indicator': [{
            'delta' : {'increasing': {'color': '#000000', 'symbol': ''}, 'decreasing': {'color': '#000000', 'symbol': ''}}}]}}
        )
    
    return fig