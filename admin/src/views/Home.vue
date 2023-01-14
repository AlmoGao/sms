<template>
  <div class="page">
    <div class="page-nav">
      <Navs />
    </div>
    <div class="page-content">
      <router-view/>
    </div>
  </div>
</template>

<script setup>
import Navs from '../components/Navs.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const token = sessionStorage.getItem('token')
if (!token) {
  router.replace({ name: 'login' })
} 

</script>

<style lang="less" scoped>
.page {
  width: 100%;
  height: 100%;
  display: flex;
  background-color: #fff;
  .page-nav {
    height: 100%;
    overflow-y: auto;
    background-color: #20262c;
  }
  .page-content {
    flex: 1;
    height: 100%;
    overflow: hidden;
    background-image: url('../assets/bg.jpg');
    background-size: cover;
  }
}
</style>
