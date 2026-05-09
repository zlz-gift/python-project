<script setup>
import { reactive, ref } from "vue"
import { login } from "../api/user"
import { useRouter } from "vue-router"

const form = reactive({
  username: "",
  password: ""
})

const loading = ref(false)
const router = useRouter()

// 去注册页
function goRegister() {
  router.push("/register")
}

// 登录
async function handleLogin() {
  if (loading.value) return

  // ✅ 前端校验
  if (!form.username || !form.password) {
    alert("用户名或密码不能为空")
    return
  }

  loading.value = true

  try {
    const res = await login(form)

    // 存 token
    localStorage.setItem("token", res.data.token)

    // （可选）存用户信息
    if (res.data.user) {
      localStorage.setItem("user", JSON.stringify(res.data.user))
    }

    alert("登录成功")

    router.push("/")
  } catch (error) {
    console.log(error)

    alert(
      error?.response?.data?.detail ||
      "登录失败"
    )
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <el-card class="login-card">
      <h1 class="title">用户登录</h1>

      <el-form>
        <!-- 用户名 -->
        <el-form-item>
          <el-input
            v-model="form.username"
            placeholder="用户名"
            clearable
          />
        </el-form-item>

        <!-- 密码 -->
        <el-form-item>
          <el-input
            v-model="form.password"
            placeholder="密码"
            type="password"
            show-password
            clearable
          />
        </el-form-item>

        <!-- 登录按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%"
          >
            登录
          </el-button>
        </el-form-item>

        <!-- 注册入口 -->
        <el-form-item style="text-align: center;">
          <el-button type="text" @click="goRegister">
            没有账号？去注册
          </el-button>
        </el-form-item>

      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
}

.login-card {
  width: 400px;
  padding: 10px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}
</style>