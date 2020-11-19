import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: 'show_routers/',
    method: 'post',
    // params: { token }
    token
  })
}

export function logout() {
  return request({
    url: 'logout/',
    method: 'post'
  })
}


export function get_cpq_token() {
  return request({
    url: 'get_cpq_token/',
    method: 'post'
  })
}
