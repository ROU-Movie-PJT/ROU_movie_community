<script setup>
  defineProps({
    actor: Object
  })

  const image = function(path) {
    return `https://image.tmdb.org/t/p/original/${path}`
  }
</script>

<template>
  <div class="actor-content">
    <img v-if="actor.profile_path" class="profile-img" :src="image(actor.profile_path)" alt="">
    <img v-else class="profile-img" src="../../assets/profile.png" alt="">
    <p class="name">{{ actor.name }}</p>
  </div>
</template>

<style scoped>
  .actor-content {
    display: flex;
    height: 60px;
    align-items: center;
    gap: 1rem;
    width: 32%;
  }
  .profile-img {
    height: 100%;
    border-radius: 50%;
    background-color: gainsboro;
  }
  .name {
    margin: 0;
    color: white;
  }
</style>
