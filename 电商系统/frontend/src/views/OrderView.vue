<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { getOrders } from "../api/order"
import AppHeader from "../components/AppHeader.vue"
import AppFooter from "../components/AppFooter.vue"

const router = useRouter()
const orders = ref([])

async function loadOrders() {
  const res = await getOrders()
  orders.value = res.data
}

function goDetail(id) {
  router.push(`/orders/${id}`)
}

const statusType = (status) => {
  const map = { "已下单": "success", "已发货": "warning", "已完成": "info", "已取消": "danger" }
  return map[status] || "info"
}

onMounted(() => {
  loadOrders()
})
</script>

<template>
  <AppHeader />
  <div class="container">
    <div class="page-header">
      <h1>📋 我的订单</h1>
      <p class="subtitle">查看您的订单记录</p>
    </div>

    <div v-if="orders.length === 0" class="empty">
      <div class="empty-icon">📭</div>
      <p>暂无订单</p>
      <el-button type="primary" @click="router.push('/')">去逛逛</el-button>
    </div>

    <div v-else class="order-list">
      <el-card
        v-for="order in orders"
        :key="order.id"
        class="order-card"
        shadow="hover"
        @click="goDetail(order.id)"
      >
        <div class="order-header">
          <span class="order-id">订单号 #{{ order.id }}</span>
          <el-tag :type="statusType(order.status)" size="small">
            {{ order.status }}
          </el-tag>
        </div>
        <div class="order-body">
          <div class="item-summary">
            <span v-for="(item, i) in order.items.slice(0, 3)" :key="i" class="item-name">
              {{ item.name || '商品#' + item.product_id }}
            </span>
            <span v-if="order.items.length > 3" class="more">等{{ order.items.length }}件</span>
          </div>
          <div class="order-total">¥{{ order.total_price.toFixed(2) }}</div>
        </div>
      </el-card>
    </div>
  </div>
  <AppFooter />
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px 60px;
  min-height: calc(100vh - 70px - 200px);
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.empty {
  text-align: center;
  padding: 100px 20px;
  color: #999;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 16px;
}

.empty p {
  font-size: 16px;
  margin: 16px 0;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-card {
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.12) !important;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.order-id {
  font-weight: 600;
  color: #333;
  font-size: 15px;
}

.order-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  color: #999;
  font-size: 13px;
}

.item-name {
  background: #f5f5f5;
  padding: 2px 8px;
  border-radius: 4px;
}

.more {
  color: #667eea;
}

.order-total {
  font-size: 22px;
  font-weight: 700;
  color: #ff6b6b;
  flex-shrink: 0;
  margin-left: 16px;
}
</style>
