<script setup>
  import { ref } from 'vue'
  const isSearching = ref(false)
</script>

<template>
  <div class="header">
    <nav class="header-nav">
      <button class="login-btn">로그인</button>
      <form class="search-bar">
        <input class="input-text" type="text" placeholder="영화 제목, 감독 이름으로 검색 가능">
        <button v-if="!isSearching" class="search-btn" type="submit">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g clip-path="url(#clip0_10_294)">
              <path d="M12.5322 19.0332C13.9297 19.0332 15.2393 18.6113 16.3291 17.8906L20.1787 21.749C20.4336 21.9951 20.7588 22.1182 21.1104 22.1182C21.8398 22.1182 22.376 21.5469 22.376 20.8262C22.376 20.4922 22.2617 20.167 22.0156 19.9209L18.1924 16.0801C18.9834 14.9551 19.4492 13.5928 19.4492 12.1162C19.4492 8.31055 16.3379 5.19922 12.5322 5.19922C8.73535 5.19922 5.61523 8.31055 5.61523 12.1162C5.61523 15.9219 8.72656 19.0332 12.5322 19.0332ZM12.5322 17.1875C9.74609 17.1875 7.46094 14.9023 7.46094 12.1162C7.46094 9.33008 9.74609 7.04492 12.5322 7.04492C15.3184 7.04492 17.6035 9.33008 17.6035 12.1162C17.6035 14.9023 15.3184 17.1875 12.5322 17.1875Z" fill="#3C3C43" fill-opacity="0.6"/>
            </g>
            <defs>
              <clipPath id="clip0_10_294">
                <rect width="28" height="28" fill="white"/>
              </clipPath>
            </defs>
          </svg>
        </button>
        <button v-else class="cancel-btn">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: text-bottom;">
            <path d="M9 18C13.9235 18 18 13.9147 18 9C18 4.07647 13.9147 0 8.99118 0C4.07647 0 0 4.07647 0 9C0 13.9147 4.08529 18 9 18ZM5.88529 12.8471C5.48823 12.8471 5.16176 12.5118 5.16176 12.1059C5.16176 11.9118 5.24118 11.7353 5.37353 11.5941L7.95882 9.00882L5.37353 6.42353C5.24118 6.28235 5.16176 6.10588 5.16176 5.91176C5.16176 5.50588 5.48823 5.18824 5.88529 5.18824C6.09706 5.18824 6.26471 5.25882 6.39706 5.4L8.99118 7.98529L11.6118 5.39118C11.7618 5.24118 11.9206 5.17059 12.1147 5.17059C12.5118 5.17059 12.8382 5.49706 12.8382 5.89412C12.8382 6.09706 12.7765 6.25588 12.6265 6.41471L10.0324 9.00882L12.6176 11.5853C12.7588 11.7353 12.8294 11.9029 12.8294 12.1059C12.8294 12.5118 12.5029 12.8471 12.0971 12.8471C11.8941 12.8471 11.7176 12.7588 11.5765 12.6265L8.99118 10.0412L6.42353 12.6265C6.28235 12.7676 6.09706 12.8471 5.88529 12.8471Z" fill="#3C3C43" fill-opacity="0.6"/>
          </svg>
        </button>
      </form>
    </nav>
  </div>
</template>

<style scoped>
  .header {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding-left: 200px;
    z-index: 500;
  }

  .header-nav {
    display: flex;
    position: relative;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
    height: 56px;
    padding: 12px 40px;
    background-color: #222222;
    gap: 1rem;
    font-size: 18px;
  }

  .search-bar {
    border: 1px solid gainsboro;
    border-radius: 10px;
    background-color: white;
    overflow: hidden;
    font-size: 1rem;
    width: 20%;
    display: flex;
    justify-content: space-between;
    padding: 0 5px;
  }

  .input-text {
    border: none;
    background-color: rgba(0, 0, 0, 0);
    color: black;
    font-size: small;
    width: 80%;
  }

  .input-text:focus {
    outline: none;
  }

  .cancel-btn {
    border: none;
    background-color: white;
  }

  .search-btn {
    border: none;
    background-color: white;
  }
  
  .login-btn {
    border: none;
    border-radius: 5px;
    font-size: 1rem;
  }

  @media screen and (max-width: 47em) {
    .header {
      padding-left: 0;
    }
  }
</style>