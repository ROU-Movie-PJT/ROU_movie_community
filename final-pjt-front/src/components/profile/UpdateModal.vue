<script setup>
  import { ref, computed, watch } from 'vue'
  import { useProfileStore } from '../../stores/profile'
  import { useUserStore } from '../../stores/user'
  const userStore = useUserStore()
  const profileStore = useProfileStore()
  const modalRef = ref()

  const isLike = computed(() => {
    return profileStore.pType === 'like'
  })

  const updateProfile = function () {
    if (profileStore.pType === 'hate') {
      modalRef.value.click()
    }
    profileStore.updateProfile()
  }
</script>

<template>
  <div class="modal fade" tabindex="-1" id="updateModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">모달 제목</h4> 
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" ref="modalRef"></button>
        </div>
        <div class="modal-body">
          <!-- like -->
          <div v-if="isLike" class="genre-list">
            <li class="list" v-for="choice in profileStore.likeChoice" :key="choice">
                <input class="btn-check" type="checkbox" :value="choice.genre" :id="choice.genre" :checked="choice.isSelected" v-model="choice.isSelected">
                <label :for="choice.genre" class="btn btn-outline-primary">{{ choice.genre }}</label>
            </li>
          </div>
          <!-- hate -->
          <div v-else class="genre-list">
            <li class="list" v-for="choice in profileStore.hateChoice" :key="choice">
                <input class="btn-check" type="checkbox" :value="choice.genre" :id="choice.genre" :checked="choice.isSelected" v-model="choice.isSelected">
                <label :for="choice.genre" class="btn btn-outline-primary">{{ choice.genre }}</label>
            </li>
          </div>
          
          <button class="btn btn-dark" @click="updateProfile">저장</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .list {
    list-style: none;
  }

  .modal-body {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
  }

  .genre-list {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }
</style>