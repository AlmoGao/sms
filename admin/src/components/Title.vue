<template>
    <el-tabs v-model="activeName">
        <el-tab-pane :label="props.title" name="first"></el-tab-pane>
    </el-tabs>
</template>

<script setup>
import { ref, defineProps } from 'vue'

const props = defineProps({
    title: {
        type: String,
        default: ''
    }
})
const activeName = ref('first')
</script>