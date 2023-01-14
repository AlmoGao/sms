<template>
    <div class="page-his">
        <Title :title="'发送记录'" />
        <div class="content">
            <div class="search box">
                <div class="search-item">
                    <span>发送人</span>
                    <el-input class="input" size="small" type="text" clearable v-model.trim="search.username"></el-input>
                </div>
                <div class="search-item">
                    <span>发送号码</span>
                    <el-input class="input" size="small" type="text" clearable v-model.trim="search.mobile"></el-input>
                </div>
                <div class="search-item">
                    <span>模板id</span>
                    <el-input class="input" size="small" type="text" clearable v-model.trim="search.tid"></el-input>
                </div>
                <div class="search-item">
                    <span>模板内容</span>
                    <el-input class="input" size="small" type="text" clearable  v-model.trim="search.content"></el-input>
                </div>
                <div class="search-item">
                    <span>发送状态</span>
                    <el-select v-model="search.status" class="input" size="small" clearable >
                        <el-option
                        v-for="(item, key) in statusMap"
                        :key="key"
                        :label="item"
                        :value="key"
                        />
                    </el-select>
                </div>
                <div style="width:100%"></div>
                <div class="search-item">
                    <span>创建时间</span>
                    <el-date-picker
                        size="small"
                        v-model="search.createTime"
                        type="daterange"
                    />
                </div>
                <div class="search-item">
                    <span>发送时间</span>
                    <el-date-picker
                        size="small"
                        v-model="search.sendTime"
                        type="daterange"
                    />
                </div>
            </div>
            <div class="box">
                <div class="table">
                    <el-table v-loading="loading" :empty-text="'暂无数据'" :data="showList" stripe style="width: 100%" highlight-current-row fit>
                        <el-table-column :min-width="1" show-overflow-tooltip prop="username" label="发送人"/>
                        <el-table-column :min-width="2" show-overflow-tooltip prop="_createTime" label="创建时间"/>
                        <el-table-column :min-width="2" show-overflow-tooltip prop="_sendTime" label="发送时间"/>
                        <el-table-column :min-width="2" show-overflow-tooltip prop="mobile" label="发送号码"/>
                        <el-table-column :min-width="1" show-overflow-tooltip prop="tid" label="模板id"/>
                        <el-table-column :min-width="2" show-overflow-tooltip prop="content" label="模板内容"/>
                        <el-table-column :min-width="2" show-overflow-tooltip prop="datas" label="模板参数"/>
                        <el-table-column :min-width="2" show-overflow-tooltip prop="result" label="发送回执"/>
                        <el-table-column :min-width="2" show-overflow-tooltip prop="_status" label="发送状态">
                            <template #default="scope">
                                <b :style="{'color':scope.row._statusColor}">{{ scope.row._status }}</b>
                            </template>
                        </el-table-column>
                        <el-table-column :min-width="1" show-overflow-tooltip label="操作">
                            <template #default="scope">
                                <el-popconfirm v-if="scope.row.status==9" :confirm-button-text="'确认'" :cancel-button-text="'取消'" title="确认取消发送该信息吗?" @confirm="deleteRow(scope.row)">
                                    <template #reference>
                                        <el-button :loading="loading" size="small" type="danger">撤销</el-button>
                                    </template>
                                </el-popconfirm>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-pagination
                        style="margin:23px auto 0 auto"
                        v-model:current-page="page.currPage"
                        v-model:page-size="page.pageSize"
                        :page-sizes="[10, 20, 50, 100]"
                        layout="total, sizes, prev, pager, next, jumper"
                        :total="page.total"
                        @size-change="() => page.currPage = 1"
                        />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Title from '../components/Title.vue'
import { _allHistory, _deletePresend } from '../axios'
import { ref, computed } from 'vue'
import moment from 'moment'
import { ElMessage } from 'element-plus'


const search = ref({
    username: '',
    mobile: '',
    tid: '',
    content: '',
    status: '',
    createTime: [],
    sendTime: [],
})

const statusMap = {
    0: '失败',
    1: '成功',
    9: '未发送',
}
const statusColorMap = {
    0: 'red',
    1: 'green',
    9: 'orange'
}

const loading = ref(false)
const list = ref([])
const getList = () => {
    loading.value = true
    _allHistory().then(res => {
        if (res.code) return
        list.value = (JSON.parse(res.data) || []).map(item => {
            item._createTime = moment(item.createTime * 1).format('YYYY/MM/DD HH:mm:SS')
            item._sendTime = '--'
            if (item.sendTime) {
                item._sendTime = moment(item.sendTime * 1).format('YYYY/MM/DD HH:mm:SS')
            }
            item._status = statusMap[item.status]
            item._statusColor = statusColorMap[item.status]
            return item
        }).sort((a, b) => {
            return b.createTime - a.createTime
        })
        page.value.total = list.value.length
    }).finally(() => {
        loading.value = false
    })
}
getList()

const page = ref({
    currPage: 1,
    pageSize: 10,
    total: 0
})

const showList = computed(() => {
    let arr = list.value.filter(item => {
        return (
            item.username.toString().includes(search.value.username) &&
            item.mobile.toString().includes(search.value.mobile) &&
            item.tid.toString().includes(search.value.tid) &&
            item.content.toString().includes(search.value.content) &&
            item.status.toString().includes(search.value.status) 
        )
    })
    console.log(search.value.createTime)
    if (search.value.createTime && search.value.createTime.length) {
        const start = Date.parse(new Date(search.value.createTime[0]))
        const end = Date.parse(new Date(search.value.createTime[1])) + (24 * 60 * 60 - 1) * 1000
        arr = arr.filter(item => {
            return item.createTime <= end && item.createTime >= start
        })
    }
    if (search.value.sendTime && search.value.sendTime.length) {
        const start = Date.parse(new Date(search.value.sendTime[0]))
        const end = Date.parse(new Date(search.value.sendTime[1])) + (24 * 60 * 60 - 1) * 1000
        arr = arr.filter(item => {
            return item.sendTime <= end && item.sendTime >= start
        })
    }
    page.value.total = arr.length
    return arr.slice(
        page.value.pageSize * (page.value.currPage - 1),
        page.value.pageSize * page.value.currPage
        )
})


// 删除
const deleteRow = row => {
    loading.value = true
    _deletePresend({
        rowid: row.rowid
    }).then(res => {
        if (res.code) return
        ElMessage.success('操作成功')
        getList()
    }).finally(() => {
        loading.value = false
    })
}


</script>

<style lang="less" scoped>
.page-his {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 32px 32px 22px 32px;
    background-color: rgba(255,255,255,0.9);
    .search {
            display: flex;
            margin-bottom: 32px;
            background-color: #fff;
            padding: 20px 20px 0 20px;
            flex-wrap: wrap;
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
</style>