<template>
  <div id="app">
    <div id="body">
      <el-row class="topbar-wrap" type="flex" justify="center" v-if="$route.path!=='/help'">
        <el-col :span="2" class="topbar-title">
          <div>
            ImageProcessing
          </div>
        </el-col>
        <!-- <el-col :span="19" class="topbar-nav" v-if="$route.meta.navbar_active">
          <nav-bar>
          </nav-bar>
        </el-col>
        <el-col :span="19" v-else></el-col>
        <el-col :span="1" style="height: 62px;" class="topbar-user" v-if="$route.meta.icon_active">
          <el-dropdown :hide-on-click="false" v-model="nickname">
            <span class="el-dropdown-link" style="cursor: pointer;">
              <i class="el-icon-third-zhanghu"></i>
              {{$store.state.nickname}}
            </span>
            <el-dropdown-menu  slot="dropdown">
              <el-dropdown-item command="logout">退出</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-col> -->

<!-- <el-col :span="1" class="test-btn" v-if="$route.name!=='login'&&$route.name!=='register'">
          <span @click="editTest">
                测试
          </span>
        </el-col> -->

      </el-row>
      <router-view @col-width="changeColWidth"/>
    </div>
    <footer>
      <p class="p2">问题反馈邮箱：lishengtao2017@gmail.com</p>
    </footer>
  </div>
</template>

<script>
import {signal} from './Signal.js'
export default {
  name: 'App',
  components:{
  },
  data() {
    return {
      colWidth: 18,
      canPwdDlgShow: false,
      username: ''
    }
  },
  methods: {
    logout() {
      this.$confirm('是否确认登出', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      })
      .then(() => {
        this.$axios.get('/user/logout')
        .then((response) => {
          this.$cookies.remove('username');
          this.$router.push('/login');
        })
        .catch((err) => {
        })
      })
      .catch(() => {
      })
    },
    changeColWidth(val) {
      this.colWidth = val;
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
}
.topbar-wrap {
  background-color: #ffffff;
  border-bottom: solid 1px #e6e6e6;
  margin-bottom: 20px;
}
.topbar-title {
  height: 62px;
  font-weight: bold;
  font-size: large;
  display: -webkit-box;
  -webkit-box-pack:center;
  -webkit-box-align:center;
  -webkit-box-orient: vertical;
  text-align: center;
}
.topbar-user {
  display: -webkit-box;
  -webkit-box-pack:center;
  -webkit-box-align:center;
  -webkit-box-orient: vertical;
  text-align: center;
}
.help-btn {
  font-size: 14px;
  cursor: pointer;
  height: 62px;
  /*font-weight: bold;*/
  /*font-size: large;*/
  display: -webkit-box;
  -webkit-box-pack:center;
  -webkit-box-align:center;
  -webkit-box-orient: vertical;
  text-align: center;
}
.test-btn{
  font-size: 14px;
  cursor: pointer;
  height: 62px;
  display: -webkit-box;
  -webkit-box-pack:center;
  -webkit-box-align:center;
  -webkit-box-orient: vertical;
  text-align: center;
}
#body {
  min-height: 100%;
  padding-bottom: 41px;
}
footer {
  height: 41px;
  margin-top: -41px;
  text-align: center;
  background-color: #ffffff;
  bottom:0;
  position: relative;
  width: 100%;
  font-size: small;
  color: #909399;
}
footer .p1{
  margin-block-end: 5px;
}
footer .p2{
  margin-block-start: 5px;
}
</style>
