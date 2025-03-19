import request from '@/utils/request'


// 获取广告规则源列表
export function getAdblockList(params) {
    return request({
        url: '/adblock/list',
        method: 'get',
        params
    })
}

// 添加
export function addAdblockSource(data) {
    return request({
        url: '/adblock/add',
        method: 'post',
        data
    })
}

// 删除
export function deleteAdblockSource(data) {
    return request({
        url: '/adblock/delete',
        method: 'post',
        data
    })
}

// 启用/禁用
export function updateAdblockStatus(data) {
    return request({
        url: '/adblock/status',
        method: 'post',
        data
    })
}
