<template>
    <div class="page-template">
        <Title :title="'模板管理'" />
        <div class="content">
            <div class="search box">
                <div class="search-content">
                    <div class="search-item">
                        <span>模板ID</span>
                        <el-input class="input" size="small" clearable type="text" v-model.trim="search.id"></el-input>
                    </div>
                    <div class="search-item">
                        <span>模板内容</span>
                        <el-input class="input" size="small" clearable type="text" v-model.trim="search.content"></el-input>
                    </div>
                    <div class="search-item">
                        <span>参数数量</span>
                        <el-input class="input" size="small" clearable type="text" v-model.trim="search.params"></el-input>
                    </div>
                </div>
                <el-button :loading="loading" type="primary" @click="addRow">新增</el-button>
            </div>
            <div class="box">
                <el-table v-loading="loading" :empty-text="'暂无数据'" :data="showList" stripe style="width: 100%" highlight-current-row fit>
                    <el-table-column :min-width="1" show-overflow-tooltip prop="id" label="模板id"/>
                    <el-table-column :min-width="5" show-overflow-tooltip prop="content" label="模板内容" />
                    <el-table-column :min-width="1" show-overflow-tooltip prop="params" label="参数数量" />
                    <el-table-column :min-width="2" show-overflow-tooltip label="操作">
                        <template #default="scope">
                            <el-button size="small" type="warning" @click="updateRow(scope.row)">修改</el-button>
                            <el-popconfirm :confirm-button-text="'确认'" :cancel-button-text="'取消'" title="确认删除该数据吗?" @confirm="deleteRow(scope.row)">
                                <template #reference>
                                    <el-button size="small" type="danger">删除</el-button>
                                </template>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>

        <!-- 弹窗  -->
        <el-dialog
            v-model="dialogVisible"
            :title="dialogTitle"
            width="500px"
            :close-on-click-modal="false"
        >
            <div class="dialog-content">
                <div class="input-item">
                    <span class="input-title">模板ID:</span>
                    <el-input-number :disabled="dialogType==2" :controls="false" v-model="form.id"  class="input" placeholder="模板ID"></el-input-number>
                </div>
                <div class="input-item">
                    <span class="input-title">模板内容:</span>
                    <el-input v-model="form.content" type="textarea" :rows="5"  class="input" placeholder="模板内容"></el-input>
                    <p class="tips">默认以70个字符（字符包含：汉字、字母、符号）为一条（以下发内容长度为准），超过长度平台将会自动分割为多条（每条都按67个字符分隔）发送，分割后的多条短信将按照具体占用条数计费。</p>
                </div>
                <div class="input-item">
                    <span class="input-title">参数数量:</span>
                    <el-input-number :controls="false" v-model="form.params"  :step="1" :min="0" class="input" placeholder="参数数量: 不填默认为0"></el-input-number>
                </div>
            </div>
            <template #footer>
            <span class="dialog-footer">
                <el-button :loading="loading" @click="dialogVisible = false">取消</el-button>
                <el-button :loading="loading" type="primary" v-if="dialogType == 1" :disabled="!form.id || !form.content" @click="addItem">确认</el-button>
                <el-button :loading="loading" type="primary" v-if="dialogType == 2" :disabled="!form.id || !form.content" @click="updateItem">确认</el-button>
            </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import Title from '../components/Title.vue'
import { _allTemplate, _addTemplate, _updateTemplate, _delTemplate } from '../axios'
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const list = ref([])
const loading = ref(false)
const search = ref({
    id: '',
    content: '',
    params: '',
})

const showList = computed(() => {
    return list.value.filter(item => {
        return item.id.toString().includes(search.value.id) &&
                item.content.toString().includes(search.value.content) &&
                item.params.toString().includes(search.value.params)
    })

})

const getList = () => {
    loading.value = true
    _allTemplate().then(res => {
        if (res.code) return
        list.value = JSON.parse(res.data)
    }).finally(() => {
        loading.value = false
    })
}
getList()

const dialogType = ref(1) // 1-新增  2-修改
const dialogTitle = ref('')
const dialogVisible = ref(false)
const form = ref({
    id: null,
    content: '',
    params: null
})
// 新增弹窗
const addRow = () => {
    form.value = {
        id: null,
        content: '',
        params: null
    }
    dialogTitle.value = '新增'
    dialogType.value = 1
    dialogVisible.value = true
}
// 新增请求
const addItem = () => {
    if (!form.value.params) form.value.params = 0
    loading.value = true
    _addTemplate(form.value).then(res => {
        if (res.code) return
        ElMessage.success('新增成功')
        dialogVisible.value = false
        getList()
    }).finally(() => {
        loading.value = false
    })
}
// 修改弹窗
const updateRow = row => {
    form.value = row
    dialogTitle.value = '修改'
    dialogType.value = 2
    dialogVisible.value = true
}
// 修改请求
const updateItem = () => {
    if (!form.value.params) form.value.params = 0
    loading.value = true
    _updateTemplate(form.value).then(res => {
        if (res.code) return
        ElMessage.success('修改成功')
        dialogVisible.value = false
        getList()
    }).finally(() => {
        loading.value = false
    })
}

// 删除
const deleteRow = row => {
    loading.value = true
    _delTemplate(row).then(res => {
        if (res.code) return
        ElMessage.success('删除成功')
        getList()
    }).finally(() => {
        loading.value = false
    })
}

</script>

<style lang="less" scoped>
.page-template {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 32px 32px 22px 32px;
    background-color: rgba(255,255,255,0.9);
    .content {
        padding-top: 20px;
        .search {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 32px;
            background-color: #fff;
            padding: 20px 20px 0 20px;
            .search-content {
                flex: 1;
                flex-wrap: wrap;
                display: flex;
                justify-content: flex-start;
                align-items: center;
                .search-item {
                    display: flex;
                    align-items: center;
                    margin-right: 32px;
                    word-break: keep-all;
                    margin-bottom: 22px;
                    span {
                        margin-right: 8px;
                    }
                }
            }
        }
    }
}
.dialog-content {
    .input-item {
        margin-bottom: 20px;
        display: flex;
        align-items: flex-start;
        flex-wrap: wrap;
        .input-title {
            width: 80px;
        }
        .input {
            flex: 1;
        }
        .tips {
            width: 100%;
            font-size: 12px;
            color: #999;
        }
    }
}
</style>