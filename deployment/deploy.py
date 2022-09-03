
import pandas as pd
import numpy as np
import pickle
from flask import Flask, request, jsonify

import warnings 
warnings.filterwarnings('ignore')

movies = pd.read_csv('artifacts//movies.csv')
ratings = pd.read_csv('artifacts//ratings.csv')

def find_similar_movies(movie_id):
    #get similar users that rated the movie above 4
    similar_users = ratings[
        (ratings['movieId'] == movie_id) & (ratings['rating']>4)
    ]["userId"].unique()
    
    #find other movies they similars users rated above 4
    similar_users_recs = ratings[
        (ratings["userId"].isin(similar_users)) & (ratings['rating']>4)
    ]['movieId']
    
    #find the percentage of similar_users who liked the  movies particular to that niche i.e movies that a greater than 10% of the users similar to us liked
    similar_users_recs = similar_users_recs.value_counts()/len(similar_users)
    similar_users_recs = similar_users_recs[similar_users_recs > .1]
    
    #find how much all_users liked these movies in the niche >10% i.e (including users outside that niche)
    all_users = ratings[
        (ratings['movieId'].isin(similar_users_recs.index)) & (ratings['rating']>4)
    ]
    
    #find the percentage of all users who liked each movie recommendend
    all_users_recs = all_users['movieId'].value_counts()/len(all_users['userId'].unique())
    
    #combine the percentage of simlar_users_rec and all_users_recs
    rec_percentage = pd.concat([similar_users_recs,all_users_recs],axis=1)
    rec_percentage.columns = ['similar','all']
    
    #we want movies that have big bifference between the two numbers
    rec_percentage['score'] = rec_percentage['similar']/rec_percentage['all'] 
    #sort_values
    rec_percentage = rec_percentage.sort_values('score',ascending=False)
    #get top 10  recommendations
    rec_movies =  rec_percentage.head(10).merge(movies,left_index=True , right_on='movieId')[['title','genres','score']]

    return rec_movies.title.to_dict()


app = Flask('movie')

@app.route('/recommend', methods=['POST'])

def recommend():
    title_dict = request.get_json()
    title = title_dict["title"]

    movie_id = movies.loc[(movies.title ==title),'movieId'].values[0]
    
    recommendation =  find_similar_movies(movie_id)

    return jsonify(recommendation)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)

    
##ps = preprocessing_single(single_dict=d)
#result = predict_single(trained_models=loaded_models,df_single=ps)
#print("Predictions : ",result)



