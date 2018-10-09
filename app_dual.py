# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import base64

def get_data_from_file():
    trail_data = pd.read_pickle('trail_data.pickle')
    trail_data_clean = pd.read_pickle('trail_data_clean.pickle')
    indices = pd.read_pickle('indices.pickle')
    cosine_sim = pd.read_pickle('cosine_sim.pickle')
    df_top_ten = pd.read_pickle('top_10_rider_recs.pickle')
    return trail_data,indices,trail_data_clean,cosine_sim


def get_recs_cosine(trail_data,trail_id,indices,cosine_sim):
    idx = indices[trail_id]
    # Get the pairwsie similarity scores of all trails with that trail
    sim_scores = list(enumerate(cosine_sim[idx]))    
    # Sort trails using similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)    
    # 10 most similar trails
    sim_scores = sim_scores[1:11]    
    # Get trails
    trail_indices = [i[0] for i in sim_scores]    
    input_data = trail_data.iloc[[indices[trail_id]]]
    return trail_data.iloc[trail_indices],input_data




def shrink_table(reclist,trail_data):
     df_small = trail_data.loc[reclist['index'],['trail_id','rating', 'distance','climb','descent','description','trail_num']]     
     df_small['Difficulty rating'] = reclist['Difficulty rating']
     df_small = df_small[['trail_id','Difficulty rating','rating', 'distance','climb','descent','description','trail_num']]
     df_small.columns = ['Trail ID', 'Difficulty', 'Rating', 'Distance',
        'Climb','Descent','Description','trail_num']
     return df_small

def parse_input(user_input):
    clean_input = user_input.replace('https://www.trailforks.com/trails/','')
    clean_input = clean_input.replace('/','')
    clean_input = clean_input.replace(' ','-')
    clean_input = clean_input.lower()
    return clean_input

def generate_tables_cosine_rec(reclist,input_row):
    page = []
    
    # widget specs
    wig_width = '600'
    wig_height = '325'
    map_height = '325'
    
    
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
    return page

def generate_error_message():
    html_ouput = html.Div([
            html.H4('Hmmm...we cannot find that trail or user.'),
                     ('Try copying and entering the url of the trail page from Trailforks.com or check the spelling of your username.  '),
                     ('Also, this proof of concept trail recommender is currently to a subset of trails from British Columbia, Canada which have descriptions.  It is also limited to users who have ridden these trails')],style = {'text-align': 'center'})
    
    return html_ouput


#Load data as soon as the app starts up
trail_data,indices,trail_data_clean,cosine_sim = get_data_from_file()
bg_image = base64.b64encode(open('mtb_background.jpg', 'rb').read())

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
    clean_input = parse_input(value)
    if trail_data_clean['trail_id'].str.contains(clean_input).any():
        reclist,input_row = get_recs_cosine(trail_data_clean,clean_input,indices,cosine_sim)
        reclist = shrink_table(reclist,trail_data)
        input_row = shrink_table(input_row,trail_data)
        return generate_tables_cosine_rec(reclist,input_row)
    else:
        return generate_error_message()
    
if __name__ == '__main__':
    app.run_server(host="0.0.0.0")
