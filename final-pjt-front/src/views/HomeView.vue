<script setup>
  import { ref, watch, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMovieStore } from '../stores/movies'
  import MovieCarousel from '../components/home/MovieCarousel.vue'
  import Badge from '../components/common/Badge.vue'
  import MovieCard from '../components/home/MovieCard.vue'
  import 'vue3-carousel/dist/carousel.css'
  import { Carousel, Slide, Navigation } from 'vue3-carousel'

  const store = useMovieStore()
  const router = useRouter()

  onMounted(() => {
    store.getRecommendMovies()
    store.getTrendMovies()
  })

  const favoriteGenres = ref({
    1: '액션',
    4: '코미디',
    9: '판타지',
  })

  const sortTitles = {
    20: '관객이 많은 영화 TOP 30',
    21: '최신 개봉 영화 TOP 30',
    22: '개봉 예정 영화 TOP 30',
    23: '평점이 높은 영화 TOP 30'
  }

  const viewMore = ref(false)
  const activeBadge = ref(20)

  const moreGenres = function() {
    viewMore.value = !viewMore.value
  }

  const selectBadge = function(badge) {
    activeBadge.value = badge
  }

  const goDetail = function(id) {
    router.push({name: 'movie_detail', params: {id: id}})
  }
</script>

<template>
  <div class="container">
    <!-- <MovieCarousel /> -->
    <div class="badges">
      <Badge 
        :class="{'text-bg-primary': activeBadge === 20, 'text-bg-secondary': activeBadge !== 20}" 
        name="TOP30"
        @click="selectBadge(20)"
        :href="'#'+activeBadge"
      />
      <Badge 
        v-for="genre in viewMore ? Object.keys(store.choice) : Object.keys(favoriteGenres)" 
        :class="{'text-bg-secondary': activeBadge !== genre, 'text-bg-primary': activeBadge === genre}" 
        :name="store.choice[genre]"
        @click="selectBadge(genre)"
        :href="'#'+activeBadge"
      />
      <Badge class="text-bg-light" @click="moreGenres" :name="viewMore ? 'X' : '더보기'" />
    </div>
    <div>
      <div class="movie-list" v-for="(title, key) in sortTitles" :key="title">
        <span :id="key" class="anchor"></span>
        <span class="sort-title">{{ title }}</span>
        <Carousel :items-to-show="7" :wrap-around="true">
          <template v-for="item in store.recommendMovies[key]" :key="item">
            <Slide v-if="item.poster_path" @click="goDetail(item.id)">
              <MovieCard class="carousel__item" :item=item />
            </Slide>
          </template>
          <template #addons>
            <Navigation />
          </template>
        </Carousel>
      </div>
      <div class="movie-list" v-for="key in 19" :key="key">
        <span :id="key" class="anchor"></span>
        <span class="sort-title">{{ store.choice[key] }}</span>
        <Carousel :items-to-show="7" :wrap-around="true">
          <template v-for="item in store.recommendMovies[key]" :key="item">
            <Slide v-if="item.poster_path" @click="goDetail(item.id)">
              <MovieCard class="carousel__item" :item=item />
            </Slide>
          </template>
          <template #addons>
            <Navigation />
          </template>
        </Carousel>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 80%;
    height: 100%;
    padding: 2rem 0;
    gap: 2rem;
  }

  .badges {
    width: 100%;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    z-index: 1;
  }

  .carousel__slide {
    margin: .5rem;
  }

  .sort-title {
    color: white;
  }

  .carousel {
    margin-bottom: 1rem;
  }

  .anchor{
    display: block;
    height: 56px;       /* 헤더의 height와 동일한 값 */
    margin-top: -56px;  /* 헤더의 height와 동일한 값 */
    visibility: hidden;
    z-index: 0;
}
</style>
