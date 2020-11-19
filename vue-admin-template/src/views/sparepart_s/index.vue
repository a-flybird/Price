<template>
  <el-container style="margin: auto">
    <el-header>
      <el-col :span="4" :offset="20" style="line-height: 60px">
        <span> {{ username }} </span>
        <el-button size="mini" @click="logout">注 销</el-button>
      </el-col>
    </el-header>
    <el-main>
      <el-row type="flex" justify="center">
        <el-col :span = "12">
          <el-input placeholder="请输入编码或名称或型号" v-model="productcode" :clearable="true" style="width: 600px">
            <el-button slot="append" icon="el-icon-search" type="primary" plain @click="search" @keyup.enter.native="search">搜索</el-button>
          </el-input>
        </el-col>
      </el-row>
      <el-row type="flex" justify="center" style="margin: 15px;">
        <el-col :span="3">
          <el-upload ref="upload" action="http://127.0.0.1:8080/" :headers="headers" :auto-upload="false" :show-file-list="false" :on-change="uploadExcel">
            <el-button slot="trigger" icon="el-icon-upload2" size="small">批量查询</el-button>
          </el-upload>
        </el-col>
        <el-col :span="3">
          <el-button size="small" icon="el-icon-download" @click="exportExcel">下载模板</el-button>
        </el-col>
      </el-row>
      <el-table :data="tableData" style="width: 96%;margin: 15px 2% auto 2%" :border="true" size="small" :header-cell-style="{background:'#F5F7FA'}">
        <el-table-column prop="productcode" width="135px" label="产品编码"></el-table-column>
        <el-table-column prop="description" :show-overflow-tooltip="true" min-width="240px" label="产品描述(中文)"></el-table-column>
        <el-table-column prop="description_en" :show-overflow-tooltip="true" min-width="240px" label="产品描述(英文)"></el-table-column>
        <el-table-column prop="unit" label="单位"></el-table-column>
        <el-table-column min-width="85px" label="USD">
          <template slot-scope="scope">
            <span>&#36;{{ scope.row.USD }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="85px" label="EUR">
          <template slot-scope="scope">
            <span>&#8364;{{ scope.row.EUR }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="85px" label="GBP">
          <template slot-scope="scope">
            <span>&#163;{{ scope.row.GBP }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="CNY" label="CNY">
          <template slot-scope="scope">
            <span>&#165;{{ scope.row.CNY }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="85px" label="CAD">
          <template slot-scope="scope">
            <span>&#163;{{ scope.row.CAD }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="85px" label="AUD">
          <template slot-scope="scope">
            <span>&#165;{{ scope.row.AUD }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>

<script>
  import { search_bj,exportExcel_bj } from '@/api/data';
  import NProgress from 'nprogress';
    export default {
      name: "index",
      data(){
        return{
          _token:'',
          username: this.$store.getters.name,
          productcode:'',
          tableData:[],
          headers:{
            Authorization: 'Bearer '+ this.$store.getters.token,
          },
        }
      },
      methods:{
        async logout() {
          await this.$store.dispatch('user/logout')
          this.$router.push(`/login?redirect=${this.$route.fullPath}`)
        },
        search(){
          NProgress.start();
          search_bj(this.productcode).then((response) =>{
            if (response.data.rows.length > 0){
              this.$message({
                message: '请求成功',
                type:'success',
                showClose:true
              });
            }else{
              this.$message({
                message: '未查询到结果',
                type:'error',
                showClose:true
              });
            }
            this.tableData = response.data.rows;
            NProgress.done()
          })
        },
        exportExcel() {
          exportExcel_bj({file:'123'}).then(function (res) {
            if (1) {
              let blob = new Blob([res.data], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8'});
              let downloadElement = document.createElement('a');
              let href = window.URL.createObjectURL(blob); //创建下载的链接
              downloadElement.href = href;
              downloadElement.download = 'File template.xlsx'; //下载后文件名
              document.body.appendChild(downloadElement);
              downloadElement.click(); //点击下载
              document.body.removeChild(downloadElement); //下载完成移除元素
              window.URL.revokeObjectURL(href); //释放掉blob对象
            }
          });
        },
        uploadExcel(file){
          let formData = new FormData();
          formData.append('file', file.raw);
          this.axios.post('http://192.168.29.73:8081/api/uploadExcel_bj/', formData, {headers:{'Authorization':'Bearer '+this.$store.getters.token}, responseType: 'arraybuffer'} ).then(function (response) {
            if (response.status === 200) {
              let filename = response.headers['content-disposition'].split(';')[1].split('=')[1];
              let blob = new Blob([response.data], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8'});
              let downloadElement = document.createElement('a');
              let href = window.URL.createObjectURL(blob); //创建下载的链接
              downloadElement.href = href;
              downloadElement.download = filename; //下载后文件名
              document.body.appendChild(downloadElement);
              downloadElement.click(); //点击下载
              document.body.removeChild(downloadElement); //下载完成移除元素
              window.URL.revokeObjectURL(href); //释放掉blob对象
            }
          });
        },
      },
    }
</script>

