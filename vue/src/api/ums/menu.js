import request from '@/utils/request'

// 获取菜单列表
export function getMenuList(page, page_size, level,window_key) {
  return request({
    url: '/menu/list',
    method: 'get',
    params: { page, page_size , level,window_key}
  })
}

// 获取所有菜单（树形结构）
export function getMenuTree(window_key) {
  return request({
    url: '/menu/treeList',
    method: 'get',
    params: {window_key}
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
