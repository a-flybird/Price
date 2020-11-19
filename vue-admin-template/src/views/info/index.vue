<template>
  <el-container>
    <el-main>
      <el-button icon="el-icon-edit" plain size="mini" @click="Create">注册用户</el-button>
      <el-table :data="usertable" size="mini" style="width: 98%;margin: 15px 1% auto 1%" border :header-cell-style="{background:'#F5F7FA'}">
        <el-table-column prop="username" width="240px" label="username"></el-table-column>
        <el-table-column prop="first_name" width="120px" label="first name"></el-table-column>
        <el-table-column prop="last_name" width="120px" label="last name"></el-table-column>
        <el-table-column prop="email" width="240px" label="email"></el-table-column>
        <el-table-column prop="roles.role_name" width="120px" label="role">
          <template slot-scope="scope">
            <el-tag type="danger" size="small" v-if="scope.row.roles.role_code === 'admin'">{{scope.row.roles.role_name}}</el-tag>
<!--            <el-tag size="small" v-if="scope.row.roles.role_code === 'editor'">{{scope.row.roles.role_name}}</el-tag>-->
            <el-tag type="success" size="small" v-if="scope.row.roles.role_code === 'visitor'">{{scope.row.roles.role_name}}</el-tag>
<!--            <el-tag type="success" size="small" v-if="scope.row.roles.role_code === 'editor_bj'">{{scope.row.roles.role_name}}</el-tag>-->
            <el-tag size="small" v-if="scope.row.roles.role_code!=='admin'&&scope.row.roles.role_code!=='visitor'">{{scope.row.roles.role_name}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column width="120px" label="is_active">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.is_active" disabled></el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="last_login" width="135px" label="last_login"></el-table-column>
        <el-table-column min-width="140px" label="edit">
          <template slot-scope="scope">
            <el-button size="mini" icon="el-icon-edit" @click="handleUpdate(scope.row)">编辑</el-button>
            <el-button v-if="user_role === 'admin'" size="mini" icon="el-icon-edit" @click="handleUpdate2(scope.row)">修改密码</el-button>
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
        <el-form :model="userform" ref="dataForm" :rules="rules" label-position="left" label-width="120px" style="margin: auto 20px auto 20px;" size="mini">
          <el-form-item label="username" prop="username">
            <el-input v-if="this.dialogStatus === 'update'" :disabled="true" v-model="userform.username" style="width: 250px"></el-input>
            <el-input v-if="this.dialogStatus === 'create'" v-model="userform.username" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="first name" prop="first_name">
            <el-input v-model="userform.first_name" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="last name" prop="last_name">
            <el-input v-model="userform.last_name" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="email" prop="email">
            <el-input v-model="userform.email" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="roles" prop="roles">
            <el-select v-model="userform.roles" clearable @change="change_userrole">
              <el-option v-for="item in userrole" :key="item.key" :label="item.label" :value="item.key"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="is_active" prop="is_active">
            <el-switch v-model="userform.is_active"></el-switch>
          </el-form-item>
          <el-form-item v-if="this.dialogStatus === 'create'" label="password" prop="password">
            <el-input v-model="userform.password" show-password style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item v-if="this.dialogStatus === 'create'" label="repassword" prop="re_password">
            <el-input v-model="userform.re_password" show-password style="width: 250px"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button size="small" @click="cancel">取 消</el-button>
          <el-button type="primary" size="small" @click="dialogStatus==='create'?create_user():update_user()">保 存</el-button>
        </div>
      </el-dialog>
      <el-dialog title="修改密码" :visible.sync="pwdVisible" label-position="left" label-width="60px" :close-on-click-modal="false">
        <el-form :model="pwdform" ref="pwdForm" :rules="pwds" style="margin: auto 20px auto 20px;" size="mini">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="pwdform.username" :disabled="true" style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="newpwd">
            <el-input v-model="pwdform.newpwd" show-password style="width: 250px"></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="newpwd">
            <el-input v-model="pwdform.re_newpwd" show-password style="width: 250px"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button size="small" @click="cancel">取 消</el-button>
          <el-button type="primary" size="small" @click="update_password()">保 存</el-button>
        </div>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script>
  import {show_user, show_role, register, update_user, update_pwd} from '@/api/data';
  export default {
      name: "index",
      data(){
        return{
          user_role: this.$store.getters.roles,
          dialogFormVisible:false,
          pwdVisible:false,
          dialogStatus:'',
          pwdStatus:'',
          usertable:[],
          userform:{
            username:'',
            first_name:'',
            last_name:'',
            email:'',
            roles:'',
            is_active:false,
            password:'',
            re_password:'',
          },
          total:1,
          page_num:1,
          page_size:10,
          pwdform:{
            id:'',
            username:'',
            newpwd:'',
            re_newpwd:'',
          },
          userrole:[],
          rules:{
            username: [{ required: true, message: '请输入用户名称'}],
            email: [{ required: true, message: '请输入邮箱'}],
            roles: [{ required: true, message: '请选择角色'}],
            password: [{ required: true, message: '请输入密码'}],
            re_password: [{ required: true, message: '请输再次入密码'}],
          },
          pwds:{
            username: [{ required: true, message: '请输入用户名称'}],
            newpwd: [{ required: true, message: '请输入密码'}],
            re_newpwd: [{ required: true, message: '请输再次入密码'}],
          },
        }
      },
      methods:{
        cancel(){
          this.dialogFormVisible = false;
          this.pwdVisible = false;
        },
        Create(){
          this.userform = {};
          this.dialogStatus = 'create';
          this.dialogFormVisible = true;
        },
        handleUpdate(row){
          this.dialogStatus = 'update';
          this.userform = Object.assign({},row);
          if(row.roles){this.userform.roles = row.roles.role_id;}//获取当前用户的角色id，因为不接受对象类型？
          this.dialogFormVisible = true;
        },
        handleUpdate2(row){
          this.pwdStatus = 'update';
          this.pwdform = Object.assign({},row);
          if(row.id){this.pwdform.id = row.id;}//获取当前用户id，因为不接受对象类型？
          this.pwdVisible = true;
        },
        update_password(){
          const pwd = new FormData();
          pwd.append('id',this.pwdform['id'] || '');
          pwd.append('newpwd',this.pwdform['newpwd'] || '');
          pwd.append('re_newpwd',this.pwdform['re_newpwd'] || '');
          update_pwd(pwd).then((res) =>{
            this.pwdVisible = false;
            this.pageCurrentChange(this.page_num,this.page_size);
          })
        },
        create_user(){
          const user = new FormData();
          user.append('username',this.userform['username'] || '');
          user.append('first_name',this.userform['first_name'] || '');
          user.append('last_name',this.userform['last_name'] || '');
          user.append('email',this.userform['email'] || '');
          user.append('roles',this.userform['roles'] || '');
          user.append('is_active',this.userform['is_active'] || false);
          user.append('password',this.userform['password'] || '');
          user.append('re_password',this.userform['re_password'] || '');
          register(user).then((response) =>{
            this.dialogFormVisible = false;
            this.pageCurrentChange(this.page_num,this.page_size);
          })
        },
        update_user(){
          const user = new FormData();
          user.append('id',this.userform['id'] || '');
          user.append('username',this.userform['username'] || '');
          user.append('first_name',this.userform['first_name'] || '');
          user.append('last_name',this.userform['last_name'] || '');
          user.append('email',this.userform['email'] || '');
          user.append('roles',this.userform['roles'] || '');
          user.append('is_active',this.userform['is_active'] || false);
          update_user(user).then((response) =>{
            this.dialogFormVisible = false;
            this.pageCurrentChange(this.page_num,this.page_size);
          })
        },
        // show_user(page_num, page_size){
        //   show_user(page_size, page_num).then((response)=>{
        //     this.usertable = response.data.rows.map(one => {
        //       const obj = one;
        //       if(obj.is_active === 1){
        //         obj.is_active = true;
        //       } else {
        //         obj.is_active = false;
        //       }
        //       return obj;
        //     });
        //   })
        // },
        pageCurrentChange(page_num,page_size){
          const vn = this;
          if(page_size){
            this.page_size = page_size;
          }
          if(page_num){
            this.page_num = Number(page_num);
          }
          show_user(this.page_size,this.page_num).then((response) =>{
            const { data } = response;
            vn.usertable = data.rows.map(one =>{
              const obj = one;
              if(obj.is_active ===1){
                obj.is_active = true;
              }else{
                obj.is_active = false;
              }
              return obj;
            });
            vn.total = data.total;
            vn.page_num = data.page_num;
          })
        },
        pageSizeChange(page_size){
          this.page_size = page_size;
          this.pageCurrentChange(1,page_size)
        },
        show_role(){
          show_role().then((response)=>{
            this.userrole = response.data.rows.map(item => {
              return { key: item.id, label: item.role_name,  value: item.description};
            });
          })
        },
        change_userrole(a){
          this.userform.roles = a;
        },
    },
    created() {
      this.$nextTick(() => {
        this.pageCurrentChange(1,10);
        this.show_role();
      });
    },
    mounted() {
      // this.pageCurrentChange(1,10);
    }
  }
</script>

<style scoped>

</style>
