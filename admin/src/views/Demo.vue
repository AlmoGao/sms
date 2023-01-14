<template>
    <div class="page-dashboard">
        <Title :title="'首页'" />
        <div class="content">
            内容
        </div>
    </div>
</template>

<script setup>
import Title from '../components/Title.vue'

</script>

<style lang="less" scoped>
.page-dashboard {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 32px 32px 22px 32px;
    background-color: rgba(255,255,255,0.9);
}
</style>