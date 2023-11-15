<script setup>
  defineProps({
    name: String
  })
</script>

<template>
  <div class="badge">
    {{ name }}
  </div>
</template>

<style scoped>
  .badge {
    height: 20px;
    cursor: pointer;
    font-family: 'Pretendard-ExtraLight';
  }
</style>
