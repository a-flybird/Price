<template>
  <el-container>
    <el-main>
      <el-button icon="el-icon-edit" plain size="mini" @click="Create">创建角色</el-button>
      <el-table :data="roletable" size="mini" style="width: 98%;margin: 15px 1% auto 1%" border :header-cell-style="{background:'#F5F7FA'}">
        <el-table-column prop="role_code" width="120px" label="角色编码"></el-table-column>
        <el-table-column prop="role_name" width="120px" label="角色名称"></el-table-column>
        <el-table-column prop="description" width="120px" label="角色描述"></el-table-column>
        <el-table-column min-width="140px" label="操作">
          <template slot-scope="scope">
            <el-button size="mini" icon="el-icon-edit" @click="handleUpdate(scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog title="编辑" :visible.sync="dialogFormVisible" :close-on-click-modal="false" width="30%">
        <el-form :model="roleform" ref="dataForm" :rules="rules" label-position="left" style="margin: auto 20px auto 20px;" size="mini">
          <el-form-item label="角色编码" prop="role_code">
            <el-input v-model="roleform.role_code" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="角色名称" prop="role_name">
            <el-input v-model="roleform.role_name" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="角色描述" prop="description">
            <el-input v-model="roleform.description" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="角色权限" prop="smenus">
            <el-checkbox-group v-model="roleform.smenus">
              <el-checkbox v-for="menu in dmenus" :label="menu.key" :key="menu.key" name="smenus">{{menu.label}}</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button size="small" @click="cancel">取 消</el-button>
          <el-button type="primary" size="small" @click="dialogStatus==='create'?create_role():update_role()">保 存</el-button>
        </div>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script>
  import { show_role,show_menus,update_role,create_role } from '@/api/data';
  export default {
      name: "index",
      data(){
        return{
          dialogFormVisible:false,
          dialogStatus:'',
          roletable:[],
          dmenus:[],
          roleform:{
            role_code:'',
            role_name:'',
            description:'',
            smenus:[],
          },
          rules:{
            role_code: [{ required: true, message: '请输入角色编码'}],
            role_name: [{ required: true, message: '请输入角色名称'}],
            description: [{ required: true, message: '请输入角色描述'}],
          },
        }
      },
      methods:{
        cancel(){
          this.dialogFormVisible = false;
        },
        Create(){
          this.roleform = {
            role_code:'',
            role_name:'',
            description:'',
            smenus:[],
          };
          this.dialogStatus = 'create';
          this.dialogFormVisible = true;
        },
        handleUpdate(row){
          this.roleform = {...row, smenus: []};
          this.dialogStatus = 'update';
          this.dialogFormVisible = true;
          this.roleform.smenus = (row.menus || []).map(item => {
            return item.menu_code;
          });
          console.log(this.roleform.smenus,'123');

        },
        create_role(){
          let role = {
            'role_code':this.roleform.role_code,
            'role_name':this.roleform.role_name,
            'description':this.roleform.description,
            'menus':this.dmenus.map(one => {
              if(this.roleform.smenus.indexOf(one.key)>-1){
                return {
                  menu_code: one.key,
                  ischecked: true,
                }
              }else{
                return {
                  menu_code: one.key,
                  ischecked: false,
                }
              }
            })
          }
          create_role(role).then((response) =>{
            this.dialogFormVisible = false;
            this.show_role();
          })
        },
        update_role(){
          let role = {
            'role_code':this.roleform.role_code,
            'role_name':this.roleform.role_name,
            'description':this.roleform.description,
            'menus':this.dmenus.map(one => {
              if(this.roleform.smenus.indexOf(one.key)>-1){
                return {
                  menu_code: one.key,
                  ischecked: true,
                }
              }else{
                return {
                  menu_code: one.key,
                  ischecked: false,
                }
              }
            })
          }
          update_role(role).then((response) =>{
            this.dialogFormVisible = false;
            this.show_role();
          })
        },
        show_role(){
          show_role().then((response)=> {
            this.roletable = response.data.rows;
          })
        },
        show_menus(){
          this.dmenus=[];
          show_menus().then((response)=>{
            this.dmenus = (response.data.rows || []).map(item => {
              return { key: item.menu_code, label: item.menu_name, value: item.description};
            });
          })
        },
    },
    mounted() {
      this.show_role();
      this.show_menus();
    }
  }
</script>

<style scoped>

</style>
