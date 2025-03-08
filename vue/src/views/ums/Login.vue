<template>
    <div class="login-container">
      <el-card class="login-card">
        <img class="logo" src="@/components/icons/favicon.ico" alt="logo" />
        <div class="welcome-msg">欢迎登录，请使用企业内部账号登录</div>
  
        <el-form ref="loginFormRef" :model="loginForm" :rules="rules" label-position="top">
          <el-form-item prop="username" >
            <el-input 
              v-model="loginForm.username" 
              style="width: 280px"
              size="large"
              placeholder="请输入账号">
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
  
          <el-form-item prop="password" >
            <el-input 
              v-model="loginForm.password" 
              type="password"
              style="width: 280px"
              size="large"
              placeholder="请输入密码" 
              show-password>
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
  
          <div class="options-row">
            <el-checkbox v-model="rememberMe">记住密码</el-checkbox>
            <el-link type="primary" @click="forgotPassword" class="forgot-password">忘记密码?</el-link>
          </div>
  
          <el-button 
            type="primary" 
            class="login-button" 
            :loading="loading"
            @click="handleLogin">
            登录
          </el-button>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { User, Lock } from '@element-plus/icons-vue'
  import { login } from '@/api/ums/login' 
  import { setToken } from '@/utils/auth'
  
  const router = useRouter()
  const loginFormRef = ref(null)
  const loading = ref(false)
  const rememberMe = ref(false)
  
  const loginForm = reactive({
    username: '',
    password: ''
  })
  
  // 登录表单验证
  const rules = {
    username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
  }
  
  // 记住密码
  onMounted(() => {
    const savedUsername = localStorage.getItem('remembered_username')
    const savedPassword = localStorage.getItem('remembered_password')
    if (savedUsername && savedPassword) {
      loginForm.username = savedUsername
      loginForm.password = savedPassword
      rememberMe.value = true
    }
  })
  
  // 处理登录
  const handleLogin = async () => {
    loginFormRef.value.validate(async valid => {
      if (!valid) return
  
      loading.value = true
      try {
        const { data } = await login(loginForm.username, loginForm.password)
        setToken(data.token)
        ElMessage.success('登录成功!')
  
        if (rememberMe.value) {
          localStorage.setItem('remembered_username', loginForm.username)
          localStorage.setItem('remembered_password', loginForm.password)
        } else {
          localStorage.removeItem('remembered_username')
          localStorage.removeItem('remembered_password')
        }
  
        router.push('/home')
      } catch (error) {
        ElMessage.error(error.response?.data?.message || '登录失败')
      } finally {
        loading.value = false
      }
    })
  }
  
  // 忘记密码
  const forgotPassword = () => {
    ElMessageBox.alert('请联系企业管理员重置密码', '忘记密码', {
      confirmButtonText: '好的',
    })
  }
  </script>
  
  <style scoped>
  .login-container {
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f2f4f8;
  }
  .login-card {
    width: 500px;
    padding: 100px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    border-radius: 12px;
    background: white;
  }
  .logo {
    width: 150px;
    height: auto;
    margin-bottom: 20px;
  }
  .welcome-msg {
    font-size: 16px;
    color: #666;
    margin-bottom: 28px;
  }

  .options-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .forgot-password {
    font-size: 13px;
    color: #409eff;
    cursor: pointer;
  }
  .login-button {
    width: 60%;
    height: 40px; 
    font-size: 15px;
    margin-top: 30px;
  }
  </style>
  