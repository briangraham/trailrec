import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler,OneHotEncoder,LabelBinarizer


def get_data_from_file():
    trail_data = pd.read_pickle('trail_data.pickle')
    trail_data_clean = pd.read_pickle('trail_data_clean.pickle')
    indices = pd.read_pickle('indices.pickle')
    cosine_sim = pd.read_pickle('cosine_sim.pickle')
    df_top_ten = pd.read_pickle('top_10_rider_recs.pickle')
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

def get_recs_collab(df_top_ten,user_entry):
    df_user = df_collab[df_collab['uid'] == user_entry]
    df_user = df_user.sort_values('rank')
    user_recs = df_user['iid']
    return user_recs

def model_tfidf(trail_data):
    #vectorize
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(trail_data['description'])
    
    # dot product to get cosine sim
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def model_count_vect(trail_data):
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(trail_data['description'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    return cosine_sim

def model_tfidf_cat(trail_data):
    # vectorize and scale difficulty (categorical)
    trail_data_cat = trail_data[['Difficulty rating']]
    trail_data_cat = trail_data_cat.apply(lambda x: x.str.replace(' ','')).astype('category')    
    enc = LabelBinarizer().fit(trail_data_cat)
    df_cat = enc.transform(trail_data_cat)
    scaler_cat = StandardScaler().fit(df_cat)
    df_cat_scaled = scaler_cat.transform(df_cat)
    
    # vectorize text data
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(trail_data['description']).toarray()
    
    # concatenate and get similarity
    all_features = np.concatenate([tfidf_matrix,df_cat_scaled],axis=1)
    cosine_sim = cosine_similarity(all_features, all_features)
    return cosine_sim
def model_tfidf_num(trail_data):
    # scale numerical data (continuous)
    trail_data_numerical = trail_data[['Altitude end','Altitude start',
                                       'Grade max','climb', 'descent',
                                       'distance','rating']]
    scaler_num = StandardScaler().fit(trail_data_numerical)
    df_num_scaled = scaler_num.transform(trail_data_numerical)
    
    # vectorize text data
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(trail_data['description']).toarray()
    
    # concatenate and get similarity
    all_features = np.concatenate([tfidf_matrix,df_num_scaled],axis=1)
    cosine_sim = cosine_similarity(all_features, all_features)
    return cosine_sim
def model_tfidf_num_cat(trail_data):
    # vectorize and scale difficulty (categorical)
    trail_data_cat = trail_data[['Difficulty rating']]
    trail_data_cat = trail_data_cat.apply(lambda x: x.str.replace(' ','')).astype('category')    
    enc = LabelBinarizer().fit(trail_data_cat)
    df_cat = enc.transform(trail_data_cat)
    scaler_cat = StandardScaler().fit(df_cat)
    df_cat_scaled = scaler_cat.transform(df_cat)
    
    # scale numerical data (continuous)
    trail_data_numerical = trail_data[['Altitude end','Altitude start',
                                       'Grade max','climb', 'descent',
                                       'distance','rating']]
    scaler_num = StandardScaler().fit(trail_data_numerical)
    df_num_scaled = scaler_num.transform(trail_data_numerical)
    
    # vectorize text data
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(trail_data['description']).toarray()
    
    # concatenate and get similarity
    all_features = np.concatenate([tfidf_matrix,df_cat_scaled,df_num_scaled],axis=1)
    cosine_sim = cosine_similarity(all_features, all_features)
    return cosine_sim