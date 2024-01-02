import pandas as pd
import numpy as np


def prepare_dataframe(df):
    df_cleaned = df.apply(pd.to_numeric, errors='coerce').fillna(0)
    return df_cleaned

def cosine_similarity(v, u):
    return np.dot(v, u) / (np.linalg.norm(v) * np.linalg.norm(u))

def recommend_svd(df, user_id):
    user_id = int(user_id)
    if user_id not in df.index:
        raise ValueError(f"User ID {user_id} not found in the DataFrame.")

    U, S, VT = np.linalg.svd(df.values, full_matrices=False)
    user_index = df.index.get_loc(user_id)
    user_row = df.iloc[user_index].values
    similarities = np.array([cosine_similarity(user_row, VT[:, i]) for i in range(VT.shape[1])])
    sorted_movie_indices = np.argsort(-similarities)
    unwatched_movies = [i for i in sorted_movie_indices if df.iloc[user_index, i] == 0]
    top_10_recommendations = df.columns[unwatched_movies][:10]

    return top_10_recommendations

def svd(user_id):
    file_url = 'https://s3.eu-west-3.amazonaws.com/dauphine.projet/df.csv'
    df = pd.read_csv(file_url, index_col='user_id')
    df = prepare_dataframe(df)

    try:
        recommendations = recommend_svd(df, user_id)
        return {"Top 10 Recommendations": recommendations.tolist()}
    except ValueError as e:
        return {"Error": str(e)}
