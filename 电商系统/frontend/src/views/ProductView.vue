<script setup>
import { onMounted, ref, computed } from "vue"
import { useRouter } from "vue-router"
import { getProducts, getCategories } from "../api/product"
import { addCart } from "../api/cart"
import AppHeader from "../components/AppHeader.vue"
import AppFooter from "../components/AppFooter.vue"
import { ElMessage } from "element-plus"

const router = useRouter()
const productList = ref([])
const allCategories = ref([])
const loading = ref(false)
const addingCart = ref({})

// 搜索/筛选
const keyword = ref("")
const selectedCategory = ref("")
const minPrice = ref("")
const maxPrice = ref("")

// 分页
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

// 轮播图
const carouselItems = [
  {
    title: "618年中大促",
    subtitle: "全场低至5折，限时抢购",
    color: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    icon: "🎉"
  },
  {
    title: "新品首发",
    subtitle: "最新数码产品，抢先体验",
    color: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    icon: "🚀"
  },
  {
    title: "品质生活",
    subtitle: "精选好物，提升生活品质",
    color: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
    icon: "✨"
  }
]

async function loadProducts() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (keyword.value) params.keyword = keyword.value
    if (selectedCategory.value) params.category = selectedCategory.value
    if (minPrice.value !== "") params.min_price = minPrice.value
    if (maxPrice.value !== "") params.max_price = maxPrice.value

    const res = await getProducts(params)
    productList.value = res.data.items
    total.value = res.data.total
  } catch {
    ElMessage.error("加载商品失败")
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  try {
    const res = await getCategories()
    allCategories.value = res.data
  } catch {
    // ignore
  }
}

function handleSearch() {
  currentPage.value = 1
  loadProducts()
}

function handleReset() {
  keyword.value = ""
  selectedCategory.value = ""
  minPrice.value = ""
  maxPrice.value = ""
  currentPage.value = 1
  loadProducts()
}

function handlePageChange(page) {
  currentPage.value = page
  loadProducts()
  window.scrollTo({ top: 0, behavior: "smooth" })
}

function goDetail(id) {
  router.push(`/products/${id}`)
}

async function handleAddCart(e, id) {
  e.stopPropagation()
  addingCart.value[id] = true
  try {
    await addCart({ product_id: id, quantity: 1 })
    ElMessage.success("加入购物车成功")
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || "加入购物车失败")
  } finally {
    addingCart.value[id] = false
  }
}

onMounted(() => {
  loadProducts()
  loadCategories()
})
</script>

<template>
  <AppHeader />

  <!-- 轮播 Banner -->
  <section class="hero-section">
    <el-carousel
      height="360px"
      :interval="5000"
      arrow="always"
      indicator-position="outside"
    >
      <el-carousel-item v-for="(item, index) in carouselItems" :key="index">
        <div class="carousel-slide" :style="{ background: item.color }">
          <div class="slide-content">
            <span class="slide-icon">{{ item.icon }}</span>
            <h2>{{ item.title }}</h2>
            <p>{{ item.subtitle }}</p>
            <el-button type="default" size="large" round @click="$router.push('/')">
              立即抢购
            </el-button>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </section>

  <!-- 主内容 -->
  <div class="container">
    <!-- 分类快捷导航 -->
    <div class="category-chips" v-if="allCategories.length > 0">
      <el-tag
        :type="selectedCategory === '' ? '' : 'info'"
        :effect="selectedCategory === '' ? 'dark' : 'plain'"
        class="category-chip"
        @click="selectedCategory = ''; handleSearch()"
      >
        全部
      </el-tag>
      <el-tag
        v-for="cat in allCategories"
        :key="cat"
        :type="selectedCategory === cat ? '' : 'info'"
        :effect="selectedCategory === cat ? 'dark' : 'plain'"
        class="category-chip"
        @click="selectedCategory = cat; handleSearch()"
      >
        {{ cat }}
      </el-tag>
    </div>

    <!-- 搜索区域 -->
    <div class="search-section">
      <div class="search-row">
        <el-input
          v-model="keyword"
          placeholder="搜索商品名称..."
          clearable
          class="search-input"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <span>🔍</span>
          </template>
        </el-input>

        <el-input
          v-model="minPrice"
          placeholder="最低价"
          class="price-input"
          @keyup.enter="handleSearch"
        />
        <span class="price-sep">—</span>
        <el-input
          v-model="maxPrice"
          placeholder="最高价"
          class="price-input"
          @keyup.enter="handleSearch"
        />

        <el-button type="primary" @click="handleSearch">
          🔍 搜索
        </el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>
    </div>

    <!-- 结果统计 -->
    <div class="result-info">
      <span class="result-count">共找到 <strong>{{ total }}</strong> 件商品</span>
    </div>

    <!-- 商品列表 -->
    <div v-loading="loading" class="product-list">
      <el-card
        v-for="item in productList"
        :key="item.id"
        class="product-card"
        shadow="hover"
        @click="goDetail(item.id)"
      >
        <div class="image-wrapper">
          <img
            :src="item.image || 'https://picsum.photos/400/400?random=' + item.id"
            :alt="item.name"
            class="product-image"
          />
          <div class="card-badge">热卖</div>
        </div>

        <div class="product-info">
          <h2 class="product-name">{{ item.name }}</h2>

          <p class="product-description">
            {{ item.description || '暂无描述' }}
          </p>

          <div class="card-footer">
            <div class="price-section">
              <span class="price">¥{{ item.price }}</span>
              <span class="original-price">¥{{ (item.price * 1.2).toFixed(2) }}</span>
            </div>

            <el-button
              type="primary"
              size="small"
              circle
              class="cart-btn"
              :loading="addingCart[item.id]"
              @click="(e) => handleAddCart(e, item.id)"
            >
              🛒
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && productList.length === 0" class="empty-result">
      <div class="empty-icon">📦</div>
      <p>暂无匹配的商品</p>
      <el-button @click="handleReset">清除筛选</el-button>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, total"
        background
        @current-change="handlePageChange"
      />
    </div>
  </div>

  <AppFooter />
</template>

<style scoped>
/* ---- Hero 轮播 ---- */
.hero-section {
  margin-bottom: 40px;
}

.carousel-slide {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide-content {
  text-align: center;
  color: white;
}

.slide-icon {
  font-size: 64px;
  display: block;
  margin-bottom: 10px;
  animation: bounce 2s infinite;
}

.slide-content h2 {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 10px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.slide-content p {
  font-size: 18px;
  margin: 0 0 24px;
  opacity: 0.9;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.slide-content :deep(.el-button--default) {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.5);
  font-weight: 600;
  font-size: 15px;
}

.slide-content :deep(.el-button--default:hover) {
  background: white;
  color: #333;
  border-color: white;
}

/* ---- 主容器 ---- */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 60px;
}

/* ---- 分类导航 ---- */
.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
}

.category-chip {
  cursor: pointer;
  padding: 6px 16px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.category-chip:hover {
  transform: translateY(-2px);
}

/* ---- 搜索区 ---- */
.search-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
}

.price-input {
  width: 110px;
}

.price-sep {
  color: #999;
  font-size: 14px;
}

.result-info {
  margin-bottom: 20px;
}

.result-count {
  font-size: 14px;
  color: #999;
}

.result-count strong {
  color: #667eea;
  font-size: 16px;
}

/* ---- 商品列表 ---- */
.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
  min-height: 200px;
}

.product-card {
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #f0f0f0;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15) !important;
}

.product-card :deep(.el-card__body) {
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.08);
}

.card-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.product-info {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px;
  color: #333;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-description {
  font-size: 13px;
  color: #999;
  margin: 0 0 12px;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.price-section {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.price {
  font-size: 20px;
  font-weight: 700;
  color: #ff6b6b;
}

.original-price {
  font-size: 12px;
  color: #ccc;
  text-decoration: line-through;
}

.cart-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-size: 18px;
}

.cart-btn:hover {
  opacity: 0.9;
}

/* ---- 空状态 ---- */
.empty-result {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 16px;
}

.empty-result p {
  font-size: 16px;
  color: #999;
  margin: 0 0 20px;
}

/* ---- 分页 ---- */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 40px;
  padding-top: 20px;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@media (max-width: 768px) {
  .hero-section {
    margin-bottom: 24px;
  }

  .carousel-slide {
    height: 240px;
  }

  .slide-content h2 {
    font-size: 24px;
  }

  .slide-content p {
    font-size: 14px;
  }

  .search-row {
    flex-direction: column;
  }

  .search-input, .price-input {
    width: 100%;
    min-width: unset;
  }

  .price-sep {
    display: none;
  }

  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
  }
}
</style>
