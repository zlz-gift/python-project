<template>
  <div style="width:300px;margin:100px auto">
    <el-input v-model="username" placeholder="用户名" />
    <el-input v-model="password" type="password" placeholder="密码" style="margin-top:10px"/>
    <el-button type="primary" @click="handleLogin" style="margin-top:10px;width:100%">
      登录
    </el-button>
  </div>
</template>

<<script setup>
import { ref } from "vue"
import { login } from "../api/user"
import { useRouter } from "vue-router"

const username = ref("admin")
const password = ref("123456")
const router = useRouter()

const handleLogin = async () => {
  const res = await login({
    username: username.value,
    password: password.value
  })
  console.log("login返回:", res)

  // ⭐兼容后端返回结构
  const token = res?.access_token || res?.data?.access_token

  if (!token) {
    console.error("❌ token为空，后端返回：", res)
    return
  }

  localStorage.setItem("token", token)

  router.push("/")
}
</script>