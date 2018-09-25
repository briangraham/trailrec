import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2 
import io

def get_trail_data():
    # Query SQL trail table
    conn = psycopg2.connect("host=localhost dbname=trailrec user=briangraham")
    cur = conn.cursor()
    sql_query = """
    SELECT * FROM trails;
    """
    trail_data = pd.read_sql_query(sql_query,conn)
    
    #reset indices
    trail_data = trail_data.reset_index()
    # reverse map trail names to indices
    indices = pd.Series(trail_data.index, index=trail_data['trail_id'])
    
    return trail_data,indices

def clean_ft(col):
    col = col.str.replace(' ft','').str.replace(',','')
    col = pd.to_numeric(col)
    return col

def clean_grades(col):
    col = col.str.replace('%','')
    col = pd.to_numeric(col)
    return col

def convert_ft_mi(series):
    split_str = series.str.replace(',','').str.split()
    newcol = []
    for row in split_str:
        if row:
            if row[1] == 'ft':
                newcol.append(pd.to_numeric(row[0])/5280)
            else:
                newcol.append(pd.to_numeric(row[0]))
        else:
            newcol.append(pd.to_numeric(''))
    return newcol

def get_clean_data(trail_data):
    trail_data['Difficulty rating'] = trail_data['Difficulty rating'].str.replace('rate','')
    trail_data['Global Ranking'] = trail_data['Global Ranking'].str.replace('#','')
    trail_data['Riding area'] = trail_data['Riding area'].str.replace(', British Columbia','')
    trail_data['Riding area'] = trail_data.apply(lambda x: x['Riding area'].replace(x['city'],'',1),axis=1)
    
    ft_clean = ['Altitude change','Altitude end','Altitude max','Altitude min','Altitude start','climb','descent']
    for col in ft_clean:
        trail_data[col] = clean_ft(trail_data[col])
        
    per = ['Grade','Grade max','Grade min']
    for col in per:
        trail_data[col] = clean_grades(trail_data[col])
        
    ft_or_mi = ['distance','Distance climb','Distance down','Distance flat']
    for measure in ft_or_mi:
        trail_data[measure] = convert_ft_mi(trail_data[measure])
    
    return trail_data

def model_tfidf(trail_data):
    #vectorize
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(trail_data['description'])
    
    # dot product to get cosine sim
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def model_count_vect(trail_data):
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(trail_data['description'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    return cosine_sim
    
def get_recommendations(trail_data, trail_id,indices,cosine_sim):
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