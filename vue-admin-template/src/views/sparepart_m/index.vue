<template>
	<el-container style="margin: auto">
    <el-main>
      <el-row type="flex" justify="center">
        <el-col :span = "9" :offset="3">
          <el-input placeholder="请输入内容" v-model="code" :clearable="true" size="small">
            <el-button slot="append" icon="el-icon-refresh-left" size="mini" plain @click="pageCurrentChange(1,10)">重置</el-button>
            <el-button slot="append" icon="el-icon-search" size="mini" style="margin-left: 20px" plain @click="search" @keyup.enter.native="search">搜索</el-button>
          </el-input>
        </el-col>
        <el-col :span = "2" :offset="6">
          <el-button icon="el-icon-edit" plain size="mini" @click="handleCreate">新 建</el-button>
        </el-col>
        <el-col :span = "2">
          <el-upload action="http://192.168.29.73:8081/api/upsert_user_bj/" :headers="headers" :show-file-list="false" :on-success="uploadSuccess">
            <el-button icon="el-icon-upload2" plain size="mini">导入/更新</el-button>
          </el-upload>
        </el-col>
        <el-col :span = "2">
          <el-button icon="el-icon-download" plain size="mini" @click="downloadExcel">导 出</el-button>
        </el-col>
      </el-row>
      <el-table :data="tableData" size="mini" style="width: 98%;margin: 15px 1% auto 1%" border :header-cell-style="{background:'#F5F7FA'}">
        <el-table-column prop="productcode" width="120px" label="产品编码"></el-table-column>
        <el-table-column prop="description" :show-overflow-tooltip="true" min-width="240px" label="产品描述(中文)"></el-table-column>
        <el-table-column prop="description_en" :show-overflow-tooltip="true" min-width="240px" label="产品描述(英文)"></el-table-column>
        <el-table-column prop="unit" width="50px" label="单位"></el-table-column>
        <el-table-column min-width="70px" label="USD">
          <template slot-scope="scope">
            <span>&#36;{{ scope.row.USD }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="70px" label="EUR">
          <template slot-scope="scope">
            <span>&#8364;{{ scope.row.EUR }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="70px" label="GBP">
          <template slot-scope="scope">
            <span>&#163;{{ scope.row.GBP }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="70px" label="CNY">
          <template slot-scope="scope">
            <span>&#165;{{ scope.row.CNY }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="70px" label="CAD">
          <template slot-scope="scope">
            <span>&#36;{{ scope.row.CAD }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="70px" label="AUD">
          <template slot-scope="scope">
            <span>&#8371;{{ scope.row.AUD }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="createddate" :show-overflow-tooltip="true" label="创建时间"></el-table-column>
        <el-table-column prop="lastmodifieddate" :show-overflow-tooltip="true" label="修改时间"></el-table-column>
        <el-table-column min-width="170px" label="操作">
          <template slot-scope="scope">
            <el-button size="mini" icon="el-icon-edit" @click="handleUpdate(scope.row)">编辑</el-button>
            <el-popover placement="top-start" v-model="visibles[`visible_${scope.row.id}`]" width="160" trigger="click">
              <p>确定要删除吗？</p>
              <div>
                <el-button size="mini" @click="visibles[`visible_${scope.row.id}`] = false">取消</el-button>
                <el-button type="danger" size="mini" @click="handledelete(scope.row, visibles[`visible_${scope.row.id}`] = !visibles[`visible_${scope.row.id}`])">删除</el-button>
              </div>
              <el-button slot="reference" size="mini" icon="el-icon-delete" type="danger" plain  style="float: right">删除</el-button>
            </el-popover>
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
      <el-dialog title="编辑" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
        <el-form :model="tempForm" ref="dataForm" :rules="rules" label-position="left" label-width="120px" style="margin: auto 20px auto 20px;" size="mini">
          <el-form-item prop="productcode" label="产品编码">
            <el-input v-model="tempForm.productcode" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="description" label="产品描述(中文)">
            <el-input v-model="tempForm.description" type="textarea"></el-input>
          </el-form-item>
          <el-form-item prop="description_en" label="产品描述(英文)">
            <el-input v-model="tempForm.description_en" type="textarea"></el-input>
          </el-form-item>
          <el-form-item prop="unit" label="单位">
            <el-input v-model="tempForm.unit" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="USD" label="USD">
            <el-input v-model="tempForm.USD" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="EUR" label="EUR">
            <el-input v-model="tempForm.EUR" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="GBP" label="GBP">
            <el-input v-model="tempForm.GBP" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="CNY" label="CNY">
            <el-input v-model="tempForm.CNY" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="CAD" label="CAD">
            <el-input v-model="tempForm.CAD" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="AUD" label="AUD">
            <el-input v-model="tempForm.AUD" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="createddate" label="创建时间">
            <el-input v-model="tempForm.createddate" :disabled="true" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="lastmodifieddate" label="修改时间">
            <el-input v-model="tempForm.lastmodifieddate" :disabled="true" style="width: 250px"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button size="small" @click="cancel">取 消</el-button>
          <el-button type="primary" size="small" @click="dialogStatus==='create'?createData():updateData()">保 存</el-button>
        </div>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script>
  import { delete_item_bj,create_item_bj,update_item_bj,price_list_bj,searchall,download_user_bj } from '@/api/data';
  import NProgress from 'nprogress';
export default {
  name: "basedata",
  data(){
      return{
        username:'',
        code:'',
        headers:{
            Authorization: 'Bearer '+ this.$store.getters.token,
        },
        tableData:[],
        total:1,
        page_num:1,
        page_size:10,
        dialogFormVisible:false,
        dialogStatus:'',
        visibles: {},
        options:[
          {
            value:'Pricing',
            label:'定价',
          },
          {
            value:'Quotation',
            label:'报价',
          }
        ],
        tempForm: {
          productcode:'',
          description:'',
          description_en:'',
          unit:'',
          USD:'',
          EUR:'',
          GBP:'',
          CNY:'',
          CAD:'',
          AUD:'',
          createddate:'',
          lastmodifieddate:'',
        },
        rules:{
          description: [{ required: true, message: '请输入产品描述', trigger: 'blur'}],
          product_type: [{ required: true, message: '请输入物料类型', trigger: 'blur'}],
          price_source: [{ required: true, message: '请选择价格来源', trigger: 'blur'}],
        },
      }
  },
  methods:{
    cancel(){
      this.dialogFormVisible = false;
    },
    handleCreate() {
      this.tempForm = {};
      this.dialogStatus = 'create';
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row){
      this.tempForm = Object.assign({},row);
      this.dialogStatus = 'update';
      this.dialogFormVisible = true;
    },
    handledelete(row,visible){
      console.log(row,visible)
      let data = new FormData();
      data.append('id',row.id);
      delete_item_bj(data).then((response)=> {
        this.pageCurrentChange(this.page_num, this.page_size);
      })
    },
    createData(){
      const vv = this;
      let data = new FormData();
      data.append('productcode',this.tempForm['productcode'] || '');
      data.append('description',this.tempForm['description'] || '');
      data.append('description_en',this.tempForm['description_en'] || '');
      data.append('unit',this.tempForm['unit'] || '');
      data.append('USD',this.tempForm['USD'] || '');
      data.append('EUR',this.tempForm['EUR'] || '');
      data.append('GBP',this.tempForm['GBP'] || '');
      data.append('CNY',this.tempForm['CNY'] || '');
      data.append('CAD',this.tempForm['CAD'] || '');
      data.append('AUD',this.tempForm['AUD'] || '');
      this.$refs['dataForm'].validate((valid)=>{
        if(valid){
          create_item_bj(data).then((response)=>{
            this.pageCurrentChange(this.page_num,this.page_size);
            this.dialogFormVisible = false;
          })
        }else{
          vv.$message({
            message: '保存失败！',
            type:'error',
            showClose:true
          });
          return false
        }
      })
    },
    updateData(){
      const vm = this;
      let data = new FormData();
      data.append('productcode',this.tempForm['productcode'] || '');
      data.append('description',this.tempForm['description'] || '');
      data.append('description_en',this.tempForm['description_en'] || '');
      data.append('unit',this.tempForm['unit'] || '');
      data.append('USD',this.tempForm['USD'] || '');
      data.append('EUR',this.tempForm['EUR'] || '');
      data.append('GBP',this.tempForm['GBP'] || '');
      data.append('CNY',this.tempForm['CNY'] || '');
      data.append('CAD',this.tempForm['CAD'] || '');
      data.append('AUD',this.tempForm['AUD'] || '');
      this.$refs['dataForm'].validate((valid)=>{
        if(valid){
          update_item_bj(data).then((response)=>{
            this.pageCurrentChange(this.page_num,this.page_size);
            this.dialogFormVisible = false;
          })
        }else{
          vm.$message({
            message: '保存失败！',
            type:'error',
            showClose:true
          });
          return false
        }
      })
    },
    pageCurrentChange(page_num,page_size){
      const vn = this;
      if(page_size){
        this.page_size = page_size;
      }
      if(page_num){
        this.page_num = Number(page_num);
      }
      price_list_bj(page_size,this.page_num).then((response) =>{
        const { data } = response;
        vn.tableData = data.rows;
        vn.total = data.total;
        vn.page_num = data.page_num;
        // rows.forEach(one => {
        //   this.visibles[`visibles_${one.id}`] = false;
        // })
      })
    },
    pageSizeChange(page_size){
      this.page_size = page_size;
      this.pageCurrentChange(1,page_size)
    },
    search(){
      searchall(this.code).then((response) =>{
        this.tableData = response.data.rows;
      })
    },
    uploadSuccess(res,file){
      if(file.status === 'success') {
        this.$message({
          message: '上传成功',
          type: 'success',
          showClose: true
        });
        this.pageCurrentChange(this.page_num,this.page_size);
      }
    },
    downloadExcel(){
      NProgress.start();
      download_user_bj({file:'123'}).then(function (res) {
        let date = new Date();
        let filename = date.getTime();
        let blob = new Blob([res.data], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8'});
        let downloadElement = document.createElement('a');
        let href = window.URL.createObjectURL(blob); //创建下载的链接
        downloadElement.href = href;
        downloadElement.download = filename; //下载后文件名
        document.body.appendChild(downloadElement);
        downloadElement.click(); //点击下载
        document.body.removeChild(downloadElement); //下载完成移除元素
        window.URL.revokeObjectURL(href); //释放掉blob对象
      });
      NProgress.done();
    },
  },
  mounted() {
    this.pageCurrentChange(1,10);
  }
}
</script>
