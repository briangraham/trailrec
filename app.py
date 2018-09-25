# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from model import get_trail_data,model_tfidf,get_recommendations

# Query SQL
trail_data,indices = get_trail_data()
cosine_sim = model_tfidf(trail_data)


def shrink_table(df_trail):
    df_small = df_trail[['trail_id', 'Difficulty rating', 'rating', 'distance',
       'climb','descent','description']]
    return df_small

def generate_tables(reclist,input_row):
    reclist = shrink_table(reclist)
    input_row = shrink_table(input_row)
    output = html.Div([
            html.Div([
                    html.H2('Your Entry'),
                    html.Table(
                        # Header
                        [html.Tr([html.Th(col) for col in input_row.columns])] +
                
                        # Body
                        [html.Tr([
                            html.Td(input_row.iloc[i][col]) for col in input_row.columns
                            ]) for i in range(len(input_row))]
                        )
                    ]),
            html.Div([
                    html.H2('Personalized Recommendations'),
                    html.Table(
                        # Header
                        [html.Tr([html.Th(col) for col in reclist.columns])] +
                
                        # Body
                        [html.Tr([
                            html.Td(reclist.iloc[i][col]) for col in reclist.columns
                            ]) for i in range(len(reclist))]
                        )
                    ])
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
    reclist,input_row = get_recommendations(trail_data,value,indices,cosine_sim)
    return generate_tables(reclist,input_row)


if __name__ == '__main__':
    app.run_server()
