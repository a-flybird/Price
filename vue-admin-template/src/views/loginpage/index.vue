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
          <el-input placeholder="请输入编码或名称或型号" v-model="productcode" :clearable="true" style="width: 600px" @keyup.enter.native="pageCurrentChange(1,10)">
            <el-button slot="append" icon="el-icon-search" type="primary" plain @click="pageCurrentChange(1,10)">搜 索</el-button>
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
        <el-table-column prop="productcode" width="135px" label="编码"></el-table-column>
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="model" label="型号"></el-table-column>
        <el-table-column prop="description"  min-width="240px" label="产品描述"></el-table-column>
        <el-table-column prop="product_type" width="80px" label="物料类型"></el-table-column>
        <el-table-column prop="price_source" width="85px" label="价格来源"></el-table-column>
        <el-table-column min-width="85px" label="RRP(USD)">
          <template slot-scope="scope">
            <span>&#36;{{ scope.row.RRP_USD }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="85px" label="RRP(EUR)">
          <template slot-scope="scope">
            <span>&#8364;{{ scope.row.RRP_EUR }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="85px" label="RRP(GBP)">
          <template slot-scope="scope">
            <span>&#163;{{ scope.row.RRP_GBP }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="85px" label="RRP(CNY)">
          <template slot-scope="scope">
            <span>&#165;{{ scope.row.RRP_RMB }}</span>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @current-change="pageCurrentChange"
        @size-change="pageSizeChange"
        :hide-on-single-page="true"
        :background="true"
        :current-page="page_num"
        :page-size="page_size"
        :pager-count="7"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="width: 90%;margin: 10px 5% 10px 5%">
      </el-pagination>
    </el-main>
  </el-container>
</template>

<script>
  import {search, exportExcel, searchall} from '@/api/data';
  import NProgress from 'nprogress';
    export default {
      name: "index",
      data(){
        return{
          _token:'',
          username: this.$store.getters.name,
          productcode:'',
          tableData:[],
          total:1,
          page_num:1,
          page_size:10,
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
          search(this.productcode).then((response) =>{
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
          exportExcel({file:'123'}).then(function (res) {
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
          this.axios.post('http://192.168.29.73:8081/api/uploadExcel/', formData, {headers:{'Authorization':'Bearer '+this.$store.getters.token}, responseType: 'arraybuffer'} ).then(function (response) {
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
        pageCurrentChange(page_num,page_size){
          NProgress.start();
          const vn = this;
          if(page_size){
            this.page_size = page_size;
          }
          if(page_num){
            this.page_num = Number(page_num);
          }
          search(this.page_size,this.page_num,this.productcode).then((response) =>{
            const { data } = response;
            vn.tableData = data.rows;
            vn.total = data.total;
            vn.page_num = data.page_num;
            if(data.rows.length === 0){
              this.$message({
                message: '未查询到结果',
                type:'error',
                showClose:true
              });
            }
            NProgress.done();
          })
        },
        pageSizeChange(page_size){
          this.page_size = page_size;
          this.pageCurrentChange(1,page_size)
        },
      },
    }
</script>

