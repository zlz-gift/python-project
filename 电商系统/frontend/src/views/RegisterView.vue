<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import { register } from "../api/user"

const router = useRouter()
const loading = ref(false)

const form = reactive({
  username: "",
  password: "",
  nickname: ""
})

// 注册
async function handleRegister() {
  if (loading.value) return

  // ✅ 前端校验（非常重要）
  if (!form.username || !form.password || !form.nickname) {
    alert("请填写完整信息")
    return
  }

  if (form.password.length < 6) {
    alert("密码至少6位")
    return
  }

  loading.value = true

  try {
    await register(form)

    alert("注册成功")

    // 注册成功跳登录
    router.push("/login")

  } catch (error) {
    console.log(error)

    alert(
      error?.response?.data?.detail ||
      "注册失败"
    )
  } finally {
    loading.value = false
  }
}

// 去登录
function goLogin() {
  router.push("/login")
}
</script>

<template>
  <div class="register-container">
    <el-card class="register-card">

      <h1 class="title">用户注册</h1>

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
            placeholder="密码（至少6位）"
            type="password"
            show-password
            clearable
          />
        </el-form-item>

        <!-- 昵称 -->
        <el-form-item>
          <el-input
            v-model="form.nickname"
            placeholder="昵称"
            clearable
          />
        </el-form-item>

        <!-- 注册按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleRegister"
            style="width: 100%"
          >
            注册
          </el-button>
        </el-form-item>

        <!-- 去登录 -->
        <el-form-item style="text-align: center;">
          <el-button type="text" @click="goLogin">
            已有账号？去登录
          </el-button>
        </el-form-item>

      </el-form>

    </el-card>
  </div>
</template>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
}

.register-card {
  width: 400px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}
</style>