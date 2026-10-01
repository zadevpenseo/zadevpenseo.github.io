# Book Recommendation Engine using KNN - freeCodeCamp Machine Learning with Python Project 3
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def get_recommends(book="Where the Heart Is (Oprah's Book Club (Paperback))", df_books=None, df_ratings=None):
    if df_books is None or df_ratings is None:
        # Load Data if not provided
        df_books = pd.read_csv("BX-Books.csv", encoding="iso-8859-1", sep=";", header=0, names=['isbn', 'title', 'author'], usecols=['isbn', 'title', 'author'], dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})
        df_ratings = pd.read_csv("BX-Book-Ratings.csv", encoding="iso-8859-1", sep=";", header=0, names=['user', 'isbn', 'rating'], usecols=['user', 'isbn', 'rating'], dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})

    # Filter out users with less than 200 ratings and books with less than 100 ratings
    user_counts = df_ratings['user'].value_counts()
    book_counts = df_ratings['isbn'].value_counts()

    df_ratings_filtered = df_ratings[
        (df_ratings['user'].isin(user_counts[user_counts >= 200].index)) &
        (df_ratings['isbn'].isin(book_counts[book_counts >= 100].index))
    ]

    # Merge ratings with books
    df_combined = pd.merge(df_ratings_filtered, df_books, on='isbn')
    df_combined = df_combined.drop_duplicates(subset=['title', 'user'])

    # Create pivot table
    df_pivot = df_combined.pivot(index='title', columns='user', values='rating').fillna(0)
    matrix = csr_matrix(df_pivot.values)

    # Build model
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(matrix)

    # Get recommendations
    distances, indices = model_knn.kneighbors(df_pivot.loc[book].values.reshape(1, -1), n_neighbors=6)
    
    recommended_books = []
    for i in range(1, len(distances.flatten())):
        recommended_books.append([df_pivot.index[indices.flatten()[i]], distances.flatten()[i]])
    
    # Needs to be sorted by distance descending for FCC test
    recommended_books.sort(key=lambda x: x[1], reverse=True)
    
    return [book, recommended_books]
