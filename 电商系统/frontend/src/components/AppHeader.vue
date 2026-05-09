<script setup>

import { useRouter } from "vue-router"
import { onMounted, ref } from "vue"
import { getUserInfo } from "../api/user"
const router = useRouter()
const nickname = ref("")
function goHome() {

  router.push("/")
}

function goCart() {

  router.push("/cart")
}

function logout() {

  localStorage.removeItem("token")

  router.push("/login")
}

async function loadUserInfo() {

  const res = await getUserInfo()

  nickname.value = res.data.nickname
}

onMounted(() => {

  loadUserInfo()
})
</script>

<template>

  <div class="header">

    <div
      class="logo"
      @click="goHome"
    >
      电商系统
    </div>
    <div class="user-info">
        欢迎你，{{ nickname }}
    </div>

    <div class="menu">

      <el-button
        @click="goHome"
      >
        首页
      </el-button>

      <el-button
        type="primary"
        @click="goCart"
      >
        购物车
      </el-button>

      <el-button
        type="danger"
        @click="logout"
      >
        退出登录
      </el-button>

    </div>

  </div>

</template>

<style scoped>

.header {

  height: 60px;

  background: #24292f;

  display: flex;

  justify-content: space-between;

  align-items: center;

  padding: 0 40px;
}

.logo {

  color: white;

  font-size: 24px;

  font-weight: bold;

  cursor: pointer;
}

.menu {

  display: flex;

  gap: 10px;
}
.user-info {

  color: white;

  margin-right: 20px;
}
</style>