<template>
    <div class="page-dashboard">
        <Title :title="'首页'" />
        <div class="content">
            <div class="left box">
                <div class="title">
                    <b>数据统计</b>
                </div>

                <div class="block orange">
                    <span>未发送：</span>
                    <div>{{ hisPre }}</div>
                </div>
                <div class="block green">
                    <span>历史成功：</span>
                    <div>{{ hisTotal }}</div>
                </div>
                <div class="block red">
                    <span>历史失败：</span>
                    <div>{{ hisFaild}}</div>
                </div>
                
            </div>
            <div class="right box">
                <div class="item">
                    <b>系统配置</b>
                </div>
                <div class="item">
                    <div class="title">ACCOUNT SID:</div>
                    <input type="text" class="input" v-model.trim="config.accountSid">
                </div>
                <div class="item">
                    <div class="title">AUTH TOKEN:</div>
                    <input type="text" class="input" v-model.trim="config.token">
                </div>
                <div class="item">
                    <div class="title">Rest URL:</div>
                    <input type="text" class="input" v-model.trim="config.restUrl">
                </div>
                <div class="item">
                    <div class="title">AppID:</div>
                    <input type="text" class="input" v-model.trim="config.appid">
                </div>
                <el-button :loading="loading" type="primary" @click="updateRow" :disabled="!config.accountSid||!config.token||!config.restUrl||!config.appid" class="btn">修改</el-button>
            </div>
        </div>
    </div>
</template>

<script setup>
import Title from '../components/Title.vue'
import { _allConfig, _updateConfig, _allHistory } from '../axios'
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)

// 配置
const config = ref({
    rowid: '',
    appid: '',
    accountSid: '',
    token: '',
    restUrl: '',
})
_allConfig().then(res => {
    if (res.code) return
    config.value = JSON.parse(res.data)
})
// 修改配置
const updateRow = () => {
    loading.value = true
    _updateConfig(config.value).then(res => {
        if (res.code) return
        ElMessage.success('操作成功')
    }).finally(() => {
        loading.value = false
    })
}

// 历史记录
const history = ref([])
_allHistory().then(res => {
    if (res.code) return
    history.value = JSON.parse(res.data)
    console.log(history.value)
})
// 历史已发送
const hisTotal = computed(() => {
    return history.value.filter(item => item.status == 1).length || 0
})
// 历史失败
const hisFaild = computed(() => {
    return history.value.filter(item => item.status == 0).length || 0
})
// 未发送
const hisPre = computed(() => {
    return history.value.filter(item => item.status == 9).length || 0
})

</script>

<style lang="less" scoped>
.page-dashboard {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 32px 32px 22px 32px;
    background-color: rgba(255,255,255,0.9);
    .content {
        padding: 32px;
        display: flex;
        .left {
            flex: 1;
            .title {
                margin-bottom: 44px;
            }
            .block {
                width: 90%;
                padding: 26px;
                border-radius: 12px;
                box-shadow: 0px 4px 10px #eee;
                margin-bottom: 24px;
                display: flex;
                text-align: center;
                align-items: center;
                font-size: 18px;
                color: #fff;
                div {
                    flex: 1;
                    font-size: 36px;
                }
            }
            .orange {
                background-color: #e39300;
            }
            .green {
                background: green;
            }
            .red {
                background-color: #8d0000;
            }
        }
        .right {
            flex: 1;
            padding-left: 24px;
            .item {
                display: flex;
                align-items: center;
                margin-bottom: 22px;
                .title {
                    width: 120px;
                    font-size: 14px;
                }
                .input {
                    flex: 1;
                    height: 40px;
                    padding: 0 10px;
                }
            }
            .btn {
                margin-left: 120px;
                height: 40px;
                width: 300px;
            }
        }
    }
}
</style>