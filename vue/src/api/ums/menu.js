import request from '@/utils/request'

// 获取菜单列表
export function getMenuList(page, page_size) {
  return request({
    url: '/menu/list',
    method: 'get',
    params: { page, page_size }
  })
}

// 获取所有菜单（树形结构）
export function getMenuTree() {
  return request({
    url: '/menu/treeList',
    method: 'get'
  })
}

// 添加菜单
export function addMenu(data) {
  return request({
    url: '/menu/add',
    method: 'post',
    data
  })
}

// 编辑菜单
export function updateMenu(menu_id, data) {
  return request({
    url: `/menu/edit/${menu_id}`,
    method: 'post',
    data
  })
}

// 删除菜单
export function deleteMenu(menu_id) {
  return request({
    url: `/menu/delete/${menu_id}`,
    method: 'post'
  })
}

// 修改菜单显示状态
export function updateMenuStatus(menu_id, hidden) {
  return request({
    url: `/menu/updateHidden/${menu_id}`,
    method: 'post',
    data: { hidden }
  })
}

// 获取菜单的层级关系
export function getMenuHierarchy(menu_id, page, page_size) {
  return request({
    url: `/menu/hierarchy/${menu_id}`,
    method: 'get',
    params: { page, page_size }
  })
}
