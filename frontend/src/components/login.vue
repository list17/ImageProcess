<template>
	<el-container>
		<el-main>
			<el-row type="flex" justify="center">
				<el-col>
					<el-container class="login-container">
						<el-header class="login-header" style="height: 30px;">
						欢迎来到List 图像处理
						</el-header>
						<el-form ref="AccountForm" :model="account" :rules="rules" label-position="left" label-width="0px" class="demo-ruleForm">
							<el-form-item prop="username" :error="errorMsg">
								<div align="left">用户名</div>
								<el-input type="text" v-model="account.username" auto-comlete="off" placeholder="请输入账号" prefix-icon="el-icon-third-geren"></el-input>
							</el-form-item>
							<el-form-item prop="password" :error="errorMsg">
								<div align="left">密码</div>
								<el-input type="password" v-model="account.password" auto-complete="off" placeholder="请输入密码" prefix-icon="el-icon-third-jiesuo"></el-input>
							</el-form-item>
							<el-button type="text" size="mini" style="margin-bottom: 10px;" @click="showForgetPwdDialog">忘记密码？</el-button>
							<el-form-item style="width:100%; text-align: center;">
								<el-button type="primary" style="width: 45%" round @click="login">登录</el-button><el-button style="width: 45%" round @click="register">注册</el-button>
							</el-form-item>
						</el-form>
					</el-container>
				</el-col>
			</el-row>
		</el-main>
	</el-container>
</template>

<script>
import {signal} from '../Signal.js'
export default {
	name: 'login',
	components: {
	},
	data() {
		return {
			logining: false,
			account: {
				username: '',
				password: '',
			},
			errorMsg: '',
			rules: {
				username: [
				{required: true, message: '请输入账号', trigger: 'blur'}
				],
				password: [
				{required: true, message: '请输入密码', trigger: 'blur'}
				]
			},
			checked: true,
			canPwdDlgShow: false,
		};
	},
	methods: {
		login() {
			this.$refs['AccountForm'].validate((valid) => {
				if (valid) {
					this.errorMsg = ''
					let params = new URLSearchParams()
					params.append('username', this.account.username)
					params.append('password', this.account.password)
					this.$axios.post('/user/login', params).then(response => {
						if (response.data['msg'] === "login success"){
							let data_t = {
								username: response.data['username'],
								userEmail: response.data['email'],
								nickname: response.data['nickname'],
							}
							this.$store.commit('login', data_t)
							signal.$emit('login')
							this.$router.push('/image_processing');
						}
						else if (response.data['msg'] === "already login"){
							let data_t = {
								username: response.data['username'],
								userEmail: response.data['email'],
								nickname: response.data['nickname'],
							}
							this.$cookies.remove('username');
							this.$store.commit('login', data_t)
							signal.$emit('login')
							this.$router.push('/image_processing');
						}
					})
					.catch(err=>{
						this.errorMsg = err.response.data['msg']
					})
				}
			})
		},
		register() {
			this.$router.push('/register')
		},
		showForgetPwdDialog() {
			this.canPwdDlgShow = true
		}
	},
	activated() {
		this.username = ''
		this.password = ''
	},
	beforeRouteEnter(to, from, next) {
		next(vm => {
			vm.$store.commit('setRouteList', []);
		})
	}
}
</script>

<style scoped>
.login-container {
	margin:0 auto;
	-webkit-border-radius: 5px;
	border-radius: 5px;
	-moz-border-radius: 5px;
	background-clip: padding-box;
	width: 350px;
	padding: 35px 35px 15px 35px;
	background: #fff;
	border: 1px solid #eaeaea;
	box-shadow: 0 0 25px #cac6c6;
}
.login-header {
	text-align: left;
	border-top: none;
	border-left: none;
	border-right:none;
	border-bottom: 1px solid #eaeaea;
}
</style>
