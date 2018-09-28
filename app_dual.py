# -*- coding: utf-8 -*-
import dash
import base64
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

# Load background image
bg_image = base64.b64encode(open('mtb_background.jpg', 'rb').read())

def shrink_table(reclist,trail_data):
    df_small = trail_data.loc[reclist['index'],['trail_id','description','trail_num']]
    df_small.columns = ['Trail ID', 'Description','trail_num']
    return df_small

def generate_tables(reclist,input_row):
    table = []
    
    table.append(html.Tr(html.Td(html.H3('Your Entry'),colSpan='7')))
    
    input_graphics = html.Tr([
        html.Td(html.Iframe(src='https://www.trailforks.com/widgets/trail/?trailid='+input_row['trail_num']+'&elevation=1&map=0&noheader=0',width='500', height='350',
                            style={'float': 'inherit', 'border': 'none'})),
        html.Td(html.Iframe(src='https://www.trailforks.com/widgets/trail/?trailid='+input_row['trail_num']+'&elevation=0&map=1&noheader=1&info=0',width='500', height='350',
                            style={'float': 'inherit', 'border': 'none'}))
        ])
    input_description = html.Tr(html.Td(input_row['Description'],colSpan='2'))
    table.append(html.Tr(html.Td(html.Table([input_graphics,input_description]))))
    
    table.append(html.Tr(html.Td(html.H3('Personalized Recommendations'),colSpan='7')))
    
    for num,desc in zip(reclist['trail_num'],reclist['Description']):
        rec_graphics = html.Tr([
            html.Td(html.Iframe(src='https://www.trailforks.com/widgets/trail/?trailid='+num+'&elevation=1&map=0&noheader=0',width='500', height='350',
                                style={'float': 'inherit', 'border': 'none'})),
            html.Td(html.Iframe(src='https://www.trailforks.com/widgets/trail/?trailid='+num+'&elevation=0&map=1&noheader=1&info=0',width='500', height='350',
                                style={'float': 'inherit', 'border': 'none'}))
            ])
        rec_description = html.Tr(html.Td(desc,colSpan='2'))
        table.append(html.Tr(html.Td(html.Table([rec_graphics,rec_description]))))

    output = html.Div(html.Table(table))
                
                        # Body
                        #[html.Tr([
                        #    html.Td(html.A(input_row.iloc[i][col],href = 'https://www.trailforks.com/trails/'+input_row.iloc[i][col]+'/')) if col == 'Trail ID' else html.Td(input_row.iloc[i][col]) for col in input_row.columns
                        #    ]) for i in range(len(input_row))] +
                        
                        #[html.Tr([html.Th(col) for col in reclist.columns])] +
                
                        # Body
                        #[html.Tr([
                        #    html.Td(html.A(reclist.iloc[i][col],href = 'https://www.trailforks.com/trails/'+reclist.iloc[i][col]+'/')) if col == 'Trail ID' else html.Td(reclist.iloc[i][col]) for col in reclist.columns
                        #    ]) for i in range(len(reclist))]
            
    return output


app = dash.Dash(__name__)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.title = 'Rec&Ride'

app.layout = html.Div([
    html.Div([html.H1('Rec & Ride',style = {'textAlign': 'center'}),
              html.H2('MTB Trail Recommender',style = {'textAlign': 'center'})]),
    
    html.Div(html.Img(src='data:image/jpeg;base64,{}'.format(bg_image.decode('ascii')),
                      style = {'width':'100%', 'padding':'0','margin':'0','box-sizing':'border-box'})),
                      
    html.H3('Enter your favorite trail or your username:', style = {'margin':'auto', 'display':'block', 'margin-top':'50px', 
                                               'margin-bottom':'10px','text-align':'center'},
           id='prompt-text'),
    html.Div([
        dcc.Input(
            id='favorite-trail',
            type='text',
            placeholder='trail name or username',
            style = {'margin':'auto','display':'block'}),
        html.Button('Submit', id='button-primary',
                    style = {'margin':'auto', 'margin-top':'10px','display':'block', 'margin-bottom':'50px'}),
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
    reclist,input_row = get_recommendations(trail_data_clean,value,indices,cosine_sim)
    reclist = shrink_table(reclist,trail_data)
    input_row = shrink_table(input_row,trail_data)
    return generate_tables(reclist,input_row)


if __name__ == '__main__':
    app.run_server()
