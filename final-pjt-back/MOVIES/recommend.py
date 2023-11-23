from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Movie
import pandas as pd

def recommend_movies(title):
    # Create a DataFrame with the relevant movie information
    df = pd.DataFrame.from_records(Movie.objects.all().values(
        'title', 'overview', 'vote_count', 'vote_average', 'popularity'
    ))

    # Generate TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['overview'])

    # Compute cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Create a Series with movie titles indexed by their DataFrame index
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    idx = indices.get(title)
    if idx is None:
        return []  # 제목이 목록에 없으면 빈 리스트 반환

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:22]  # 가장 유사한 10개의 영화 선택

    movie_indices = [i[0] for i in sim_scores]
    
    # movie_indices를 사용하여 추천된 영화의 제목을 가져오기
    recommended_titles = df['title'].iloc[movie_indices]

    # 추천된 제목과 일치하는 Movie 인스턴스 검색
    recommended_movie_instances = Movie.objects.filter(title__in=recommended_titles)
    return recommended_movie_instances
