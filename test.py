from pydoc import plain
from typing import final
import pandas as pd
#import numpy as np
#import pickle
import streamlit as st


@st.cache(allow_output_mutation = True)
def load_artifacts():
    movies = pd.read_csv('artifacts//movies.csv')
    ratings = pd.read_csv('artifacts//ratings.csv')
    return movies,ratings

movies, ratings = load_artifacts()

titles = movies.title.unique()


#show_cols = ['Player','Team','Year','Career'] 

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

    return rec_movies

def submit():
    st.title('Movie Recommendation System')
    st.image("""shawshank.jpg""")
    st.header('Movie Title')

    title = st.selectbox(
     'Search Title :', titles)

    movie_id = movies.loc[(movies.title ==title),'movieId'].values[0]

    recommendation = find_similar_movies(movie_id)
    
    if st.button('Get Recommendation'):
        st.write("Similar Users Liked : ")  
        st.write("")
        st.dataframe(recommendation)


if __name__ == '__main__':
    submit()
