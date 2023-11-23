# # from sklearn.feature_extraction.text import TfidfVectorizer
# # from sklearn.metrics.pairwise import linear_kernel
# # from django.contrib.auth.models import User
# # from .models import *
# # import pandas as pd
# # from django.contrib.auth import get_user_model

# # User = get_user_model()


# # def recommend_movies(title):
# #     # Create a DataFrame with the relevant movie information
# #     df = pd.DataFrame.from_records(Movie.objects.all().values(
# #         'title', 'overview', 'vote_count', 'vote_average', 'popularity'
# #     ))

# #      # 사용자 선호도에 따라 영화 필터링
# #     #  user_instance = User.objects.get(pk=user_id)
# #     user_like_genres = User.like_genres.all()
# #     user_hate_genres = User.hate_genres.all()
# #     # user_like_genres = User.like_genres.all().values_list('name', flat=True)
# #     # user_hate_genres = User.hate_genres.all().values_list('name', flat=True)
# #     df = df[df['genre'].apply(lambda x: x in user_like_genres and x not in user_hate_genres)]

# #     # Generate TF-IDF matrix
# #     tfidf = TfidfVectorizer(stop_words='english')
# #     tfidf_matrix = tfidf.fit_transform(df['overview'])

# #     # Compute cosine similarity matrix
# #     cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# #     # Create a Series with movie titles indexed by their DataFrame index
# #     indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# #     idx = indices.get(title)
# #     if idx is None:
# #         return []  # 제목이 목록에 없으면 빈 리스트 반환

# #     sim_scores = list(enumerate(cosine_sim[idx]))
# #     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
# #     sim_scores = sim_scores[1:21]  # 가장 유사한 20개의 영화 선택

# #     movie_indices = [i[0] for i in sim_scores]

# #     # movie_indices를 사용하여 추천된 영화의 제목을 가져오기
# #     recommended_titles = df['title'].iloc[movie_indices]

# #     # 추천된 제목과 일치하는 Movie 인스턴스 검색
# #     recommended_movie_instances = Movie.objects.filter(title__in=recommended_titles)
# #     return recommended_movie_instances


# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from django.contrib.auth import get_user_model  # User 모델을 가져옴
# from .models import *
# import pandas as pd

# User = get_user_model()  # 현재 사용 중인 User 모델을 가져옴

# def recommend_movies(user_id, title):
#     try:
#         # 현재 로그인한 사용자의 정보를 가져옴
#         user_instance = User.objects.get(pk=user_id)

#         # 사용자 선호도에 따라 영화 필터링
#         user_like_genres = user_instance.like_genres.all()
#         user_hate_genres = user_instance.hate_genres.all()

#         # 선호하는 장르에 속하고 싫어하는 장르에 속하지 않는 영화만 필터링
#         movies = Movie.objects.filter(genres__in=user_like_genres).exclude(genres__in=user_hate_genres)

#         # 필터링된 영화들로부터 DataFrame 생성
#         df = pd.DataFrame.from_records(movies.values(
#             'title', 'overview', 'vote_count', 'vote_average', 'popularity'
#         ))

#         # Generate TF-IDF matrix
#         tfidf = TfidfVectorizer(stop_words='english')
#         tfidf_matrix = tfidf.fit_transform(df['overview'])

#         # Compute cosine similarity matrix
#         cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#         # Create a Series with movie titles indexed by their DataFrame index
#         indices = pd.Series(df.index, index=df['title']).drop_duplicates()

#         idx = indices.get(title)
#         if idx is None:
#             return []  # 제목이 목록에 없으면 빈 리스트 반환

#         sim_scores = list(enumerate(cosine_sim[idx]))
#         sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#         sim_scores = sim_scores[1:21]  # 가장 유사한 20개의 영화 선택

#         movie_indices = [i[0] for i in sim_scores]

#         # movie_indices를 사용하여 추천된 영화의 제목을 가져오기
#         recommended_titles = df['title'].iloc[movie_indices]

#         # 추천된 제목과 일치하는 Movie 인스턴스 검색
#         recommended_movie_instances = Movie.objects.filter(title__in=recommended_titles)
#         return recommended_movie_instances

#     except User.DoesNotExist:
#         return []


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.contrib.auth import get_user_model  # User 모델을 가져옴
from .models import *
import pandas as pd

User = get_user_model()


def recommend_movies(user_id, title):
    try:
        # 현재 로그인한 사용자의 정보를 가져옴
        user_instance = User.objects.get(pk=user_id)

        # 사용자 선호도에 따라 영화 필터링
        user_like_genres = user_instance.like_genres.all()
        user_hate_genres = user_instance.hate_genres.all()

        # 선호하는 장르에 속하고 싫어하는 장르에 속하지 않는 영화만 필터링
        movies = Movie.objects.filter(genres__in=user_like_genres).exclude(
            genres__in=user_hate_genres)

        # 필터링된 영화들로부터 DataFrame 생성
        df = pd.DataFrame.from_records(movies.values(
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
        sim_scores = sim_scores[1:21]  # 가장 유사한 20개의 영화 선택

        movie_indices = [i[0] for i in sim_scores]


        # movie_indices를 사용하여 추천된 영화의 제목을 가져오기
        recommended_titles = df['title'].iloc[movie_indices]


        # 추천된 제목과 일치하는 Movie 인스턴스 검색
        recommended_movie_instances = Movie.objects.filter(
            title__in=recommended_titles)
        return recommended_movie_instances

    except User.DoesNotExist:
        return []
