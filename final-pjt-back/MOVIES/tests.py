from django.test import TestCase
from MOVIES.models import *
# Create your tests here.
# 
from django.test import TestCase

# Create your tests here.

# @api_view(['GET'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def api_test_TT(request):
#     Trend.objects.all().delete()

#     params = {
#         'language': 'ko',
#         'api_key': TMDB_API_KEY,
#     }
#     response = requests.get(TMDB_TRENDING_BASE_URL, params=params).json()
#     movie_trend = response['results']

#     for movie in movie_trend:
#         trend_serializer = TrendSerializer(data=movie)
#         if trend_serializer.is_valid(raise_exception=True):
#             trend_serializer.save()

#     return JsonResponse({'message': 'Success'})



#                     runtime = response['runtime']
#                     video = response['videos']['results'][0].get('key')
#                     

#                     movie['video'] = video    
#                                    
#                     movie_serializer = MovieSerializer(data=movie)

#                     if movie_serializer.is_valid(raise_exception=True):
#                         movie_id = movie['id']
#                         if movie['release_date'] == '':
#                             movie['release_date'] = None
#                         if movie['video'] == '':
#                             movie['video'] = None    
#                         movie_serializer.save(movie_id = movie_id, release_date=movie['release_date'], director=movie['director'], video=movie['video'])




@permission_classes([IsAuthenticatedOrReadOnly])
class FetchTMDBPopularMovies(APIView):

    def get(self, request, format=None):
        async_to_sync(self.fetch_all_movies)()  # async_to_sync를 사용하여 비동기 함수 호출
        return Response({'message': 'Success'})

    async def fetch_all_movies(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_movie_page(session, page)
                     for page in range(1, 501)]
            await asyncio.gather(*tasks)

    async def fetch_movie_page(self, session, page):
        params = {
            'language': 'ko-KR',
            'api_key': TMDB_API_KEY,
            'page': page
        }
        try:
            response = await session.get(TMDB_POPULAR_BASE_URL, params=params)
            data = await response.json()
            movie_list = data['results']
            await asyncio.gather(*[self.process_movie(movie) for movie in movie_list])
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error: {e}")

    async def process_movie(self, movie):
        await sync_to_async(self.save_movie)(movie)

    def save_movie(self, movie):
        movie_id = movie['id']
        movie_data = {
            'like_movie_users_count': 0,
            'dislike_movie_users_count': 0,
            'watching_movie_users_count': 0,
            'favorite_movie_users_count': 0,
        }
        # Update movie_data with the actual movie data
        movie_data.update(movie)
        movie_serializer = MovieSerializer(data=movie_data)
        if movie_serializer.is_valid(raise_exception=True):
            if movie['release_date'] == '':
                movie['release_date'] = None
            movie_serializer.save(
                movie_id=movie_id, release_date=movie['release_date'])


@permission_classes([IsAuthenticatedOrReadOnly])
class UpdateTMDBMovieDetails(APIView):

    def get(self, request, format=None):
        async_to_sync(self.update_movies_with_additional_details)()
        return Response({'message': 'Movie details updated successfully'})

    async def update_movies_with_additional_details(self):
        movies = await sync_to_async(list)(Movie.objects.all())
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.update_movie_detail(session, movie) for movie in movies])

    async def update_movie_detail(self, session, movie):
        movie_id = movie.movie_id
        detail_url = f'{TMDB_DETAIL_INFO_BASE_URL}{movie_id}'
        params = {
            'language': 'ko-KR',
            'api_key': TMDB_API_KEY,
            'append_to_response': 'credits,videos',
        }

        response = await session.get(detail_url, params=params)
        details = await response.json()

        # Check if the required data is available
        if 'credits' in details and 'genres' in details and 'videos' in details:
            await sync_to_async(self.save_movie_details)(movie, details)
        else:
            logging.error(
                f"Required data missing in API response for movie ID {movie_id}")

    def save_movie_details(self, movie, details):
        movie.runtime = details.get('runtime')
        director = next((crew['name'] for crew in details['credits']
                        ['crew'] if crew['job'] == 'Director'), None)
        movie.director = director

        # Update actors and genres
        # video = response['videos']['results'][0].get('key')
        videos_data = details['videos']['results'] if 'videos' in details else [
        ]
        actors_data = details['credits']['cast'] if 'credits' in details else [
        ]
        genres_data = details['genres'] if 'genres' in details else []
        actors = [self.update_or_create_actor(actor) for actor in actors_data]
        genres = [self.update_or_create_genre(genre) for genre in genres_data]

        movie.actors.set(actors)
        movie.genres.set(genres)
        # movie.genres.set(videos)

        movie.save()


    def update_or_create_actor(self, actor_data):
        actor, _ = Actor.objects.update_or_create(
            person_id=actor_data['id'],
            defaults={
                'name': actor_data['name'], 'profile_path': actor_data.get('profile_path')}
        )
        return actor

    def update_or_create_genre(self, genre_data):
        genre, _ = Genre.objects.update_or_create(
            genre_id=genre_data['id'],
            defaults={'name': genre_data['name']}
        )
        return genre

# TMDB Genre 정보


@api_view(['GET'])
def api_test_TG(request):
    params = {
        'language': 'ko',
        'api_key': TMDB_API_KEY,
    }
    response = requests.get(TMDB_GENRE_BASE_URL, params=params).json()
    movie_genres = response['genres']

    for genre in movie_genres:
        genre_serializer = GenreSerializer(data=genre)
        if genre_serializer.is_valid(raise_exception=True):
            genre_id = genre['id']
            genre_serializer.save(genre_id=genre_id)
    return JsonResponse({'message': 'Success'})

# TMDB 영화 트렌드
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_test_TT(request):
    params = {
        'language': 'ko',
        'api_key': TMDB_API_KEY,
    }
    response = requests.get(TMDB_TRENDING_BASE_URL, params=params).json()
    movies_trend = response['results']
    

    for movie in movies_trend:
        trend_serializer = TrendSerializer(data=movie)
        if trend_serializer.is_valid(raise_exception=True):
            trend_serializer.save(movie_id=movie['id'])

    return JsonResponse({'message': 'Success'})

