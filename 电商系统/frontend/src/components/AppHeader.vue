<script setup>

import { useRouter } from "vue-router"
import { onMounted, ref } from "vue"
import { getUserInfo } from "../api/user"
const router = useRouter()
const nickname = ref("")
const isAdmin = ref(false)
function goHome() {

  router.push("/")
}

function goCart() {

  router.push("/cart")
}

function goAdmin() {

  router.push("/admin/products")
}

function logout() {

  localStorage.removeItem("token")

  router.push("/login")
}

async function loadUserInfo() {

  const res = await getUserInfo()

  nickname.value = res.data.nickname
  isAdmin.value = res.data.role === "admin"
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
        @click="() => router.push('/orders')"
      >
        我的订单
      </el-button>

      <el-button
        type="primary"
        @click="goCart"
      >
        购物车
      </el-button>

      <el-button
        v-if="isAdmin"
        type="success"
        @click="goAdmin"
      >
        管理后台
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
  height: 70px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  color: white;
  font-size: 24px;
  font-weight: 600;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.user-info {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  flex: 1;
  text-align: center;
}

.menu {
  display: flex;
  gap: 12px;
}

.menu :deep(.el-button) {
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.menu :deep(.el-button--default) {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.menu :deep(.el-button--default:hover) {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.menu :deep(.el-button--primary) {
  background: rgba(255, 255, 255, 0.3);
  border-color: white;
}

.menu :deep(.el-button--primary:hover) {
  background: white;
  color: #667eea;
}

.menu :deep(.el-button--danger) {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.menu :deep(.el-button--danger:hover) {
  background: #ff6b6b;
  border-color: #ff6b6b;
  color: white;
}

@media (max-width: 768px) {
  .header {
    padding: 0 20px;
    height: 60px;
  }
  
  .logo {
    font-size: 18px;
  }
  
  .user-info {
    font-size: 12px;
  }
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