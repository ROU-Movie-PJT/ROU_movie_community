<script setup>
  import { ref, computed } from 'vue'
  import axios from 'axios'

  const props = defineProps({
    movie: Object
  })

  const trailer = ref(null)

  axios({
    method: 'get',
    url: 'https://www.googleapis.com/youtube/v3/search',
    params: {
      key: import.meta.env.VITE_YOUTUBE_API_KEY,
      part: 'snippet',
      type: 'video',
      q: `${props.movie.title} 공식 예고편`
    }
  })
    .then(res => {
      trailer.value = res.data.items[0]
      // console.log(trailer.value.id.videoId)
    })
    .catch(err => {
      console.log(err)
    })

  const isNotEmpty = computed(() => {
    return trailer.value !== null
  })

  const getVideoUrl = function() {
    return `https://www.youtube.com/embed/${trailer.value.id.videoId}`
  }
</script>

<template>
  <div class="modal fade" tabindex="-1" id="trailerModal">
    <div class="modal-dialog">
      <div v-if="isNotEmpty" class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ movie.title }} 예고편</h4> 
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <iframe :src="getVideoUrl()" frameborder="0" width="100%" height="300px"></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .modal-title {
    color: black;
  }
</style>