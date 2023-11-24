from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.contrib.auth import get_user_model
from .models import Movie
import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import MovieRecommendSerializer

User = get_user_model()

def recommend_movies(user_id, title):
    try:
        user_instance = User.objects.get(pk=user_id)
        user_like_genres = user_instance.like_genres.all()
        user_hate_genres = user_instance.hate_genres.all()

        movies = Movie.objects.filter(genres__in=user_like_genres).exclude(
            genres__in=user_hate_genres)

        df = pd.DataFrame.from_records(movies.values(
            'title', 'overview', 'vote_count', 'vote_average', 'popularity'
        ))

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['overview'].dropna())

        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        indices = pd.Series(df.index, index=df['title']).drop_duplicates()

        idx = indices.get(title)
        if idx is None:
            return []

        sim_scores = list(enumerate(cosine_sim[idx]))
        # Ensure that sim_scores are in the correct format
        sim_scores = [(i, score) for i, score in sim_scores if isinstance(score, (int, float))]

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:21]

        movie_indices = [i[0] for i in sim_scores]
        recommended_titles = df['title'].iloc[movie_indices]

        recommended_movie_instances = Movie.objects.filter(
            title__in=recommended_titles)
        return recommended_movie_instances

    except User.DoesNotExist:
        return []
    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return []
