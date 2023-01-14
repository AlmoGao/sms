<template>
    <div class="page-user">
        <Title :title="'密码管理'" />
        <div class="content box">
            <el-input class="input" type="password" show-password v-model.trim="form.password" placeholder="原密码"></el-input>
            <el-input class="input" type="password" show-password v-model.trim="form.newPass" placeholder="新密码"></el-input>
            <el-input class="input" type="password" show-password v-model.trim="form.surePass" placeholder="再次输入密码"></el-input>
            <el-button :disabled="!form.password || !form.newPass || !form.surePass" @click="change" class="btn" type="primary" :loading="loading">确认修改</el-button>
        </div>
    </div>
</template>

<script setup>
import Title from '../components/Title.vue'
import { ref } from 'vue'
import { _changPass } from '../axios'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const form = ref({
    password: '',
    newPass: '',
    surePass: '',
})

const change = () => {
    if (form.value.newPass != form.value.surePass) return ElMessage.error('两次新密码不一致')
    loading.value = true
    _changPass(form.value).then(res => {
        if (res.code) return
        console.log(res)
        ElMessage.success('修改成功')
        form.value = {
            password: '',
            newPass: '',
            surePass: '',
        }
    }).finally(() => {
        loading.value = false
    })
}
</script>

<style lang="less" scoped>
.page-user {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 32px 32px 22px 32px;
    background-color: rgba(255,255,255,0.9);
    .content {
        padding: 40px;
        display: inline-flex;
        flex-direction: column;
        align-items: flex-start;
        .input {
            width: 400px;
            height: 40px;
            margin-bottom: 20px;
        }
        .btn {
            width: 400px;
            height: 40px;
        }
    }
}
</style>