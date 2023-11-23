<script setup>
  import { ref, computed } from 'vue'

  const props = defineProps({
    movie: Object
  })

  const isNotEmpty = computed(() => {
    return props.movie.videos !== null
  })

  const getVideoUrl = function() {
    return `https://www.youtube.com/embed/${props.movie.videos}`
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