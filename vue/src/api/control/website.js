import request from '@/utils/request'

// 获取自定义规则列表
export const getCustomRules = () => {
  return request.get('/custom_rule/list')
}

// 修改自定义规则状态
export const updateCustomRuleStatus = (id, status) => {
  return request.post('/custom_rule/updateStatus', { id, status })
}

// 添加自定义规则
export const addCustomRules = (data) => {
  return request.post('/custom_rule/add', data)
}

// 删除单个自定义规则
export const deleteCustomRule = (id) => {
  return request.post('/custom_rule/delete', { id })
}

// 批量删除规则
export const deleteCustomRuleBatch = (ids) => {
  return request.post('/custom_rule/batchDelete', { ids })
}


