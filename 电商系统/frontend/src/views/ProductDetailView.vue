<script setup>
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { getProductById } from "../api/product"
import { addCart } from "../api/cart"
import AppHeader from "../components/AppHeader.vue"
import AppFooter from "../components/AppFooter.vue"
import { ElMessage } from "element-plus"

const route = useRoute()
const router = useRouter()
const product = ref(null)
const quantity = ref(1)
const loading = ref(false)

async function loadProduct() {
  try {
    const res = await getProductById(route.params.id)
    product.value = res.data
  } catch {
    ElMessage.error("商品不存在")
    router.push("/")
  }
}

async function handleAddCart() {
  loading.value = true
  try {
    await addCart({
      product_id: product.value.id,
      quantity: quantity.value
    })
    ElMessage.success("加入购物车成功")
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "加入购物车失败")
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProduct()
})
</script>

<template>
  <AppHeader />
  <div class="container" v-if="product">
    <!-- 面包屑 -->
    <div class="breadcrumb">
      <el-breadcrumb separator=">">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ product.category }}</el-breadcrumb-item>
        <el-breadcrumb-item>{{ product.name }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 商品详情 -->
    <div class="detail-section">
      <!-- 左侧图片 -->
      <div class="image-area">
        <div class="main-image">
          <img
            :src="product.image || 'https://picsum.photos/500/500?random=' + product.id"
            :alt="product.name"
          />
        </div>
      </div>

      <!-- 右侧信息 -->
      <div class="info-area">
        <h1 class="product-name">{{ product.name }}</h1>
        <p class="product-category">
          <el-tag size="small">{{ product.category }}</el-tag>
        </p>

        <div class="price-area">
          <span class="current-price">¥{{ product.price }}</span>
          <span class="original-price">¥{{ (product.price * 1.2).toFixed(2) }}</span>
          <span class="discount-tag">限时8.3折</span>
        </div>

        <el-divider />

        <p class="product-description">
          <span class="desc-label">商品描述：</span>
          {{ product.description || '暂无描述' }}
        </p>

        <el-divider />

        <div class="stock-info">
          <span class="stock-label">库存：</span>
          <span :class="['stock-value', product.stock > 0 ? 'in-stock' : 'out-of-stock']">
            {{ product.stock > 0 ? `有货 (剩余${product.stock}件)` : '暂时缺货' }}
          </span>
        </div>

        <div class="action-area">
          <div class="quantity-control">
            <span class="qty-label">数量：</span>
            <el-input-number
              v-model="quantity"
              :min="1"
              :max="product.stock"
              :disabled="product.stock <= 0"
            />
          </div>

          <div class="action-buttons">
            <el-button
              type="primary"
              size="large"
              :disabled="product.stock <= 0"
              :loading="loading"
              @click="handleAddCart"
              class="add-cart-btn"
            >
              🛒 加入购物车
            </el-button>
            <el-button size="large" @click="router.push('/')">
              继续购物
            </el-button>
          </div>
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
  padding: 30px 20px 60px;
  min-height: calc(100vh - 70px - 200px);
}

.breadcrumb {
  margin-bottom: 30px;
  padding: 12px 0;
}

.detail-section {
  display: flex;
  gap: 48px;
  animation: fadeInUp 0.6s ease;
}

/* ---- 左侧图片 ---- */
.image-area {
  flex: 0 0 480px;
}

.main-image {
  width: 100%;
  height: 480px;
  border-radius: 16px;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f0 100%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.main-image:hover img {
  transform: scale(1.05);
}

/* ---- 右侧信息 ---- */
.info-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 12px;
  line-height: 1.4;
}

.product-category {
  margin: 0 0 20px;
}

.price-area {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 16px 0;
}

.current-price {
  font-size: 32px;
  font-weight: 700;
  color: #ff4757;
}

.original-price {
  font-size: 16px;
  color: #bbb;
  text-decoration: line-through;
}

.discount-tag {
  background: #ff6b6b;
  color: white;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.product-description {
  font-size: 15px;
  color: #555;
  line-height: 1.8;
  margin: 0;
}

.desc-label {
  font-weight: 600;
  color: #333;
}

.stock-info {
  margin-bottom: 24px;
}

.stock-label {
  color: #666;
  font-size: 14px;
}

.stock-value {
  font-weight: 600;
  font-size: 14px;
}

.in-stock {
  color: #2ed573;
}

.out-of-stock {
  color: #ff4757;
}

.action-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.qty-label {
  color: #666;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.add-cart-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-weight: 600;
  padding: 12px 32px;
}

.add-cart-btn:hover {
  opacity: 0.9;
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

@media (max-width: 768px) {
  .detail-section {
    flex-direction: column;
    gap: 24px;
  }

  .image-area {
    flex: none;
    width: 100%;
  }

  .main-image {
    height: 300px;
  }

  .product-name {
    font-size: 22px;
  }

  .current-price {
    font-size: 24px;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
