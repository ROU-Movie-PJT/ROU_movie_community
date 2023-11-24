<script setup>
  import { useRoute, useRouter } from 'vue-router'
  import { ref, computed } from 'vue'
  import { useMovieStore } from '../stores/movies';
  import { useCommunityStore } from '../stores/community'

  const route = useRoute()
  const router = useRouter()
  const store = useMovieStore()
  const communityStore = useCommunityStore()

  const movieId = ref(route.params.movieId)

  const isReview = computed(() => {
    return movieId.value !== '0'
  })

  const isEdit = computed(() => {
    return route.params.name === 'community_update'
  })

  const title = ref('')
  const content = ref('')

  const createReview = function () {
    if (title.value === '' | content.value === '') {
      window.alert('제목과 내용을 작성해주세요')
    } else {
      const payload = {
        title:  title.value,
        content: content.value,
        movieId: movieId.value
      }
      if (isReview.value) {
        communityStore.createMovieReview(payload)
      } else {
        communityStore.createReview(payload)
      }
    }
  }

  const goBack = function () {
    router.go(-1)
  }
</script>

<template>
  <div class="content-box">
    <h3 v-if="isReview" class="h3"><b>{{ store.movieDetail.title }}</b> 리뷰</h3>
    <form class="create-form" @submit.prevent="createReview">
      <input class="input" type="text" id="title" placeholder="제목을 입력하세요" v-model.trim="title">
      <textarea class="textarea" id="content" rows="10" placeholder="내용을 입력하세요" v-model.trim="content"></textarea>
      <div class="buttons">
        <button class="btn btn-secondary" @click.prevent="goBack">뒤로 가기</button>
        <button class="btn btn-signature" type="submit">작성하기</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
  .content-box {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .create-form {
    width: 60%;
    display: flex;
    flex-direction: column;
    padding: 2rem;
    gap: 1rem;
  }

  .input {
    border-radius: 10px;
    outline: none;
    padding: .5rem 1rem;
  }

  .textarea {
    border-radius: 10px;
    resize: none;
    outline: none;
    padding: 1rem;
  }
  
  .buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }

  .h3 {
    color: white;
  }

  .btn-signature {
    background-color: #7B61FF;
    color: white;
  }

  .btn-signature:hover {
    background-color: #7459fb;
    color: white;
  }
</style>