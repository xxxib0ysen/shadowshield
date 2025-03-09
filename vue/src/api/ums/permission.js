import request from '@/utils/request'

// 获取权限列表
export function getPermissionList(keyword, page, page_size) {
  return request({
    url: '/permission/list',
    method: 'get',
    params: { keyword, page, page_size }
  })
}

// 添加权限
export function addPermission(data) {
  return request({
    url: '/permission/add',
    method: 'post',
    data
  })
}

// 更新权限
export function updatePermission(permission_id, data) {
  return request({
    url: `/permission/edit/${permission_id}`,
    method: 'post',
    data
  })
}

// 删除权限
export function deletePermission(permission_id) {
  return request({
    url: `/permission/delete/${permission_id}`,
    method: 'post'
  })
}
