# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from model import model_tfidf,get_recommendations,model_tfidf_num_cat,model_tfidf_num,model_tfidf_cat
from etl import get_trail_data,clean_ft,clean_grades,convert_ft_mi,get_clean_data
# Query SQL
trail_data,indices = get_trail_data()
trail_data_clean = get_clean_data(trail_data)
#cosine_sim = model_tfidf(trail_data)
cosine_sim = model_tfidf_num_cat(trail_data_clean)
#cosine_sim = model_tfidf_num(trail_data)
#cosine_sim = model_tfidf_cat(trail_data)


def shrink_table(reclist,trail_data):
    df_small = trail_data.loc[reclist['index'],['trail_id','rating', 'distance','climb','descent','description','trail_num']]
    
    df_small['Difficulty rating'] = reclist['Difficulty rating']
    df_small = df_small[['trail_id','Difficulty rating','rating', 'distance','climb','descent','description']]
    df_small.columns = ['Trail ID', 'Difficulty', 'Rating', 'Distance',
       'Climb','Descent','Description']
    return df_small

def generate_tables(reclist,input_row):
    output = html.Div([
            html.Div([
                    
                    html.Table(
                        [html.Tr(html.Td(html.H3('Your Entry'),colSpan='7'))] +
                        # Header
                        [html.Tr([html.Th(col) for col in input_row.columns])] +
                
                        # Body
                        [html.Tr([
                            html.Td(html.A(input_row.iloc[i][col],href = 'https://www.trailforks.com/trails/'+input_row.iloc[i][col]+'/')) if col == 'Trail ID' else html.Td(input_row.iloc[i][col]) for col in input_row.columns
                            ]) for i in range(len(input_row))] +
                        [html.Tr(html.Td(html.H3('Personalized Recommendations'),colSpan='7'))]+
                        [html.Tr([html.Th(col) for col in reclist.columns])] +
                
                        # Body
                        [html.Tr([
                            html.Td(html.A(reclist.iloc[i][col],href = 'https://www.trailforks.com/trails/'+reclist.iloc[i][col]+'/')) if col == 'Trail ID' else html.Td(reclist.iloc[i][col]) for col in reclist.columns
                            ]) for i in range(len(reclist))]
                        )
                   ]),
                ])
            
    return output



app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    
    html.H1('Rec & Ride'),
    dcc.Input(
        id='favorite-trail',
        type='text',
        placeholder='trail name',
        ),
    html.Button('Submit', id='button-primary'),
    html.Div(id='output-recommendation')
])


@app.callback(
    dash.dependencies.Output('output-recommendation', 'children'),
    [dash.dependencies.Input('button-primary', 'n_clicks')],
    [dash.dependencies.State('favorite-trail', 'value')])
def update_output_rec(n_clicks,value):
    value = value.replace('https://www.trailforks.com/trails/','')
    value = value.replace('/','')
    reclist,input_row = get_recommendations(trail_data_clean,value,indices,cosine_sim)
    reclist = shrink_table(reclist,trail_data)
    input_row = shrink_table(input_row,trail_data)
    return generate_tables(reclist,input_row)


if __name__ == '__main__':
    app.run_server()
