<template>
	<el-container style="margin: auto">
    <el-main>
      <el-row type="flex" justify="center">
        <el-col :span = "9" :offset="3">
          <el-input placeholder="请输入内容" v-model="code" :clearable="true" size="small" @keyup.enter.native="pageCurrentChange(1,10)">
            <el-button slot="append" icon="el-icon-refresh-left" size="small" plain type="primary" @click="reset_search(1,10)">重 置</el-button>
            <el-button slot="append" icon="el-icon-search" size="small" style="margin-left: 20px" plain type="primary" @click="pageCurrentChange(1,10)">搜 索</el-button>
          </el-input>

        </el-col>
        <el-col :span = "2" :offset="6">
          <el-button v-if="user_role==='admin' || user_role==='editor'" icon="el-icon-edit" plain size="mini" @click="handleCreate">新 建</el-button>
        </el-col>
        <el-col :span = "2">
          <el-upload
            action="http://192.168.29.63:8990/api/upsert_user/"
            :headers="headers"
            :show-file-list="false"
            :on-progress="uploading"
            :on-success="uploadSuccess">
            <el-button v-if="user_role==='admin' || user_role==='editor'" icon="el-icon-upload2" plain size="mini" :loading="upload_status">导入/更新</el-button>
          </el-upload>
        </el-col>
        <el-col :span = "2">
          <el-button icon="el-icon-download" plain size="mini" @click="downloadExcel" :loading="download_status">导 出</el-button>
        </el-col>
      </el-row>
      <el-table :data="tableData" size="mini" style="width: 98%;margin: 15px 1% auto 1%" border :header-cell-style="{background:'#F5F7FA'}">
        <el-table-column prop="productcode" width="120px" label="编码"></el-table-column>
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="model" label="型号"></el-table-column>
        <el-table-column prop="description" :show-overflow-tooltip="true" min-width="240px" label="描述"></el-table-column>
        <el-table-column prop="product_type" width="70px" label="物料类型"></el-table-column>
        <el-table-column prop="price_source" width="70px" label="价格来源"></el-table-column>
        <el-table-column min-width="70px" label="RRP(USD)">
          <template slot-scope="scope">
            <span>&#36;{{ scope.row.RRP_USD }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="70px" label="RRP(EUR)">
          <template slot-scope="scope">
            <span>&#8364;{{ scope.row.RRP_EUR }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="70px" label="RRP(GBP)">
          <template slot-scope="scope">
            <span>&#163;{{ scope.row.RRP_GBP }}</span>
          </template>
        </el-table-column>
        <el-table-column min-width="70px" label="RRP(CNY)">
          <template slot-scope="scope">
            <span>&#165;{{ scope.row.RRP_RMB }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="createddate" :show-overflow-tooltip="true" label="创建时间"></el-table-column>
        <el-table-column prop="lastmodifieddate" :show-overflow-tooltip="true" label="修改时间"></el-table-column>
        <el-table-column prop="remark" :show-overflow-tooltip="true" label="备注"></el-table-column>
        <el-table-column v-if="user_role==='admin' || user_role==='editor'" min-width="170px" label="操作">
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
        <el-form :model="tempForm" ref="dataForm" :rules="rules" label-position="left" label-width="90px" style="margin: auto 20px auto 20px;" size="mini">
          <el-form-item prop="productcode" label="编码">
            <el-input v-model="tempForm.productcode" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="name" label="名称">
            <el-input v-model="tempForm.name" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="model" label="型号">
            <el-input v-model="tempForm.model" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="description" label="描述">
            <el-input v-model="tempForm.description" type="textarea"></el-input>
          </el-form-item>
          <el-form-item prop="product_type" label="物料类型">
<!--            <el-input v-model="tempForm.product_type" style="width: 250px"></el-input>-->
            <el-select v-model="tempForm.product_type" style="width: 250px">
              <el-option v-for="i in product_type_options" :key="i.value" :label="i.label" :value="i.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item prop="price_source" label="价格来源">
            <el-select v-model="tempForm.price_source" style="width: 250px">
              <el-option v-for="i in options" :key="i.value" :label="i.label" :value="i.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item prop="RRP_USD" label="RRP(USD)">
            <el-input v-model="tempForm.RRP_USD" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="RRP_EUR" label="RRP(EUR)">
            <el-input v-model="tempForm.RRP_EUR" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="RRP_GBP" label="RRP(GBP)">
            <el-input v-model="tempForm.RRP_GBP" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="RRP_RMB" label="RRP(CNY)">
            <el-input v-model="tempForm.RRP_RMB" type="number" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="createddate" label="创建时间">
            <el-input v-model="tempForm.createddate" :disabled="true" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="lastmodifieddate" label="修改时间">
            <el-input v-model="tempForm.lastmodifieddate" :disabled="true" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item prop="remark" label="备注">
            <el-input v-model="tempForm.remark" type="textarea"></el-input>
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
  import { delete_item,create_item,update_item,price_list,searchall,download_user } from '@/api/data';
  import NProgress from 'nprogress';
export default {
  name: "basedata",
  data(){
      return{
        user_role: this.$store.getters.roles,
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
          { value:'定价', label:'定价',},
          { value:'报价', label:'报价',},
          { value:'CPQ推送', label:'CPQ推送',},
        ],
        product_type_options:[
          { value:'自研硬件', label:'自研硬件',},
          { value:'自研软件', label:'自研软件',},
          { value:'外购硬件', label:'外购硬件',},
          { value:'外购软件', label:'外购软件',},
          { value:'定制软件', label:'定制软件',},
          { value:'其他硬件', label:'其他硬件',}
        ],
        tempForm: {
          productcode:'',
          name:'',
          model:'',
          description:'',
          product_type:'',
          price_source:'',
          RRP_USD:'',
          RRP_EUR:'',
          RRP_GBP:'',
          RRP_RMB:'',
          createddate:'',
          lastmodifieddate:'',
          remark:'',
        },
        rules:{
          description: [{ required: true, message: '请输入产品描述', trigger: 'blur'}],
          product_type: [{ required: true, message: '请输入物料类型', trigger: 'blur'}],
          price_source: [{ required: true, message: '请选择价格来源', trigger: 'blur'}],
        },
        upload_status:false,
        download_status:false,
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
      delete_item(data).then((response)=> {
        this.pageCurrentChange(this.page_num, this.page_size);
      })
    },
    createData(){
      const vv = this;
      let data = new FormData();
      data.append('productcode',this.tempForm['productcode'] || '');
      data.append('name',this.tempForm['name'] || '');
      data.append('model',this.tempForm['model'] || '');
      data.append('description',this.tempForm['description'] || '');
      data.append('product_type',this.tempForm['product_type'] || '');
      data.append('price_source',this.tempForm['price_source'] || '');
      data.append('RRP_USD',this.tempForm['RRP_USD'] || '');
      data.append('RRP_EUR',this.tempForm['RRP_EUR'] || '');
      data.append('RRP_GBP',this.tempForm['RRP_GBP'] || '');
      data.append('RRP_RMB',this.tempForm['RRP_RMB'] || '');
      data.append('remark',this.tempForm['remark'] || '');
      this.$refs['dataForm'].validate((valid)=>{
        if(valid){
          create_item(data).then((response)=>{
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
      data.append('name',this.tempForm['name'] || '');
      data.append('model',this.tempForm['model'] || '');
      data.append('description',this.tempForm['description'] || '');
      data.append('product_type',this.tempForm['product_type'] || '');
      data.append('price_source',this.tempForm['price_source'] || '');
      data.append('RRP_USD',this.tempForm['RRP_USD'] || '');
      data.append('RRP_EUR',this.tempForm['RRP_EUR'] || '');
      data.append('RRP_GBP',this.tempForm['RRP_GBP'] || '');
      data.append('RRP_RMB',this.tempForm['RRP_RMB'] || '');
      data.append('remark',this.tempForm['remark'] || '');
      this.$refs['dataForm'].validate((valid)=>{
        if(valid){
          update_item(data).then((response)=>{
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
      searchall(this.page_size,this.page_num,this.code).then((response) =>{
        NProgress.start();
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
    reset_search(page_num,page_size){
      this.code = '';
      this.pageCurrentChange(page_num,page_size);
    },
    search(){
      searchall(this.code).then((response) =>{
        this.tableData = response.data.rows;
        if(response.data.rows.length === 0){
          this.$message({
            message: '未查询到结果',
            type:'error',
            showClose:true
          });
        }
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
        NProgress.done();
        this.upload_status = false;
      }
    },
    uploading(){
      NProgress.start();
      this.upload_status = true;
    },
    downloadExcel(){
      NProgress.start();
      this.download_status = true;
      let vv = this;
      download_user({file:'123'}).then(function (res) {
        let date = new Date();
        let filename = date.toLocaleString().replace(/\//g,'-');
        let blob = new Blob([res.data], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8'});
        let downloadElement = document.createElement('a');
        let href = window.URL.createObjectURL(blob); //创建下载的链接
        downloadElement.href = href;
        downloadElement.download = filename.toString(); //下载后文件名
        document.body.appendChild(downloadElement);
        downloadElement.click(); //点击下载
        document.body.removeChild(downloadElement); //下载完成移除元素
        window.URL.revokeObjectURL(href); //释放掉blob对象
        NProgress.done();
        vv.download_status = false;
      });
    },
  },
  mounted() {
    this.pageCurrentChange(1,10);
  }
}
</script>
