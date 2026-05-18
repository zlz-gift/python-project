<script setup>

import { onMounted, ref, computed } from "vue"
import { deleteCart } from "../api/cart"
import { getCart } from "../api/cart"
import AppHeader from "../components/AppHeader.vue"
const cartList = ref([])
const totalPrice = computed(() => {

  return cartList.value.reduce(

    (sum, item) => {

      return sum +
        item.price * item.quantity
    },

    0
  )
})
async function loadCart() {

  const res = await getCart()

  cartList.value = res.data
}

async function handleDelete(id) {

  await deleteCart(id)

  alert("删除成功")

  loadCart()
}

onMounted(() => {

  loadCart()
})

</script>

<template>
  <AppHeader />
  <div class="container">
    <div class="header-section">
      <h1>🛒 购物车</h1>
      <p class="subtitle">查看和管理您的购物车</p>
    </div>

    <div v-if="cartList.length === 0" class="empty-cart">
      <div class="empty-icon">🛍️</div>
      <p>购物车为空</p>
      <el-button type="primary" href="/">继续购物</el-button>
    </div>

    <div v-else class="cart-content">
      <div class="table-wrapper">
        <el-table
          :data="cartList"
          style="width: 100%"
          stripe
          :default-sort="{ prop: 'name', order: 'ascending' }"
        >
          <el-table-column
            prop="name"
            label="商品名称"
            min-width="200"
          />

          <el-table-column
            prop="price"
            label="价格"
            width="100"
            align="right"
          >
            <template #default="{ row }">
              <span class="price">¥{{ row.price }}</span>
            </template>
          </el-table-column>

          <el-table-column
            prop="quantity"
            label="数量"
            width="100"
            align="center"
          />

          <el-table-column
            label="小计"
            width="120"
            align="right"
          >
            <template #default="{ row }">
              <span class="subtotal">¥{{ (row.price * row.quantity).toFixed(2) }}</span>
            </template>
          </el-table-column>

          <el-table-column
            label="操作"
            width="180"
            align="center"
            fixed="right"
          >
            <template #default="scope">
              <el-button
                type="danger"
                text
                @click="handleDelete(scope.row.cart_id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="summary-section">
        <div class="summary-card">
          <div class="summary-item">
            <span class="label">商品总数：</span>
            <span class="value">{{ cartList.length }}</span>
          </div>
          <div class="summary-item">
            <span class="label">总数量：</span>
            <span class="value">{{ cartList.reduce((sum, item) => sum + item.quantity, 0) }}</span>
          </div>
          <div class="divider"></div>
          <div class="summary-item total">
            <span class="label">应付金额：</span>
            <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
          </div>
          <el-button
            type="primary"
            size="large"
            class="checkout-btn"
          >
            🔐 去结算
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
  animation: fadeInDown 0.6s ease;
}

.header-section h1 {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 16px;
  color: #999;
  margin: 0;
}

.empty-cart {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

.empty-cart p {
  font-size: 18px;
  color: #999;
  margin: 20px 0;
}

.cart-content {
  animation: fadeInUp 0.6s ease;
}

.table-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
  overflow: hidden;
}

.table-wrapper :deep(.el-table) {
  border: none;
}

.table-wrapper :deep(.el-table thead.is-first-row th) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.table-wrapper :deep(.el-table th.el-table__cell) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.table-wrapper :deep(.el-table tr:hover > td) {
  background: #f9f9ff;
}

.price {
  color: #ff6b6b;
  font-weight: 600;
  font-size: 16px;
}

.subtotal {
  color: #667eea;
  font-weight: 600;
  font-size: 15px;
}

.summary-section {
  display: flex;
  justify-content: flex-end;
}

.summary-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #f9fafb 100%);
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 30px;
  min-width: 350px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 15px;
}

.summary-item.total {
  margin-bottom: 0;
}

.label {
  color: #666;
  font-weight: 500;
}

.value {
  color: #333;
  font-weight: 600;
  font-size: 16px;
}

.total-price {
  font-size: 28px;
  color: #ff6b6b;
  font-weight: 700;
}

.divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #ddd, transparent);
  margin: 20px 0;
}

.checkout-btn {
  width: 100%;
  margin-top: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-size: 16px;
  font-weight: 600;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@media (max-width: 768px) {
  .container {
    padding: 30px 15px;
  }

  .header-section h1 {
    font-size: 24px;
  }

  .summary-card {
    min-width: auto;
    width: 100%;
  }

  .summary-section {
    justify-content: stretch;
  }
}
</style>