<template>
  <div class="layout">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <h2 class="logo">Admin</h2>
      <el-menu
        :default-active="route.path"
        router
        background-color="#304156"
        text-color="#fff"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/dashboard">
          首页
        </el-menu-item>

        <el-menu-item index="/user">
          用户管理
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 右侧 -->
    <div class="main">
      <!-- 顶部 -->
      <div class="header">
        <div>后台管理系统</div>
        <el-button type="danger" @click="logout">退出</el-button>
      </div>

      <!-- 内容区 -->
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

/* 侧边栏 */
.sidebar {
  width: 200px;
  background: #304156;
  color: #fff;
}

.logo {
  text-align: center;
  padding: 20px 0;
}

/* 主区域 */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 顶部 */
.header {
  height: 60px;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

/* 内容 */
.content {
  flex: 1;
  padding: 20px;
  background: #f0f2f5;
}
</style>