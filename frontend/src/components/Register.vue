<template>
	<el-container>
		<el-main>
			<el-row type="flex" justify="center">
				<el-col :span="10">
					<el-container class="register-container">
						<el-header class="register-header" style="height: 30px;">
							注册您的账号
						</el-header>
						<el-main>
							<el-form ref="AccountForm" :model="account" :rules="rules" label-position="left" label-width="0px" class="demo-ruleForm">
								<el-form-item class="register-item" prop="nickname" :error="error.usernameErrorMsg">
									<div align="left">昵称</div>
									<el-input type="text" v-model="account.nickname" placeholder="请输入昵称" prefix-icon="el-icon-third-geren"></el-input>
								</el-form-item>
								<el-form-item class="register-item" prop="password" :error="error.passwordErrorMsg">
									<div align="left">密码</div>
									<el-input type="password" v-model="account.password" placeholder="请输入密码" prefix-icon="el-icon-third-jiesuo"></el-input>
								</el-form-item>
								<el-form-item class="register-item" prop="password2">
									<div align="left">确认密码</div>
									<el-input type="password" v-model="account.password2" placeholder="请确认密码" prefix-icon="el-icon-third-jiesuo"></el-input>
								</el-form-item>
								<el-form-item class="register-item" prop="email" :error="error.emailErrorMsg">
									<div align="left">邮箱</div>
									<el-input type="email" v-model="account.email" placeholder="请输入邮箱" prefix-icon="el-icon-third-youxiang"></el-input>
								</el-form-item>
								<el-form-item style="width:100%; text-align: center;">
									<el-button style="width: 45%" round @click="register">注册</el-button>
									<el-button style="width: 45%" round @click="cancel">取消</el-button>
								</el-form-item>
							</el-form>
						</el-main>
					</el-container>
				</el-col>
			</el-row>
		</el-main>
	</el-container>
</template>

<script>
export default {
	name: 'register',
	data() {
		let validator_password = (rule, value, callback) => {
			if (!value) {
				callback (new Error('请输入密码'))
			}
			else {
				if (value.length < 6) {
					callback (new Error('密码长度至少大于6个字符'))
				}
				callback()
			}
		}
		let validator_password2 = (rule, value, callback) => {
			if (!value) {
				callback (new Error('请确认密码'))
			}
			else {
				if (value !== this.account.password) {
					callback (new Error('两次密码不一致'))
				}
				callback()
			}
		}

		let validator_email = (rule, value, callback) => {
			if (!value) {
				callback (new Error('请输入邮箱'))
			}
			else {
				let pattern = /^([a-zA-Z0-9]+[-_\.]?)+@[a-zA-Z0-9]+\.[a-z]+$/
				if (!pattern.test(value)) {
					callback(new Error('请输入正确格式的邮箱'))
				}
				callback()
			}
		}

		return {
			account: {
				nickname: '',
				password: '',
				password2: '',
				code: '',
				email: ''
			},
			error: {
				usernameErrorMsg: '',
				passwordErrorMsg: '',
				emailErrorMsg: '',
			},
			rules: {
				nickname: [
				{required: true, message: '请输入昵称', trigger: 'blur'}
				],
				password: [
				{required: true, message: '请输入密码', trigger: 'blur'}
				],
				password2: [
				{required: true, trigger: 'blur', validator: validator_password2}
				],
				email: [
				{required: true, trigger: 'blur', validator: validator_email}
				]
			}
		};
	},
	methods: {
		register: function() {
			let params = new URLSearchParams()
			params.append('nickname', this.account.nickname)
			params.append('password', this.account.password)
			params.append('email', this.account.email)
			this.$axios.post('/user/register/', params).then(response=>{
				this.$confirm("确认注册邮件已发送至您注册所用的邮箱，请注意查收，一天后失效。","确定").then(()=>{
					this.$router.push('/login')
				})
			})
			.catch(err=>{
				this.$confirm(err.response.data['msg'],"确定")
			})
		},
		cancel: function() {
			this.$router.go(-1)
		}
	},
	created() {
	}
}
</script>

<style scoped>
	.register-container {
		-webkit-border-radius: 5px;
		border-radius: 5px;
		-moz-border-radius: 5px;
		background-clip: padding-box;
		margin: 0 auto;
		width: 400px;
		padding: 35px 35px 15px 35px;
		background: white;
		border: 1px solid #eaeaea;
		box-shadow: 0 0 25px #cac6c6;
	}
	.register-header {
		text-align: left;
		border-top: none;
		border-left: none;
		border-right:none;
		border-bottom: 1px solid #eaeaea;
	}
	.register-item {
		margin-bottom: 8px;
	}
</style>
