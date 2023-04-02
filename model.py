import pandas as pd
import numpy as np
import pickle
series_data = pd.read_csv(r"C:\Users\ramya\downloads\TV Series.csv")
series = pd.read_csv(r"C:\Users\ramya\downloads\TV Series.csv")
series_data=series_data.iloc[:500]
series_data = series_data.fillna('')
series_data.drop('Runtime',axis=1,inplace=True)
def clean_data(x):
    return str.lower(x.replace(" ", ""))
for i in series_data.columns:
    series_data[i] = series_data[i].apply(clean_data)
def create_soup(x):
    return x['Series Title']+ ' ' + x['Release Year'] + ' ' + x['Genre'] + ' ' +x['Rating']+' '+ x['Cast']+' '+ x['Synopsis']
series_data['soup'] = series_data.apply(create_soup, axis=1)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(series_data['soup'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

series_data=series_data.reset_index()
indices = pd.Series(series_data.index, index=series_data['Series Title'])

def reccs(title):
    global cosine_sim
    title=title.replace(' ','').lower()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    result =  series['Series Title'].iloc[movie_indices]
    result = result.to_frame()
    result = result.set_index(np.arange(1,len(result)+1))
    return result
pickle.dump(reccs,open('rsmodel.pkl','wb'))