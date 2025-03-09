import request from '@/utils/request'

// 获取资源列表
export function getResourceList(name, uri, category_id, page, pageSize) {
  return request({
    url: '/resource/list',
    method: 'get',
    params: { name, uri, category_id, page, pageSize }
  })
}

// 获取资源分类
export function getResourceCategories() {
  return request({
    url: '/resource/category/list',
    method: 'get'
  })
}

// 添加资源
export function addResource(data) {
  return request({
    url: '/resource/add',
    method: 'post',
    data
  })
}

// 修改资源
export function updateResource(resource_id, data) {
  return request({
    url: `/resource/update/${resource_id}`,
    method: 'post',
    data
  })
}

// 删除资源
export function deleteResource(resource_id) {
  return request({
    url: `/resource/delete/${resource_id}`,
    method: 'post'
  })
}
