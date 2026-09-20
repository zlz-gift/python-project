<script setup>

import { useRouter } from "vue-router"
import { onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { getUserInfo } from "../api/user"
import { useCartStore } from "../stores/cart"

const router = useRouter()
const cartStore = useCartStore()
// 购物车角标数据来自全局 store，加购后自动更新，无需刷新页面
const { totalCount } = storeToRefs(cartStore)
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
  localStorage.removeItem("user")
  cartStore.reset() // 清空购物车缓存，避免切换账号后残留上一个账号的数据

  router.push("/login")
}

async function loadUserInfo() {

  if (!localStorage.getItem("token")) return

  try {
    const res = await getUserInfo()

    nickname.value = res.data.nickname
    isAdmin.value = res.data.role === "admin"
  } catch {
    // 401 已由响应拦截器统一处理（清理登录态并跳转登录页）
  }
}

onMounted(() => {

  loadUserInfo()
  cartStore.fetch() // 进入任意页面都会同步角标；store 内有缓存标记，不会重复请求
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

      <el-badge
        :value="totalCount"
        :hidden="totalCount === 0"
        class="cart-badge"
      >
        <el-button
          type="primary"
          @click="goCart"
        >
          购物车
        </el-button>
      </el-badge>

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

/* el-badge 包裹按钮后需保持 flex 对齐，否则角标会挤压按钮位置 */
.cart-badge {
  display: inline-flex;
  align-items: center;
}

.cart-badge :deep(.el-badge__content) {
  border: none;
  font-weight: 600;
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