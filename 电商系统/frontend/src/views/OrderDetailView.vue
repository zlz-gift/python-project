<script setup>
import { onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { getOrderById } from "../api/order"
import AppHeader from "../components/AppHeader.vue"
import AppFooter from "../components/AppFooter.vue"

const route = useRoute()
const order = ref(null)

async function loadOrder() {
  const res = await getOrderById(route.params.id)
  order.value = res.data
}

onMounted(() => {
  loadOrder()
})
</script>

<template>
  <AppHeader />
  <div class="container" v-if="order">
    <div class="page-header">
      <h1>📄 订单详情</h1>
    </div>

    <el-card class="info-card">
      <div class="info-row">
        <span class="label">订单号</span>
        <span class="value">#{{ order.id }}</span>
      </div>
      <div class="info-row">
        <span class="label">状态</span>
        <el-tag :type="order.status === '已下单' ? 'success' : 'info'">
          {{ order.status }}
        </el-tag>
      </div>
      <div class="info-row">
        <span class="label">应付金额</span>
        <span class="total-price">¥{{ order.total_price.toFixed(2) }}</span>
      </div>
    </el-card>

    <el-card class="items-card">
      <template #header>
        <span class="card-title">商品明细</span>
      </template>
      <el-table :data="order.items" stripe>
        <el-table-column prop="name" label="商品名称" min-width="200" />
        <el-table-column prop="price" label="单价" width="120">
          <template #default="{ row }">¥{{ row.price }}</template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="80" />
        <el-table-column label="小计" width="120">
          <template #default="{ row }">
            ¥{{ (row.price * row.quantity).toFixed(2) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <div class="back-row">
      <el-button @click="$router.push('/orders')">← 返回订单列表</el-button>
      <el-button type="primary" @click="$router.push('/')">继续购物</el-button>
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
  margin-bottom: 24px;
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

.info-card {
  margin-bottom: 20px;
  border-radius: 10px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.info-row + .info-row {
  border-top: 1px solid #f0f0f0;
}

.label {
  color: #999;
}

.value {
  font-weight: 600;
}

.total-price {
  font-size: 22px;
  font-weight: 700;
  color: #ff6b6b;
}

.items-card {
  border-radius: 10px;
  margin-bottom: 20px;
}

.card-title {
  font-weight: 600;
  font-size: 16px;
}

.back-row {
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 12px;
}
</style>
