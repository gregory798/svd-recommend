import pandas as pd
import numpy as np
import requests
from io import StringIO
import pickle
import os



def als_online(user_id):
    user_id = int(user_id)
    df_url = 'https://s3.eu-west-3.amazonaws.com/dauphine.projet/df.csv'
    metadata_url = 'https://s3.eu-west-3.amazonaws.com/dauphine.projet/movie_metadata.pkl'

    try:
        # Loading user-movie interaction data
        df_response = requests.get(df_url)
        df_response.raise_for_status()
        df = pd.read_csv(StringIO(df_response.text), index_col='user_id')

        # Normalizing the data
        mean_user_rating = df.replace(0, np.NaN).mean(axis=1)
        df_centered = df.sub(mean_user_rating, axis=0).fillna(0)

        # ALS parameters (we can increase these parameters, but it will be slower ...)
        n_factors = 2
        n_iterations = 2
        lambda_reg = 0.1

        # Initializing user and item matrices
        n_users, n_items = df_centered.shape
        X = np.random.rand(n_users, n_factors)
        Y = np.random.rand(n_items, n_factors)

        # ALS algorithm simplified
        def ALS(X, Y, df, lambda_reg, n_iterations):
            for iteration in range(n_iterations):
                for u in range(n_users):
                    X[u] = np.linalg.solve(np.dot(Y.T, Y) + lambda_reg * np.eye(n_factors),
                                            np.dot(Y.T, df.values[u, :]))
                for i in range(n_items):
                    Y[i] = np.linalg.solve(np.dot(X.T, X) + lambda_reg * np.eye(n_factors),
                                            np.dot(X.T, df.values[:, i]))
            return X, Y

        X, Y = ALS(X, Y, df_centered, lambda_reg, n_iterations)
        predicted_ratings = np.dot(X, Y.T)
        predicted_ratings_df = pd.DataFrame(predicted_ratings, index=df.index, columns=df.columns)

        # Loading movie metadata
        metadata_response = requests.get(metadata_url)
        metadata_response.raise_for_status()
        movie_metadata = pickle.loads(metadata_response.content)

        # Function to recommend top N movies for a user
        def recommend_movies(user_id, top_n=10):
            user_ratings = predicted_ratings_df.loc[user_id]
            already_rated = df.loc[user_id]
            user_ratings[already_rated != 0] = -np.inf  # Exclude already rated movies

            # Mapping movie IDs to titles
            recommended_movie_ids = user_ratings.nlargest(top_n).index
            recommended_movie_titles = [movie_metadata[movie_id]['title'] for movie_id in recommended_movie_ids]
            return recommended_movie_titles

        recommended_movies = recommend_movies(user_id, 10)
        return {"Top 10 Recommendations": recommended_movies}

    except requests.exceptions.HTTPError as http_err:
        return {"Error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as e:
        return {"Error": f"Error occurred: {e}"}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}
    

def als(user_id):
    user_id = int(user_id)
    base_dir = r'C:\Users\grego\Desktop\svd-recommend\back' # Change the absolute path !
    df_file_path = os.path.join(base_dir, 'df.csv')
    metadata_file_path = os.path.join(base_dir, 'movie_metadata.pkl')

    try:
        # Loading user-movie interaction data from local file
        df = pd.read_csv(df_file_path, index_col='user_id')

        # Normalizing the data
        mean_user_rating = df.replace(0, np.NaN).mean(axis=1)
        df_centered = df.sub(mean_user_rating, axis=0).fillna(0)

        # ALS parameters
        n_factors = 2
        n_iterations = 2
        lambda_reg = 0.1

        # Initializing user and item matrices
        n_users, n_items = df_centered.shape
        X = np.random.rand(n_users, n_factors)
        Y = np.random.rand(n_items, n_factors)

        # ALS algorithm simplified
        def ALS(X, Y, df, lambda_reg, n_iterations):
            for iteration in range(n_iterations):
                for u in range(n_users):
                    X[u] = np.linalg.solve(np.dot(Y.T, Y) + lambda_reg * np.eye(n_factors),
                                            np.dot(Y.T, df.values[u, :]))
                for i in range(n_items):
                    Y[i] = np.linalg.solve(np.dot(X.T, X) + lambda_reg * np.eye(n_factors),
                                            np.dot(X.T, df.values[:, i]))
            return X, Y

        X, Y = ALS(X, Y, df_centered, lambda_reg, n_iterations)
        predicted_ratings = np.dot(X, Y.T)
        predicted_ratings_df = pd.DataFrame(predicted_ratings, index=df.index, columns=df.columns)

        # Loading movie metadata from local file
        with open(metadata_file_path, 'rb') as file:
            movie_metadata = pickle.load(file)

        # Function to recommend top N movies for a user
        def recommend_movies(user_id, top_n=10):
            user_ratings = predicted_ratings_df.loc[user_id]
            already_rated = df.loc[user_id]
            user_ratings[already_rated != 0] = -np.inf  # Exclude already rated movies

            # Mapping movie IDs to titles
            recommended_movie_ids = user_ratings.nlargest(top_n).index
            recommended_movie_titles = [movie_metadata[movie_id]['title'] for movie_id in recommended_movie_ids]
            return recommended_movie_titles

        recommended_movies = recommend_movies(user_id, 10)
        return {"Top 10 Recommendations": recommended_movies}

    except Exception as e:
        return {"Error": f"An unexpected error occurred: {str(e)}"}