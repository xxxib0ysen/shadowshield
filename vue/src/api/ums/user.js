import request from '@/utils/request'

// 获取用户列表
export function getUserList(keyword , page, pageSize ) {
  return request({
    url: '/user/list',
    method: 'get',
    params: { keyword, page, pageSize }
  })
}

// 获取指定用户信息
export function getUserById(user_id) {
  return request({
    url: `/user/${user_id}`,
    method: 'get'
  })
}

// 添加用户
export function addUser(data) {
  return request({
    url: '/user/add',
    method: 'post',
    data
  })
}

// 编辑用户
export function updateUser(user_id, data) {
  return request({
    url: `/user/update/${user_id}`,
    method: 'post',
    data
  })
}

// 删除用户
export function deleteUser(user_id) {
  return request({
    url: `/user/delete/${user_id}`,
    method: 'post'
  })
}

// 启用/禁用用户
export function updateUserStatus(user_id, status) {
  return request({
    url: `/user/updateStatus/${user_id}`,
    method: 'post',
    data: { status }
  })
}

// 分配角色
export function assignUserRole(user_id, role_ids) {
  return request({
    url: '/user/role/update',
    method: 'post',
    data: { user_id: user_id, role_ids: role_ids }
  })
}

// 获取用户角色
export function getUserRole(user_id) {
  return request({
    url: `/user/role/${user_id}`,
    method: 'get'
  })
}
