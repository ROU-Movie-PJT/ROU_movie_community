<script setup>
  defineProps({
    name: String
  })
</script>

<template>
  <a class="badge">
    {{ name }}
  </a>
</template>

<style scoped>
  .badge {
    height: 20px;
    cursor: pointer;
    font-family: 'Pretendard-ExtraLight';
    text-decoration: none;
  }
</style>
