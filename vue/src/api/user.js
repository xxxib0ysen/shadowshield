import axios from 'axios'

const base = "http://127.0.0.1:5000/api/users"

// 获取用户列表
export const get_user_list = (params) => {
    return axios.get(base, {params});
};

//创建用户
export const create_user = (data) => {
    return axios.post(base, data);
};

//编辑用户
export const update_user = (user_id, data) => {
    return axios.put(`${base}/${user_id}`, data);
};

//删除用户
export const delete_user = (user_id) => {
    return axios.delete(`${base}/${user_id}`);
  };

//启用/禁用
export const toggle_user_status = (user_id, status) => {
    return axios.put(`${base}/${user_id}/status`, { status });
  };

//分配角色
export const assign_user_role = (user_id, role_ids) => {
    return axios.put(`${base}/${user_id}/roles`, { role_ids });
  };