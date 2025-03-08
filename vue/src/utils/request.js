import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getToken } from '@/utils/auth'

// 创建 axios 实例
const service = axios.create({
  baseURL: 'http://localhost:5000', 
  timeout: 15000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    if (getToken()) {
      config.headers['Authorization'] = getToken() // 携带 Token
    }
    return config
  },
  error => {
    console.log(error) // 调试用
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 200) {
      ElMessage.error(res.message || '请求错误')

      // 401: 未登录，需要重新登录
      if (res.code === 401) {
        ElMessageBox.confirm('会话已过期，请重新登录', '确定登出', {
          confirmButtonText: '重新登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          localStorage.removeItem('token') // 清除 token
          location.reload() // 重新加载页面
        })
      }
      return Promise.reject('error')
    } else {
      return response.data
    }
  },
  error => {
    console.error('请求失败:', error)
    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

export default service
