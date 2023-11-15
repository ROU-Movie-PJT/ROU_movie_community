<script setup>

</script>

<template>
  <div id="carouselExample" class="carousel slide">
    <div class="carousel-inner">
      <div class="carousel-item active">
        <iframe class="d-block video" src="https://www.youtube.com/embed/pyXcDMajSz4?si=yxrr3jscnJxXhwhG&amp;controls=0&autoplay=0&mute=1" title="YouTube video player" frameborder="0" allowfullscreen></iframe>
      </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<style scoped>
  .carousel {
    width: 100%;
    height: fit-content;
    display: flex;
  }

  .video {
    width: 100%;
    height: 55vh;
  }
</style>
