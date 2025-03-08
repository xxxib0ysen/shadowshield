import request from '../../utils/request'

export function login(username, password) {
  return request({
    url: '/userLogin/login',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

export function getInfo() {
  return request({
    url: '/userLogin/info',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/userLogin/logout',
    method: 'post'
  })
}
