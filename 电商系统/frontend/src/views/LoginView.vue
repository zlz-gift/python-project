<script setup>
import { reactive, ref } from "vue"
import { login } from "../api/user"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"

const form = reactive({
  username: "",
  password: ""
})

const loading = ref(false)
const router = useRouter()

function goRegister() {
  router.push("/register")
}

async function handleLogin() {
  if (loading.value) return

  if (!form.username || !form.password) {
    ElMessage.warning("用户名或密码不能为空")
    return
  }

  loading.value = true

  try {
    const res = await login(form)
    localStorage.setItem("token", res.data.token)
    if (res.data.user) {
      localStorage.setItem("user", JSON.stringify(res.data.user))
    }
    ElMessage.success("登录成功")
    router.push("/")
  } catch (error) {
    ElMessage.error(
      error?.response?.data?.detail || "登录失败"
    )
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-content">
      <el-card class="login-card">
        <div class="logo-section">
          <div class="logo">🏪</div>
          <h1>欢迎登录</h1>
          <p>电商系统平台</p>
        </div>

        <el-form class="login-form" @keyup.enter="handleLogin">
          <!-- 用户名 -->
          <el-form-item>
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              clearable
              prefix-icon="User"
              size="large"
            />
          </el-form-item>

          <!-- 密码 -->
          <el-form-item>
            <el-input
              v-model="form.password"
              placeholder="请输入密码"
              type="password"
              show-password
              clearable
              prefix-icon="Lock"
              size="large"
            />
          </el-form-item>

          <!-- 登录按钮 -->
          <el-form-item class="button-item">
            <el-button
              type="primary"
              :loading="loading"
              @click="handleLogin"
              size="large"
              class="login-btn"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>

          <!-- 注册入口 -->
          <el-form-item class="register-item">
            <div class="register-link">
              <span>还没有账号？</span>
              <el-button type="text" @click="goRegister" class="text-link">
                立即注册
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 背景装饰 -->
    <div class="decoration decoration-1"></div>
    <div class="decoration decoration-2"></div>
    <div class="decoration decoration-3"></div>
  </div>
</template>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.login-content {
  position: relative;
  z-index: 10;
  animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.login-card {
  width: 400px;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: none;
  overflow: hidden;
}

.login-card :deep(.el-card__body) {
  padding: 48px 40px;
}

.logo-section {
  text-align: center;
  margin-bottom: 36px;
}

.logo {
  font-size: 56px;
  margin-bottom: 16px;
  animation: bounce 2s infinite;
}

.logo-section h1 {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px;
}

.logo-section p {
  color: #999;
  font-size: 14px;
  margin: 0;
}

.login-form {
  width: 100%;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.login-form :deep(.el-form-item:last-of-type) {
  margin-bottom: 0;
}

.login-form :deep(.el-input__wrapper) {
  background: #f5f7fa;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: #667eea;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.button-item {
  margin-top: 28px;
  margin-bottom: 16px;
}

.login-btn {
  width: 100%;
  height: 44px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(102, 126, 234, 0.3);
}

.register-item {
  text-align: center;
  margin: 0;
}

.register-link {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.text-link {
  color: #667eea;
  font-weight: 600;
  padding: 0;
}

.text-link:hover {
  color: #764ba2;
}

/* 背景装饰 */
.decoration {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  z-index: 1;
}

.decoration-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation: float 8s ease-in-out infinite;
}

.decoration-2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  right: -50px;
  animation: float 10s ease-in-out infinite 2s;
}

.decoration-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  right: 10%;
  animation: float 12s ease-in-out infinite 4s;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(30px);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@media (max-width: 600px) {
  .login-card {
    width: 90%;
    max-width: 360px;
  }

  .login-card :deep(.el-card__body) {
    padding: 36px 24px;
  }

  .logo-section {
    margin-bottom: 24px;
  }

  .logo-section h1 {
    font-size: 24px;
  }
}
</style>
