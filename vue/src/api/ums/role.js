import request from '@/utils/request'

export function getRoleList(keyword, page, pageSize) {
  return request({
    url: '/role/list',
    method: 'get',
    params: { keyword, page, pageSize }
  })
}

// 添加
export function addRole(data) {
  return request({
    url: '/role/add',
    method: 'post',
    data
  })
}

// 编辑
export function updateRole(role_id, data) {
  return request({
    url: `/role/edit/${role_id}`,
    method: 'post',
    data
  })
}

// 删除
export function deleteRole(role_id) {
  return request({
    url: `/role/delete/${role_id}`,
    method: 'post'
  })
}

// 更新状态
export function updateRoleStatus(role_id, status) {
  return request({
    url: `/role/updateStatus/${role_id}`,
    method: 'post',
    data: { status }
  })
}

// 获取角色菜单
export function getRoleMenu(rolerole_idId) {
  return request({
    url: `/role/listMenu/${role_id}`,
    method: 'get'
  })
}

// 获取角色资源
export function getRoleResource(role_id) {
  return request({
    url: `/role/listResource/${role_id}`,
    method: 'get'
  })
}

// 获取角色权限
export function getRolePermission(role_id) {
  return request({
    url: `/role/listPermission/${role_id}`,
    method: 'get'
  })
}

// 分配角色菜单
export function assignRoleMenu(role_id, menu_ids) {
  return request({
    url: '/role/allocMenu',
    method: 'post',
    data: { role_id: role_id, menu_ids: menu_ids }
  })
}

// 分配角色资源
export function assignRoleResource(role_id, resource_ids) {
  return request({
    url: '/role/allocResource',
    method: 'post',
    data: { role_id: role_id, resource_ids: resource_ids }
  })
}

// 分配角色权限
export function assignRolePermission(role_id, permission_ids) {
  return request({
    url: '/role/allocPermission',
    method: 'post',
    data: { role_id: role_id, permission_ids: permission_ids }
  })
}
