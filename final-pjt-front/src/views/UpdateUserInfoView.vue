<script setup>
  import { ref, onMounted } from 'vue'
  import { useUserStore } from '../stores/user';

  const userStore = useUserStore()

  const profileImage = ref(userStore.userInfo.profile_image)
  const region = ref(userStore.userInfo.region)
  const birth = ref(userStore.userInfo.birth)
  const profileImageRef = ref()
  const imagePath = ref(userStore.userInfo.profile_image)
  const profilePath = ref(`http://localhost:8000${imagePath.value}`)

  onMounted(() => {
    userStore.getUserInfo()
  })
  
  const changeProfileImage = function () {
    profilePath.value = window.URL.createObjectURL(profileImageRef.value.files[0])
    const formData = new FormData()
    formData.append('files', profileImageRef.value.files[0])
    profileImage.value = formData
  }

  const updateInfo = function () {
    const payload = {
      profileImage: profileImage.value,
      region: region.value,
      birth: birth.value
    }
    userStore.updateUserInfo(payload)
  }
</script>

<template>
  <div class="content-box">
    <div class="update-box">
      <h2><b>회원 정보 수정</b></h2>
      <form class="update-form" @submit.prevent="updateInfo">
        <div class="update-item">
          <label for="username">프로필 이미지</label>
          <div class="image-box">
            <img class="profile-image" v-if="userStore.userInfo.profile_image !== ''" :src="profilePath" alt="">
          </div>
          <input class="input" type="file" ref="profileImageRef" accept="image/*" @change="changeProfileImage">
        </div>
        <div class="update-item">
          <label for="region">지역</label>
          <input class="input" type="text" v-model="region">
        </div>
        <div class="update-item">
          <label for="birth">생년월일</label>
          <input class="input" type="date" v-model="birth">
        </div>
        <hr>
        <button type="submit" class="update-btn">수정</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
  .content-box {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .update-box {
    text-align: center;
    width: 40%;
    background-color: gainsboro;
    padding: 1.5rem;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }

  .update-form {
    display: flex;
    flex-direction: column;
    gap: .5rem;
  }
  
  .update-item {
    display: flex;
    flex-direction: column;
    text-align: start;
    gap: .25rem;
  }

  .update-btn {
    width: 100%;
    border: none;
    background-color: #7B61FF;
    border-radius: 5px;
    color: white;
    padding: .5rem;
    height: 40px;
  }

  .input {
    height: 40px;
    border: none;
    border-radius: 5px;
    outline: none;
    padding: 0 .5rem;
  }

  .image-box {
    border-radius: 50%;
    overflow: hidden;
    width: 80px;
    height: 80px;
    align-self: center;
  }

  .profile-image {
    width: 100%;
  }
</style>

