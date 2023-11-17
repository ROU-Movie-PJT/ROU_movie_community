<script setup>
  import { ref } from 'vue'
  import MovieDetailInfo from '../components/movie/MovieDetailInfo.vue'
  const info = ref(
    {
      "adult": false,
      "backdrop_path": "/mSDsSDwaP3E7dEfUPWy4J0djt4O.jpg",
      "genre_ids": [
          16,
          10751,
          14
      ],
      "id": 129,
      "original_language": "ja",
      "original_title": "千と千尋の神隠し",
      "overview": "평범한 열 살 짜리 소녀 치히로 식구는 이사 가던 중 길을 잘못 들어 낡은 터널을 지나가게 된다. 터널 저편엔 폐허가 된 놀이공원이 있었고 그곳엔 이상한 기운이 흘렀다. 인기척 하나 없는 이 마을의 낯선 분위기에 불길한 기운을 느낀 치히로는 부모님에게 돌아가자고 조르지만 부모님은 호기심에 들떠 마을 곳곳을 돌아다니기 시작한다. 어느 음식점에 도착한 치히로의 부모님은 그 곳에 차려진 음식들을 보고 즐거워하며 허겁지겁 먹어대다가 돼지로 변해버린다. 겁에 질려 당황하는 치히로에게 낯선 소년 하쿠가 나타나 빨리 이곳을 나가라고 소리치는데...",
      "popularity": 106.424,
      "poster_path": "/rIKWsMItjBLrgt51Xpk4MNAUQe2.jpg",
      "release_date": "2001-07-20",
      "title": "센과 치히로의 행방불명",
      "video": false,
      "vote_average": 8.54,
      "vote_count": 15083
    }
  )
</script>

<template>
  <div class="container">
    <MovieDetailInfo v-if="info" :info="info" />
  </div>
</template>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
  }
</style>