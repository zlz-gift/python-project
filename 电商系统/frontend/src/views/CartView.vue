<script setup>
import { onMounted, ref, computed } from "vue"
import { useRouter } from "vue-router"
import { getCart, updateCart, deleteCart } from "../api/cart"
import { createOrder } from "../api/order"
import AppHeader from "../components/AppHeader.vue"
import AppFooter from "../components/AppFooter.vue"
import { ElMessage, ElMessageBox } from "element-plus"

const router = useRouter()
const cartList = ref([])
const loading = ref(false)

const totalPrice = computed(() => {
  return cartList.value.reduce(
    (sum, item) => sum + item.price * item.quantity, 0
  )
})

const totalQuantity = computed(() => {
  return cartList.value.reduce((sum, item) => sum + item.quantity, 0)
})

async function loadCart() {
  const res = await getCart()
  cartList.value = res.data
}

async function handleQuantityChange(item, newQty) {
  if (newQty < 1) newQty = 1
  try {
    await updateCart(item.cart_id, { quantity: newQty })
    item.quantity = newQty
  } catch {
    ElMessage.error("更新数量失败")
    loadCart()
  }
}

async function handleDelete(item) {
  try {
    await ElMessageBox.confirm(`确定要将「${item.name}」从购物车中移除吗？`, "删除确认", {
      type: "warning"
    })
    await deleteCart(item.cart_id)
    ElMessage.success("已移除")
    loadCart()
  } catch {
    // cancelled
  }
}

async function handleCheckout() {
  loading.value = true
  try {
    const res = await createOrder()
    ElMessage.success("下单成功！")
    router.push(`/orders/${res.data.order_id}`)
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "下单失败")
  } finally {
    loading.value = false
  }
}

function goProduct(id) {
  router.push(`/products/${id}`)
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
      <p>购物车为空，快去逛逛吧</p>
      <el-button type="primary" size="large" @click="router.push('/')">
        继续购物
      </el-button>
    </div>

    <div v-else class="cart-content">
      <div class="table-wrapper">
        <el-table
          :data="cartList"
          style="width: 100%"
          stripe
        >
          <el-table-column label="商品信息" min-width="280">
            <template #default="{ row }">
              <div class="product-cell" @click="goProduct(row.product_id)">
                <img
                  :src="row.image || 'https://picsum.photos/80/80?random=' + row.product_id"
                  class="product-thumb"
                  :alt="row.name"
                />
                <div class="product-meta">
                  <span class="product-name">{{ row.name }}</span>
                  <span class="product-price-mobile">¥{{ row.price }}</span>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="单价" width="110" align="right">
            <template #default="{ row }">
              <span class="price">¥{{ row.price }}</span>
            </template>
          </el-table-column>

          <el-table-column label="数量" width="150" align="center">
            <template #default="{ row }">
              <el-input-number
                :model-value="row.quantity"
                :min="1"
                :max="99"
                size="small"
                @change="(val) => handleQuantityChange(row, val)"
              />
            </template>
          </el-table-column>

          <el-table-column label="小计" width="120" align="right">
            <template #default="{ row }">
              <span class="subtotal">¥{{ (row.price * row.quantity).toFixed(2) }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="100" align="center" fixed="right">
            <template #default="{ row }">
              <el-button
                type="danger"
                text
                @click="handleDelete(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="summary-section">
        <div class="summary-card">
          <div class="summary-row">
            <span>商品种类：</span>
            <span class="val">{{ cartList.length }} 种</span>
          </div>
          <div class="summary-row">
            <span>总数量：</span>
            <span class="val">{{ totalQuantity }} 件</span>
          </div>
          <div class="divider"></div>
          <div class="summary-row total-row">
            <span>应付金额：</span>
            <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
          </div>
          <el-button
            type="primary"
            size="large"
            class="checkout-btn"
            :loading="loading"
            @click="handleCheckout"
          >
            去结算
          </el-button>
        </div>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 60px;
  min-height: calc(100vh - 70px - 200px);
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

/* ---- 空购物车 ---- */
.empty-cart {
  text-align: center;
  padding: 100px 20px;
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

/* ---- 购物车内容 ---- */
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

.table-wrapper :deep(.el-table th.el-table__cell) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.table-wrapper :deep(.el-table tr:hover > td) {
  background: #f9f9ff;
}

.product-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.product-cell:hover {
  opacity: 0.7;
}

.product-thumb {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  background: #f5f5f5;
}

.product-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.product-price-mobile {
  display: none;
  color: #ff6b6b;
  font-weight: 600;
}

.price {
  color: #ff6b6b;
  font-weight: 600;
  font-size: 15px;
}

.subtotal {
  color: #667eea;
  font-weight: 700;
  font-size: 15px;
}

/* ---- 结算区 ---- */
.summary-section {
  display: flex;
  justify-content: flex-end;
}

.summary-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #f9fafb 100%);
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 30px;
  min-width: 360px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  font-size: 15px;
  color: #666;
}

.summary-row .val {
  color: #333;
  font-weight: 600;
}

.total-row {
  margin-bottom: 0;
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
  height: 44px;
}

/* ---- 动画 ---- */
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
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
