<template>
    <div class="page-mutiple">
        <Title :title="'批量发送'" />
        <div class="content box">
            <div class="item">
                <div class="title">模板:</div>
                <el-select class="input"  v-model="form.tid" placeholder="选择模板">
                    <el-option
                    v-for="item in templateList"
                    :key="item.id"
                    :label="item.id + '-' + item.content"
                    :value="item.id"
                    />
                </el-select>
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
                <div class="title">文件:</div>
                <input type="file" @change="fileChange">
                <div class="tip">
                    请按照以下格式上传excel表格
                </div>
                <div class="tip">
                    <span>第一列(A列)为手机号，第二列(B列)是第一个参数，第三列(C列)是第二个参数，以此类推... 下图为示例：</span>
                    <img src="../assets/demo.png" style="width:100%" alt="">
                </div>
            </div>
            <div class="item">
                <div class="title">发送预览：</div>
                <div class="pre">
                    <div class="tr" v-for="(item, i) in preList" :key="i">
                        <span>{{ i+1 }}</span>
                        <span>{{ item.mobile }}</span>
                        <span style="flex:1">{{ item.content }}</span>
                    </div>
                </div>
            </div>
            <div class="item">
                <el-button class="btn" type="primary" @click="send" :loading="loading">发送</el-button>
            </div>
            
        </div>
    </div>
</template>

<script setup>
import Title from '../components/Title.vue'
import { read } from 'xlsx'
import { ElMessage } from 'element-plus'
import { ref, computed } from 'vue'
import { _allTemplate, _mutipleSend } from '../axios'



// 解析excel数据
const list = ref([])
const fileChange = async (e) => {
    try {
        const file = e.target.files[0]
        const data = await file.arrayBuffer()
        const workbook = read(data)
        const sheet = workbook.Sheets.Sheet1
        // A-电话 后边依次是参数 B-参数1  C-参数2  D-参数3 ...
        const rows = [ 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I' ]
        let index = 1
        list.value = []
        while (sheet[`A${index}`]) {
            const obj = {
                mobile: sheet[`A${index}`].v,
                datas: []
            }
            for (let i = 0; i < 8; i++) {
                if (sheet[`${rows[i]}${index}`]) {
                    obj.datas.push(sheet[`${rows[i]}${index}`].v)
                } else {
                    break
                }
            }
            list.value.push(obj)
            index++
        }
        console.log('---最终：', list.value)
    } catch {
        ElMessage.warning('数据解析错误，请检查表格文件')
    }
    
}
// 预览列表
const preList = computed(() => {
    if (currTemplate.value.content && list.value.length) {
        const arr = list.value.map(item => {
            let preText = currTemplate.value.content
            for (let i = 1; i <= currTemplate.value.params; i++) {
                preText = preText.replace(`\{${i}\}`, item.datas[i-1] || `\{${i}\}`)
            }
            const obj = {
                mobile: item.mobile,
                datas: currTemplate.value.params ? item.datas : [],
                tid: form.value.tid,
                content: preText
            }
            return obj
        })
        return arr
    } else {
        return []
    }
})

const loading = ref(false)
const form = ref({
    tid: '',
    timeSwitch: false,
    time: ''
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



// 发送
const send = () => {
    console.log('---发送', form.value)
    // 模板校验
    if (!form.value.tid) return ElMessage.warning('请选择短信模板')
    // 时间校验
    if (form.value.timeSwitch && !form.value.time) return ElMessage.warning('请选择发送时间')
    // 文件校验
    if (!list.value.length) return ElMessage.warning('请上传xlsx文件')

    const params = {
        list: preList.value
    }
    if (form.value.timeSwitch) {
        params.time = Date.parse(form.value.time)
    }
    // 发送请求
    loading.value = true
    _mutipleSend(params).then(res => {
        if (res.code) return
        ElMessage.success(res.data)
        form.value = {
            tid: '',
            timeSwitch: false,
            time: ''
        }
        list.value = []
    }).finally(() => {
        loading.value = false
    })
}
</script>

<style lang="less" scoped>
.page-mutiple {
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
            .pre {
                padding: 22px 22px 22px 22px;
                margin-top: 8px;
                width: 100%;
                background-color: #eee;
                max-width: 500px;
                overflow-y: auto;
                font-size: 12px;
                .tr {
                    width: 100%;
                    display: flex;
                    align-items: center;
                    margin-bottom: 8px;
                    span {
                        margin-right: 12px;
                    }
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