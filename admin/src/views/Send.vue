<template>
    <div class="page-send">
        <Title :title="'发送短信'" />
        <div class="content box">
            <div class="item">
                <div class="title">手机号:</div>
                <el-input v-model="form.phone" type="textarea" :rows="5"  class="input" placeholder="手机号码"></el-input>
                <div class="tip">可以输入多个手机号，用<span>换行</span>或<span>英文逗号</span>隔开</div>
                <div class="tip">最多<span>70个字符</span>（字符包含：汉字、字母、符号）为一条（以下发内容长度为准），超过长度平台将会自动分割为多条（每条都按67个字符分隔）发送，分割后的多条短信将按照具体占用条数计费。</div>
            </div>
            <div class="item">
                <div class="title">模板:</div>
                <el-select class="input" v-model="form.tid" placeholder="选择模板">
                    <el-option
                    v-for="item in templateList"
                    :key="item.id"
                    :label="item.id + '-' + item.content"
                    :value="item.id"
                    />
                </el-select>
                <div class="tip">
                    <span>发送内容：</span>
                    {{ showContent }}
                </div>
            </div>
            <div class="item" v-if="currTemplate.params">
                <div class="title">模板参数:</div>
                <div class="item-list">
                    <div class="list-item" v-for="i in currTemplate.params" :key="i">
                        <span>{{`\{${i}\}`}}:</span>
                        <el-input type="text" v-model="form.params[i-1]"></el-input>
                    </div>
                </div>
            </div>
            <div class="item">
                <div class="title">定时发送:</div>
                <el-switch
                    v-model="form.timeSwitch"
                    inline-prompt
                    active-text="开"
                    inactive-text="关"
                    style="margin-right:20px"
                />
                <el-date-picker
                    class="input"
                    v-if="form.timeSwitch"
                    v-model="form.time"
                    :value-format="'YYYY/MM/DD HH:mm:ss'"
                    type="datetime"
                    placeholder="选择时间"
                />
                <div class="tip">关闭定时发送 或时间小于当前时间 会立即发送短信</div>
            </div>

            <div class="item">
                <el-button class="btn" type="primary" @click="send" :loading="loading">发送</el-button>
            </div>
        </div>
    </div>
</template>

<script setup>
import Title from '../components/Title.vue'
import { ref, computed } from 'vue'
import { _allTemplate, _send } from '../axios'
import { ElMessage } from 'element-plus'
import { assertArrayExpression } from '@babel/types';


const loading = ref(false)
const form = ref({
    phone: '',
    tid: '',
    params: [],
    timeSwitch: false,
    time: ''
})

// 最终内容
const showContent = computed(() => {
    if (currTemplate.value.content) {
        let str = currTemplate.value.content
        for (let i = 1; i <= currTemplate.value.params; i++) {
            str = str.replace(`\{${i}\}`, form.value.params[i] || `\{${i}\}`)
        }
        return str
    }
    return '--'
})

// 模板列表
const templateList = ref([])
const currTemplate = computed(() => {
    return templateList.value.find(item => item.id == form.value.tid) || {}
})
_allTemplate().then(res => {
    if (res.code) return
    templateList.value = JSON.parse(res.data)
})

// 电话转换
const replaceAll = (str, FindText, RepText) => {
    const regExp = new RegExp(FindText, 'g')
    return str.replace(regExp, RepText)
}
const trans = () => {
    try {
        let str = replaceAll(form.value.phone, ' ', '')
        str = replaceAll(str, ',\n', ',')
        str = replaceAll(str, '\n', ',')
        return str
    } catch {
        return form.value.phone
    }
    
}

// 发送
const send = () => {
    // 手机号校验处理
    if (!form.value.phone) return ElMessage.warning('请输入手机号码')
    // 模板校验
    if (!form.value.tid) return ElMessage.warning('请选择短信模板')
    // 模板参数校验
    if (currTemplate.value.params) {
        form.value.params.forEach(item => {
            if (item === '' || item === null || item === undefined) {
                return ElMessage.warning('请完整填写模板参数')
            }
        })
    }
    // 时间校验
    if (form.value.timeSwitch && !form.value.time) return ElMessage.warning('请选择发送时间')
    
    // 分批发送，每批最多200个
    const step = 200
    let arr = []
    try {
        arr = trans().split(',')
    } catch {
        arr = []
        ElMessage.error('号码解析失败')
    }
    if (!arr.length) return
    const allArr = []
    let index = 0
    arr.forEach(item => {
        if (allArr[index]) {
            if (allArr[index].length >= step) {
                index++
                allArr[index] = [ item ]
            } else {
                allArr[index].push(item)
            }
        } else {
            allArr[index] = [ item ]
        }
    })
    allArr.forEach((item, i) => {
        setTimeout(() => {
            const params = {
                mobile: item.join(','),
                tid: form.value.tid,
                datas: form.value.params,
                content: currTemplate.value.content,
            }
            if (form.value.timeSwitch) {
                params.time = Date.parse(form.value.time)
            }
            // 发送请求
            loading.value = true
            _send(params).then(res => {
                if (res.code) return
                if (i == allArr.length - 1) {
                    ElMessage.success('发送完成')
                    form.value = {
                        phone: '',
                        tid: '',
                        params: [],
                        timeSwitch: false,
                        time: ''
                    }
                }
            }).finally(() => {
                loading.value = false
            })
        }, i * 200)
    })
    
}

</script>

<style lang="less" scoped>
.page-send {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 32px 32px 22px 32px;
    background-color: rgba(255,255,255,0.9);
    .content {
        padding: 48px 128px 32px 64px;
        width: 60%;
        min-width: 800px;
        .item {
            display: flex;
            flex-wrap: wrap;
            margin-bottom: 22px;
            .title {
                width: 80px;
                height: 100%;
            }
            .input {
                flex: 1;
            }
            .btn {
                margin-left: 80px;
                flex: 1;
                margin-top: 32px;
                height: 40px;
            }
            .tip {
                width: 100%;
                font-size: 12px;
                color: #999;
                padding-left: 80px;
                margin-top: 8px;
                span {
                    color: red;
                    margin-right: 8px;
                }
            }
            .item-list {
                flex: 1;
                .list-item {
                    display: flex;
                    align-items: center;
                    margin-bottom: 4px;
                    span {
                        margin-right: 6px;
                    }
                }
            }
        }
    }
}
</style>