<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { getOrders } from "../api/order"
import AppHeader from "../components/AppHeader.vue"

const router = useRouter()
const orders = ref([])

async function loadOrders() {
  const res = await getOrders()
  orders.value = res.data
}

function goDetail(id) {
  router.push(`/orders/${id}`)
}

onMounted(() => {
  loadOrders()
})
</script>

<template>
  <AppHeader />
  <div class="container">
    <div class="page-header">
      <h1>我的订单</h1>
    </div>

    <div v-if="orders.length === 0" class="empty">
      <p>暂无订单</p>
      <el-button type="primary" @click="$router.push('/')">去逛逛</el-button>
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
          <el-tag :type="order.status === '已下单' ? 'success' : 'info'">
            {{ order.status }}
          </el-tag>
        </div>
        <div class="order-body">
          <div class="item-summary">
            共 {{ order.items.length }} 件商品
          </div>
          <div class="order-total">¥{{ order.total_price.toFixed(2) }}</div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.empty {
  text-align: center;
  padding: 80px 20px;
  color: #999;
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
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.order-id {
  font-weight: 600;
  color: #333;
}

.order-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-summary {
  color: #999;
  font-size: 14px;
}

.order-total {
  font-size: 20px;
  font-weight: 700;
  color: #ff6b6b;
}
</style>
