<template>
  <div id="app">
    <div id="body">
      <el-menu v-if="$route.meta.navbar_active"
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-menu-item index="1">图片处理</el-menu-item>
        <el-menu-item index="2">历史记录</el-menu-item>
        <el-menu-item disabled style="width: 75%; text-align: center; font-size:20px">ImageProcessing</el-menu-item>
        <template slot="title">我的工作台</template>
        <el-submenu index="3">
          <template slot="title">个人信息</template>
          <el-menu-item index="3-1">修改密码</el-menu-item>
          <el-menu-item index="3-2">登出</el-menu-item>
        </el-submenu>
      </el-menu>
      <el-row class="topbar-wrap" type="flex" justify="center" v-if="$route.path!=='/help'">
      </el-row>
      <router-view @col-width="changeColWidth"/>
    </div>
    <footer>
      <p class="p1">问题反馈邮箱：lishengtao2017@gmail.com</p>
    </footer>
  </div>
</template>

<script>
import {signal} from './Signal.js'
export default {
  name: 'App',
  data() {
    return {
      colWidth: 18,
      username: '',
      activeIndex: '1',
    }
  },
  methods: {
    logout() {
      this.$confirm('是否确认登出', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(() => {
        this.$axios.get('/user/logout').then((response) => {
        this.$cookies.remove('username');
        this.$router.push('/login');
      }).catch((err) => {console.log(err);})})
    },
    handleSelect(key, keypath){
      console.log(key)
      if(key === '2'){
        this.activeIndex = "2";
        this.$router.push('/history');
      }
      else if(key === '1'){
        this.activeIndex = "1";
        this.$router.push('/image_processing')
      }
      else if(key === '3-1'){
        this.$confirm("目前仍不支持修改密码，待后续更新")
      }
      else if(key === '3-2'){
        this.logout()
      }
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
  color: #2c3e50;
}
.topbar-wrap {
  background-color: #ffffff;
  border-bottom: solid 1px #e6e6e6;
  margin-bottom: 20px;
}
.topbar-title {
  height: 62px;
  width:50%;
  font-weight: bold;
  font-size: large;
  display: -webkit-box;
  text-align: right;
  -webkit-box-pack:center;
  -webkit-box-orient: vertical;
}
.topbar-user {
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
  margin-block-start: 5px;
}
</style>
