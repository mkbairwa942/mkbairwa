import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback, DiskcacheManager
from support_dash_tutorial import *
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd


data_eq2 = data_eq


app = dash.Dash(__name__, )
app.layout = html.Div((

    html.Div([
        html.Div([
            html.Div([
                html.H3('Global Data', style={"margin-bottom": "8px", 'color': 'red'}),                        
                html.H5("1978-2017", style={"margin-top": "8px", 'color': 'green'}),                       

            ]),
        ], className="six column", id="tittle")

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.P('Select Year:',className='fix-label', style={'color': 'white', 'margin-bottom': "1%"}),
            dcc.RangeSlider(id='select_years',            
             min=1978,
             max=2017,
             dots=True,
             value=[2010, 2017],
             marks={str(yr): str(yr) for yr in range(1970, 2017, 4)}),

        ], className="create_container twelve columns", style={'width': '98%', 'margin-left': '1%'}),

    ], className='row flex-display'),
    
    html.Div([
        html.Div([
            html.P('Select Region:', className='fix_label',style={'color': 'white'}),                   
            dcc.Dropdown(id='datee',
                        multi=False,
                        clearable=True,
                        disabled=False,
                        style={'display': True},
                        value=day,
                        placeholder='Select Date',
                        options=[{'label': c, 'value': c}
                                for c in datess], className='dcc_compon'),

            html.P('Select Country:', className='fix_label',style={'color': 'white'}),                   
            dcc.Dropdown(id='timee',
                        multi=False,
                        clearable=True,
                        disabled=False,
                        style={'display': True},
                        placeholder='Select Countries',
                        options=[], className='dcc_compon')

        ], className="create_container three columns"),

        html.Div([
            dcc.Graph(id='bar-line1',
                        config={'displayModeBar': 'hover'}),

        ], className="create_container six columns"),

        html.Div([
            dcc.Graph(id='pie',
                        config={'displayModeBar': 'hover'}),

        ], className="create_container three columns"),
    
    ], className="row flex-display"),


    html.Div([
        html.Div([
            dcc.Graph(id='map-1',
                    config={'displayModeBar': 'hover'}),

        ], className="create_container 12 columns"),

    ], className="row flex-display"),

),id='mainContainer',style={'dispaly':'flex',"flex-direction":'column'})


@app.callback(
    Output('timee','options'),
    Input('datee','value'))
def get_counrty_options(datee):
    datee = pd.Timestamp(datee)
    print(datee)
    print(type(datee))
    data_eq3 = data_eq[data_eq['DATE'] == datee]
    print(data_eq3.head(3))
    return [{'label':i,'value':i}for i in data_eq3['Time'].unique()]


@app.callback(
    Output('timee','value'),
    Input('timee','options'))
def get_counrty_value(timee):
    return [k['value']for k in timee][1]



@app.callback(Output('bar_line_1','figure'),
                [Input('datee','value')],
                [Input('timee','value')],
                [Input('select_years','value')])
def update_graph(datee,timee,select_years):

    data_eq5 = data_eq2.groupby(['DATE','Time'])[['CE_OI','PE_OI']].sum()
    data_eq6 = data_eq5[(data_eq5['DATE'] == datee) &  (data_eq5['Time'] == timee) & (data_eq5['Time'] >= select_years[0]) & (data_eq5['Time'] <= select_years[1])]
    data_eq7 = data_eq2.groupby(['DATE','Time'])[['CE_Volume','PE_Volume']].sum()
    data_eq8 = data_eq7[(data_eq7['DATE'] == datee) &  (data_eq7['Time'] == timee) & (data_eq7['Time'] >= select_years[0]) & (data_eq7['Time'] <= select_years[1])]

    return {
        'data':[go.Scatter(x= data_eq6['Time'],
                            y= data_eq6['CE_OI'],
                            mode='lines+markers',
                            name='Death',
                            line=dict(shape = 'spline',smoothing =1.3,width=3,color='#FF00FF'),
                            marker=dict(size=10,symbol='circle',color="white",
                                        line=dict(color='#FF00FF',width=2)
                                        ),
                                        hoverinfo='text',
                                        hovertext=
                                        '<b>DATE</b>: '+data_eq6['DATE'].astype(str)+'<br>'+
                                        '<b>Time</b>: '+data_eq6['Time'].astype(str)+'<br>'+
                                        '<b>Region</b>: '+data_eq6['DATE'].astype(str)+'<br>'+
                                        '<b>Death</b>: '+[f'{x:,.0f}' for x in data_eq6['CE_OI']]+'<br>'
                                        
                                        ),
                                        go.Bar(
                                            x=data_eq8['Time'],
                                            y=data_eq8['CE_Volume'],
                                            text=data_eq8['CE_Volume'],
                                            texttemplate='%{text:.2s}',
                                            textposition='auto',
                                            name='CE Volume',

                                            marker=dict(color='orange'),

                                            hoverinfo='text',
                                            hovertext=
                                            '<b>DATE</b>: '+data_eq8['DATE'].astype(str)+'<br>'+
                                            '<b>Time</b>: '+data_eq8['Time'].astype(str)+'<br>'+
                                            '<b>Region</b>: '+data_eq8['DATE'].astype(str)+'<br>'+
                                            '<b>Death</b>: '+[f'{x:,.0f}' for x in data_eq8['CE_Volume']]+'<br>'
                                        ),
                                                                                
                                        go.Bar(x=data_eq8['Time'],
                                            y=data_eq8['CE_OI'],
                                            text=data_eq8['CE_OI'],
                                            texttemplate='%{text:.2s}',
                                            textposition='auto',
                                            textfont=dict(
                                                color='white'
                                            ),
                                            name='CE OI',

                                            marker=dict(color='#9C0C38'),

                                            hoverinfo='text',
                                            hovertext=
                                            '<b>DATE</b>: '+data_eq8['DATE'].astype(str)+'<br>'+
                                            '<b>Time</b>: '+data_eq8['Time'].astype(str)+'<br>'+
                                            '<b>Region</b>: '+data_eq8['DATE'].astype(str)+'<br>'+
                                            '<b>Death</b>: '+[f'{x:,.0f}' for x in data_eq8['CE_OI']]+'<br>'
                                            )],

        'layout':go.Layout(
            barmode='stack',
            plot_bgcolor='#010915',
            paper_bgcolor='#010915',
            title={
                'text':'Attack and Death : '+(timee)+' '+'<br>'+'-'.join(
                    [str(y) for y in select_years])+'</br>',

                'y':0.93,
                'x':0.5,
                'xanchor':'center',
                'yanchor':'top'},
            titlefont={
                'color':'white',
                'size':20},
            
            hovermode='x',

            xaxis=dict(tittle='<b>Year</b>',
                       tick0=0,
                       dtick=1,
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                       )

                       ),

            yaxis=dict(tittle='<b>Attack and Death</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                       )

                       ),

            legend={
                'orientation':'h',
                'bgcolor':'#010915',
                'xanchor':'center','x':0.5,'y':-0.3},
            font=dict(
                family='sans-serif',
                size=12,
                color='white'),
            
        )

    }



@app.callback(Output('pie','figure'),
                [Input('datee','value')],
                [Input('timee','value')],
                [Input('select_years','value')])
def display_content(datee,timee,select_years):    
    data_eq9 = data_eq2.groupby(['DATE','Time'])[
        ['CE_OI','PE_OI']].sum()
    CE_Volume = data_eq9[(data_eq9['DATE'] == datee) &  (data_eq9['Time'] == timee) & (data_eq9['Time'] >= select_years[0]) & (data_eq9['Time'] <= select_years[1])]['CE_Volume'].sum()
    CE_Chg_OI = data_eq9[(data_eq9['DATE'] == datee) &  (data_eq9['Time'] == timee) & (data_eq9['Time'] >= select_years[0]) & (data_eq9['Time'] <= select_years[1])]['CE_Chg_OI'].sum()
    CE_OI = data_eq9[(data_eq9['DATE'] == datee) &  (data_eq9['Time'] == timee) & (data_eq9['Time'] >= select_years[0]) & (data_eq9['Time'] <= select_years[1])]['CE_OI'].sum()
    colors=['#FF00FF','#09C0C38','orange']

    return {
        'data':[go.Pie(labels=['Total CE_Volume','Total CE_Chg_OI','Total CE_OI'],
                       values=[CE_Volume,CE_Chg_OI,CE_OI],
                       marker=dict(colors=colors),
                       hoverinfo='label+value+percent',
                       textinfo='label+value',
                       textfont=dict(size=13)
                       # hole=0.7,
                       # rotation=45,
                       # insidetextorientation='radial',

                       )],
            
        'layout':go.Layout(
            plot_bgcolor='#010915',
            paper_bgcolor='#010915',
            hovermode='closest',
            title={
                'text':'Total Casualties :'+(timee)+' '+'<br>'+'-'.join(
                    [str(y) for y in select_years])+'</br>',

                'y':0.93,
                'x':0.5,
                'xanchor':'center',
                'yanchor':'top'},
            titlefont={
                'color':'white',
                'size':20},
            legend={
                'orientation':'h',
                'bgcolor':'#010915',
                'xanchor':'center', 'x':0.5,'y':-0.07},
            font=dict(
                family='sans-serif',
                size=12,
                color='white')
        ),            
                
    }
             
            
        

 


if __name__ == '__main__':
    app.run_server(debug=True)



