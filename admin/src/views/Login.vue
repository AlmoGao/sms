<!-- 登录 -->
<template>
    <div class="page-login">
        
        <!-- 表单 -->
        <div class="form">
            <div class="title">短信系统</div>
            <el-input class="input" type="text" v-model.trim="form.username" placeholder="账号"></el-input>
            <el-input class="input" type="password" show-password v-model.trim="form.password" placeholder="密码"></el-input>
            <el-button :disabled="!form.username || !form.password" @click="login" class="btn" type="primary" :loading="loading">登录</el-button>
        </div>

    </div>
</template>

<script setup>
import { _login } from '../axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const form = ref({
    username: '',
    password: ''
})

// 登录
const login = () => {
    loading.value = true
    if (!form.value.username || !form.value.password) return
    _login(form.value).then(res => {
        if (res.code) return
        sessionStorage.setItem('token', res.data.token)
        router.replace({name: 'home'})
        ElMessage.success('登录成功')
    }).finally(() => {
        loading.value = false
    })
}
</script>

<style lang="less" scoped>
.page-login {
    width: 100%;
    height: 100%;
    background-color: #efefef;
    background-image: url('../assets/bg.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    .form {
        background-color: #fff;
        width: 40%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translateX(-50%) translateY(-50%);
        max-width: 600px;
        min-width: 400px;
        padding: 32px 44px 66px 44px;
        border-radius: 12px;
        .title {
            text-align: center;
            color: #333;
            font-size: 24px;
            margin-bottom: 44px;
            font-weight: bold;
        }
        .input {
            margin-bottom: 32px;
            height: 42px;
        }
        .btn {
            width: 100%;
            height: 42px;
        }
    }
}
</style>