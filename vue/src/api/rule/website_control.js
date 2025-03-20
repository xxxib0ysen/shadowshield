import axios from "@/utils/request";

// 获取所有网站类型
export function getWebsiteType() {
    return axios.get("/website_control/type");
}

// 添加网站类型
export function addWebsiteType(type_name) {
    return axios.post("/website_control/type/add", { type_name });
}

// 删除网站类型
export function deleteWebsiteType(type_id) {
    return axios.post("/website_control/type/delete", { type_id });
}

// 获取网站规则
export function getWebsiteRule() {
    return axios.get("/website_control/list");
}

// 添加网站规则
export function addWebsiteRule(data) {
    return axios.post("/website_control/add", data);
}

// 删除网站规则
export function deleteWebsiteRule(website_id) {
    return axios.post("/website_control/delete", { website_id });
}

// 启用/禁用规则
export function updateWebsiteStatus(website_id, status) {
    return axios.post("/website_control/updateStatus", { website_id, status });
}
