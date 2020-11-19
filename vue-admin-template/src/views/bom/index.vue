<template>
  <el-container style="margin: auto">
    <el-main>
      <el-form :inline="true" :model="form_item" style="width: 90%;margin: auto 5% auto 5%">
        <el-form-item label="物料编码:">
          <el-input v-model="form_item.itemCode" :clearable="true" size="small"></el-input>
        </el-form-item>
        <el-form-item label="物料名称:">
          <el-input v-model="form_item.itemName" :clearable="true" size="small"></el-input>
        </el-form-item>
        <el-form-item label="物料描述:">
          <el-input v-model="form_item.itemDescription" :clearable="true" size="small"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button icon="el-icon-search" type="primary" size="small" plain @click="pageCurrentChange(form_item)">搜索</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="tableData" size="small" style="width: 90%;margin: 15px 5% auto 5%" :border="true" :header-cell-style="{background:'#F5F7FA'}">
        <el-table-column prop="itemCode" label="物料编码"></el-table-column>
        <el-table-column prop="itemName" label="物料名称"></el-table-column>
        <el-table-column prop="itemDescription" label="物料描述"></el-table-column>
        <el-table-column min-width="85px" label="操作">
          <template slot-scope="scope">
            <el-button size="mini" icon="el-icon-search" @click="get_bom_details(scope.row.bomId)">查询</el-button>
            <el-button size="mini" icon="el-icon-download" @click="exportExcel(scope.row.bomId, lang='zh_CN')">导出</el-button>
            <el-button size="mini" icon="el-icon-download" @click="exportExcel(scope.row.bomId, lang='en_US')">Export</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @current-change="pageCurrentChange"
        @size-change="pageSizeChange"
        :background="true"
        :current-page="page_num"
        :page-size="page_size"
        :pager-count="7"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="width: 90%;margin: 10px 5% 10px 5%">
      </el-pagination>
      <el-dialog title="查看BOM" :visible.sync="bomVisible" :close-on-click-modal="false">
        <el-input placeholder="请输入关键字进行过滤" v-model="filterText" size="small" style="margin-bottom: 10px;"></el-input>
        <el-tree :data="bom_data" :props="defaultProps" :filter-node-method="filterNode" ref="tree"></el-tree>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script charset="utf-8">
  import { bom_list } from '@/api/data';
  import { get_cpq_token } from '@/api/user';
  import NProgress from 'nprogress';
export default {
  name: "index",
  data(){
    return{
      form_item:{
        itemCode:null,
        itemName:null,
        itemDescription:null,
      },
      tableData:[],
      lang:'zh_CN',
      Authorization:'',
      total:1,
      page_num:1,
      page_size:10,
      bomVisible:false,
      bom_data:[],
      defaultProps:{
        children:'childBomList',
        label: data => `${data.itemCode} ${' || '} ${data.itemName} ${' || '} ${data.itemDescription}`,
      },
      filterText:'',
    }
  },
  watch:{
    filterText(val){
      this.$refs.tree.filter(val);
    }
  },
  methods:{
    get_bom_details(bomId){
      const vm = this;
      this.bomVisible = true;
      this.axios.get('https://xxxxxxxxxxxxxx.com/hvpc-mdata/v1/11/3/hvpc/mdm/bom/path/tree-bom-val',
        {params:{ bomId:bomId }, headers: { Authorization:vm.Authorization }}).then((res)=>{
          vm.bom_data = res.data;
      })
    },
    filterNode(value,data){
      if(!value) return true;
      return data.itemDescription.indexOf(value) !== -1 || data.itemCode.indexOf(value) !== -1 || data.itemName.indexOf(value) !== -1;
    },
    get_cpq_token(){
      get_cpq_token().then((res) => {
        this.Authorization = 'bearer ' + res.data.access_token;
        this.pageCurrentChange(1,10,this.form_item);
      });
    },
    pageCurrentChange(page_num,page_size,form_item){
      NProgress.start();
      const vn = this;
      if(page_size){
        this.page_size = page_size;
      }
      if(page_num){
        this.page_num = Number(page_num)-1;
      }
      if(form_item){
        this.form_item = form_item;
      }
      this.axios.get('https://xxxxxxxxxxxxxx.com/hvpc-mdata/v1/11/3/hvpc/mdm/bom/info/root',
        {
          params:{
            itemCode:this.form_item.itemCode,
            itemName:this.form_item.itemName,
            itemDescription:this.form_item.itemDescription,
            page:this.page_num,
            size:this.page_size,
          },
          headers:{
            Authorization: this.Authorization
          }
        }).then((response) =>{
        let rows = response.data.content;
        let number = response.data.number;
        let totalElements = response.data.totalElements;
        let size = response.data.size;
        if(response.status === 200){
          vn.tableData = rows;
          vn.total = totalElements;
          vn.page_num = number+1;
          vn.page_size = size;
        } else {
          vn.$message({
            message: rows,
            type:'error',
            showClose:true
          })
        }
        NProgress.done();
      })
    },
    pageSizeChange(page_num){
      this.page_num = page_num;
      this.pageCurrentChange(1,this.page_num,this.form_item)
    },
    search(){
      console.log('123');
    },
    exportExcel(bomId,lang){
      NProgress.start();
      console.log(this.Authorization)
      bom_list(bomId,this.Authorization, lang).then((res) =>{
        let filename = res.headers['content-disposition'].split(';')[1].split('=')[1];
        let blob = new Blob([res.data], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8'});
        let downloadElement = document.createElement('a');
        let href = window.URL.createObjectURL(blob); //创建下载的链接
        downloadElement.href = href;
        downloadElement.download = decodeURI(filename); //下载后文件名
        document.body.appendChild(downloadElement);
        downloadElement.click(); //点击下载
        document.body.removeChild(downloadElement); //下载完成移除元素
        window.URL.revokeObjectURL(href); //释放掉blob对象
        NProgress.done();
      })
    },
  },
  mounted() {
    this.get_cpq_token();
    // this.pageCurrentChange(1,10,this.form_item);
  }
}
</script>
<style>
  .el-tree-node__content{
    margin-bottom: 10px;
  }
</style>

