<script setup>
import { onMounted, ref } from "vue"
import { getProducts } from "../api/product"
import { addCart } from "../api/cart"
import AppHeader from "../components/AppHeader.vue"

const productList = ref([])
const keyword = ref("")
const selectedCategory = ref("")
const minPrice = ref("")
const maxPrice = ref("")
const allCategories = ref([])

async function loadProducts() {
  const params = {}
  if (keyword.value) params.keyword = keyword.value
  if (selectedCategory.value) params.category = selectedCategory.value
  if (minPrice.value !== "") params.min_price = minPrice.value
  if (maxPrice.value !== "") params.max_price = maxPrice.value
  const res = await getProducts(params)
  productList.value = res.data
}

async function loadCategories() {
  const res = await getProducts()
  const categories = [...new Set(res.data.map(p => p.category).filter(Boolean))]
  allCategories.value = categories
}

function handleSearch() {
  loadProducts()
}

function handleReset() {
  keyword.value = ""
  selectedCategory.value = ""
  minPrice.value = ""
  maxPrice.value = ""
  loadProducts()
}

async function handleAddCart(id) {
  await addCart({
    product_id: id,
    quantity: 1
  })
  alert("加入购物车成功")
}

onMounted(() => {
  loadProducts()
  loadCategories()
})
</script>

<template>
  <AppHeader />
  <div class="container">
    <div class="header-section">
      <h1>商品中心</h1>
      <p class="subtitle">精选好货，优质生活</p>
    </div>

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

        <el-select
          v-model="selectedCategory"
          placeholder="全部分类"
          clearable
          class="category-select"
        >
          <el-option
            v-for="cat in allCategories"
            :key="cat"
            :label="cat"
            :value="cat"
          />
        </el-select>

        <el-input
          v-model="minPrice"
          placeholder="最低价"
          class="price-input"
        />

        <span class="price-sep">—</span>

        <el-input
          v-model="maxPrice"
          placeholder="最高价"
          class="price-input"
        />

        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>
    </div>

    <div class="product-list">
      <el-card
        v-for="item in productList"
        :key="item.id"
        class="product-card"
        shadow="hover"
      >
        <div class="image-wrapper">
          <img
            :src="'https://picsum.photos/300/200?random=' + item.id"
            class="product-image"
            alt="商品图片"
          >
          <div class="badge">新品</div>
        </div>
        
        <div class="product-info">
          <h2 class="product-name">{{ item.name }}</h2>
          
          <p class="product-description">
            {{ item.description }}
          </p>

          <div class="price-section">
            <span class="price">¥{{ item.price }}</span>
            <span class="original-price">¥{{ (item.price * 1.2).toFixed(2) }}</span>
          </div>

          <el-button
            type="primary"
            class="add-cart-btn"
            @click="handleAddCart(item.id)"
            round
          >
            <span>🛒 加入购物车</span>
          </el-button>
        </div>
      </el-card>
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
  margin-bottom: 50px;
  animation: fadeInDown 0.6s ease;
}

.header-section h1 {
  font-size: 42px;
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

.search-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
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

.category-select {
  width: 140px;
}

.price-input {
  width: 100px;
}

.price-sep {
  color: #999;
  font-size: 14px;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.product-card {
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #f0f0f0;
  height: 100%;
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

.badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.price-section {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.price {
  font-size: 20px;
  font-weight: 700;
  color: #ff6b6b;
}

.original-price {
  font-size: 13px;
  color: #ccc;
  text-decoration: line-through;
}

.add-cart-btn {
  width: 100%;
  margin-top: auto;
  font-weight: 600;
  height: 40px;
}

.add-cart-btn :deep(.el-button) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.add-cart-btn:hover :deep(.el-button) {
  opacity: 0.9;
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

@media (max-width: 768px) {
  .container {
    padding: 30px 15px;
  }

  .header-section h1 {
    font-size: 28px;
  }

  .search-row {
    flex-direction: column;
  }

  .search-input,
  .category-select,
  .price-input {
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