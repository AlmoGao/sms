import axios from 'axios'
import { ElMessage } from 'element-plus'
import Router from './router/index'

// axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.baseURL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000'
axios.defaults.headers.post['Content-Type'] = 'application/json'


// 添加响应拦截器
axios.interceptors.response.use(function (response) {
    if (response.data.code) {
        switch (response.data.code) {
            case 401: // 登录过期
                Router.replace({name: 'login'})
                break
        }
        setTimeout(() => {
            ElMessage.error(response.data.data)
        }, 100)
        return Promise.resolve({
            code: 1,
            data: response.data
        })
    }
    return response
}, function (error) {
    ElMessage.error('网络异常')
    return Promise.resolve({
        data: {
            code: 1,
            data: '网络异常'
        }
    })
})
const req = (url, datas) => {
    return new Promise(resolve => {
        axios.post(url, datas).then(res => {
            resolve(res.data)
        })
    })
}


// 登录
export const _login = (params) => {
    return req('/login', params)
}
// 修改密码
export const _changPass = (params) => {
    return req('/changPass', params)
}
// 查询所有模板
export const _allTemplate = (params) => {
    return req('allTemplate', params)
}
// 新增模板
export const _addTemplate = (params) => {
    return req('addTemplate', params)
}
// 修改模板
export const _updateTemplate = (params) => {
    return req('updateTemplate', params)
}
// 删除模板
export const _delTemplate = (params) => {
    return req('delTemplate', params)
}


// 发送记录
export const _allHistory = (params) => {
    return req('allHistory', params)
}
// 发送短信
export const _send = (params) => {
    return req('send', params)
}
// 批量发送 
export const _mutipleSend = (params) => {
    return req('mutipleSend', params)
}
// 撤销预发送
export const _deletePresend = (params) => {
    return req('deletePresend', params)
}

// 全局配置
export const _allConfig = (params) => {
    return req('allConfig', params)
}
//更新配置
export const _updateConfig = (params) => {
    return req('updateConfig', params)
}