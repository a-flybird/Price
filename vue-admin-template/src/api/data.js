import request from "@/utils/request";
//基础数据及BOM导出接口
export function search(page_size,page_num,productcode) {
  return request({
    url: 'search/',
    method: 'get',
    params: { page_size,page_num,productcode }
  })
}
export function exportExcel(file) {
  console.log(file)
  return request({
    url: 'exportExcel/',
    method: 'post',
    responseType: 'arraybuffer',
    file
  })
}
export function uploadExcel(file) {
  console.log(file)
  return request({
    url: 'uploadExcel/',
    method: 'post',
    responseType: 'arraybuffer',
    file
  })
}
export function delete_item(data) {
  return request({
    url: 'delete_item/',
    method: 'post',
    data
  })
}
export function create_item(data) {
  return request({
    url: 'create_item/',
    method: 'post',
    data
  })
}
export function update_item(data) {
  return request({
    url: 'update_item/',
    method: 'post',
    data
  })
}
export function price_list(page_size,page_num) {
  return request({
    url: 'price_list/',
    method: 'get',
    params: { page_size, page_num }
  })
}
export function searchall(page_size,page_num,item) {
  return request({
    url: 'searchall/',
    method: 'get',
    params: { page_size,page_num,item }
  })
}
export function download_user(file) {
  return request({
    url: 'download_user/',
    method: 'post',
    responseType: 'arraybuffer',
    file
  })
}
export function bom_list(bomId,token,lang) {
  return request({
    url: 'bom_list/',
    method: 'get',
    responseType: 'arraybuffer',
    params: { bomId,token,lang }
  })
}
//用户信息接口
export function show_user(page_size, page_num) {
  return request({
    url: 'show_user/',
    method: 'get',
    params: { page_size, page_num }
  })
}
export function show_role() {
  return request({
    url: 'show_role/',
    method: 'post',
  })
}
export function register(user) {
  return request({
    url: 'register/',
    method: 'post',
    data: user,
  })
}
export function update_user(user) {
  return request({
    url: 'update_user/',
    method: 'post',
    data: user,
  })
}
//菜单角色信息接口
export function show_menus() {
  return request({
    url: 'show_menus/',
    method: 'post',
  })
}
export function update_role(role) {
  return request({
    url: 'update_role/',
    method: 'post',
    data: role,
  })
}
export function create_role(role) {
  return request({
    url: 'create_role/',
    method: 'post',
    data: role,
  })
}
export function update_pwd(pwd) {
  return request({
    url: 'update_pwd/',
    method: 'post',
    data: pwd,
  })
}
// 备件数据接口
export function price_list_bj(page_size,page_num) {
  return request({
    url: 'price_list_bj/',
    method: 'get',
    params: { page_size, page_num }
  })
}
export function create_item_bj(data) {
  return request({
    url: 'create_item_bj/',
    method: 'post',
    data
  })
}
export function update_item_bj(data) {
  return request({
    url: 'update_item_bj/',
    method: 'post',
    data
  })
}
export function delete_item_bj(data) {
  return request({
    url: 'delete_item_bj/',
    method: 'post',
    data
  })
}
export function download_user_bj(file) {
  console.log(file)
  return request({
    url: 'download_user_bj/',
    method: 'post',
    responseType: 'arraybuffer',
    file
  })
}
export function search_bj(productcode) {
  return request({
    url: 'search_bj/',
    method: 'get',
    params: { productcode }
  })
}
export function exportExcel_bj(file) {
  console.log(file)
  return request({
    url: 'exportExcel_bj/',
    method: 'post',
    responseType: 'arraybuffer',
    file
  })
}
export function uploadExcel_bj(file) {
  console.log(file)
  return request({
    url: 'uploadExcel_bj/',
    method: 'post',
    responseType: 'arraybuffer',
    file
  })
}
