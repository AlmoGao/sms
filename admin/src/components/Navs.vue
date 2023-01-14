<template>
    <el-menu
        active-text-color="#ffd04b"
        background-color="#20262c"
        class="el-menu-vertical-demo"
        :default-active="active"
        text-color="#fff"
      >
        <el-menu-item :index="item.val" v-for="(item, i) in navs" :key="i" @click="goNav(item)">
          <el-icon v-if="i==0"><HomeFilled /></el-icon>
          <el-icon v-if="i==1"><Avatar /></el-icon>
          <el-icon v-if="i==2"><HelpFilled /></el-icon>
          <el-icon v-if="i==3"><Promotion /></el-icon>
          <el-icon v-if="i==4"><Comment /></el-icon>
          <el-icon v-if="i==5"><Histogram /></el-icon>
          <span>{{ item.name }}</span>
        </el-menu-item>
    </el-menu>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const active = computed(() => {
  const target = navs.value.find(item => item.route == route.name)
  if (!target) return '1'
  return target.val
})
const navs = ref([
    { name: '首页', route: 'dashboard', val: '1' },
    { name: '账号管理', route: 'user', val: '2' },
    { name: '模板管理', route: 'template', val: '3' },
    { name: '发送短信', route: 'send', val: '4' },
    { name: '批量发送', route: 'mutiple', val: '5' },
    { name: '发送记录', route: 'history', val: '6' },
    // { name: '回执统计', route: 'back', val: '7' },
])

const goNav = item => {
    router.push({ name: item.route })
}

</script>