# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import base64
from model import get_recs_cosine,model_tfidf_num_cat, get_data_from_file

#Load data as soon as the app starts up
trail_data,indices,trail_data_clean,cosine_sim = get_data_from_file()
bg_image = base64.b64encode(open('mtb_background.jpg', 'rb').read())

def shrink_table(reclist,trail_data):
     df_small = trail_data.loc[reclist['index'],['trail_id','rating', 'distance','climb','descent','description','trail_num']]     
     df_small['Difficulty rating'] = reclist['Difficulty rating']
     df_small = df_small[['trail_id','Difficulty rating','rating', 'distance','climb','descent','description','trail_num']]
     df_small.columns = ['Trail ID', 'Difficulty', 'Rating', 'Distance',
        'Climb','Descent','Description','trail_num']
     return df_small

def generate_tables(reclist,input_row):
    page = []
    
    # widget specs
    wig_width = '600'
    wig_height = '325'
    map_height = '325'
    
    # Table
#    input_row_table = input_row.drop(['trail_num'], axis=1)
#    reclist_table = reclist.drop(['trail_num'], axis=1)
#    tabular_results = html.Div([ 
#            html.Table(
#                [html.Tr(html.Td(html.H6('Your Entry'),colSpan='7'))] +
#                # Header
#                [html.Tr([html.Th(col) for col in input_row_table.columns])] +
#        
#                # Body
#                [html.Tr([
#                    html.Td(html.A(input_row_table.iloc[i][col],href = 'https://www.trailforks.com/trails/'+input_row_table.iloc[i][col]+'/')) if col == 'Trail ID' else html.Td(input_row_table.iloc[i][col]) for col in input_row_table.columns
#                    ]) for i in range(len(input_row_table))] +
#                [html.Tr(html.Td(html.H6('Personalized Recommendations'),colSpan='8'))]+
#                [html.Tr([html.Th(col) for col in reclist_table.columns])] +
#        
#                # Body
#                [html.Tr([
#                    html.Td(html.A(reclist_table.iloc[i][col],href = 'https://www.trailforks.com/trails/'+reclist_table.iloc[i][col]+'/')) if col == 'Trail ID' else html.Td(reclist_table.iloc[i][col]) for col in reclist_table.columns
#                    ]) for i in range(len(reclist_table))]
#                )
#        ])
#         
#    page.append(tabular_results)
    #page.append(html.H3(' '))
    #page.append(html.H3('More Details'))
    
    graphical_results = []
    graphical_results.append(html.Tr(html.Td(html.H5('Your Entry'),colSpan='2')))
    
    
    graphical_results.append(html.Tr([
        html.Td(html.Iframe(src='https://www.trailforks.com/widgets/trail/?trailid='+input_row['trail_num']+'&elevation=1&map=0&noheader=0',width=wig_width, height=wig_height,
                            style={'float': 'left', 'border': 'none'}), style={'border-bottom-style':'none'}),
        html.Td(html.Iframe(src='https://www.trailforks.com/widgets/trail/?trailid='+input_row['trail_num']+'&elevation=0&map=1&noheader=1&info=0&photos=1'+'&h='+map_height,width=wig_width, height=wig_height,
                            style={'float': 'left', 'border': 'none'}), style={'border-bottom-style':'none'})
        ]))
    graphical_results.append(html.Tr(html.Td(input_row['Description'],colSpan='2')))
    graphical_results.append(html.Tr(html.Td(html.H5('Personalized Recommendations'))))
    
    for num,desc in zip(reclist['trail_num'],reclist['Description']):
        graphical_results.append(html.Tr([
            html.Td(html.Iframe(src='https://www.trailforks.com/widgets/trail/?trailid='+num+'&elevation=1&map=0&noheader=0',width=wig_width, height=wig_height,
                                style={'float': 'left', 'border': 'none'}), style={'border-bottom-style':'none'}),
            html.Td(html.Iframe(src='https://www.trailforks.com/widgets/trail/?trailid='+num+'&elevation=0&map=1&noheader=1&info=0&photos=1',width=wig_width, height=wig_height,
                                style={'float': 'left', 'border': 'none'}), style={'border-bottom-style':'none'})
            ]))
        graphical_results.append(html.Tr(html.Td(desc,colSpan='2')))
        
    page.append(html.Div(html.Table(graphical_results)))
    output = page
    return output


app = dash.Dash(__name__)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.title = 'Rec&Ride'

app.layout = html.Div([
        
    html.Div([html.H1('Rec & Ride',style = {'textAlign': 'center'}),
              html.H2('MTB Trail Recommender',style = {'textAlign': 'center'})]),
    
    html.Div(html.Img(src='data:image/jpeg;base64,{}'.format(bg_image.decode('ascii')),
                      style = {'width':'100%', 'padding':'0','margin':'0','box-sizing':'border-box'})),
                      
    html.H3('Enter your favorite trail or your username:', style = {'margin':'auto', 'display':'block', 'margin-top':'10px', 
                                               'margin-bottom':'10px','text-align':'center'},
           id='prompt-text'),
    html.Div([
        dcc.Input(
            id='favorite-trail',
            type='text',
            placeholder='trail name or username',
            style = {'margin':'auto','display':'block'}),
        html.Button('Submit', id='button-primary',
                    style = {'margin':'auto', 'margin-top':'10px','display':'block', 'margin-bottom':'10px'}),
        html.Div(id='output-recommendation',
                    style = {'margin':'auto', 'display':'block'})
    ],
    style = {'width':'100%','margin':'auto', 'display':'block'})
])


@app.callback(
    dash.dependencies.Output('output-recommendation', 'children'),
    [dash.dependencies.Input('button-primary', 'n_clicks')],
    [dash.dependencies.State('favorite-trail', 'value')])
def update_output_rec(n_clicks,value):
    value = value.replace('https://www.trailforks.com/trails/','')
    value = value.replace('/','')
    value = value.replace(' ','-')
    value = value.lower()
    reclist,input_row = get_recs_cosine(trail_data_clean,value,indices,cosine_sim)
    reclist = shrink_table(reclist,trail_data)
    input_row = shrink_table(input_row,trail_data)
    return generate_tables(reclist,input_row)


if __name__ == '__main__':
    app.run_server(host="0.0.0.0")
