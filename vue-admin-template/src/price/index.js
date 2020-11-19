import { search,exportExcel,uploadExcel,delete_item,create_item } from '@/api/data'

const action={
  //搜索编码、名称、型号
  search({ commit }, productcode) {
    return new Promise((resolve, reject) => {
      search(productcode).then(response => {
        resolve(response);
      }).catch(error => {
        reject(error);
      })
    })
  },
  exportExcel({ commit }, file) {
    return new Promise((resolve, reject) => {
      exportExcel(file).then(response => {
        resolve(response);
      }).catch(error => {
        reject(error);
      })
    })
  },
  uploadExcel({ commit }, file) {
    return new Promise((resolve, reject) => {
      uploadExcel(file).then(response => {
        resolve(response);
      }).catch(error => {
        reject(error);
      })
    })
  },
  delete_item({ commit }, data) {
    return new Promise((resolve, reject) => {
      delete_item(data).then(response => {
        resolve(response);
      }).catch(error => {
        reject(error);
      })
    })
  },
  create_item({ commit }, data) {
    return new Promise((resolve, reject) => {
      create_item(data).then(response => {
        resolve(response);
      }).catch(error => {
        reject(error);
      })
    })
  },
}

export default {
  namespace: true,
  action
}
