<template>
  <div style="padding:20px">
    <h2>Dashboard</h2>

    <el-button @click="loadUser">获取用户信息</el-button>
    <el-button @click="logout" style="margin-left:10px">退出</el-button>

    <pre style="margin-top:20px">{{ user }}</pre>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { getMe } from "../api/user"
import { useUserStore } from "../store/user"
import { useRouter } from "vue-router"

const user = ref("")
const store = useUserStore()
const router = useRouter()

const loadUser = async () => {
  const res = await getMe()
  user.value = JSON.stringify(res, null, 2)
}

const logout = () => {
  store.logout()
  router.push("/login")
}
</script>