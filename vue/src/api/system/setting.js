import request from '@/utils/request'

// 获取某个系统设置项
export const getSetting = (key) => {
    return request.get('/system/getSetting', { params: { key } })
  }
  
  // 设置某个系统设置项
  export const setSetting = (key, value) => {
    return request.post('/system/setSetting', { key, value })
  }
  