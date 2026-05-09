<script setup>

import { onMounted, ref } from "vue"

import { getProducts } from "../api/product"

import { addCart } from "../api/cart"

import AppHeader from "../components/AppHeader.vue"

const productList = ref([])

async function loadProducts() {

  const res = await getProducts()

  productList.value = res.data
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
})

</script>

<template>

  <AppHeader />

  <div class="container">

    <h1>商城系统</h1>

    <div class="product-list">

      <el-card
        v-for="item in productList"
        :key="item.id"
        class="product-card"
      >

        <img
          :src="'https://picsum.photos/300/200'"
          class="product-image"
        >

        <h2>{{ item.name }}</h2>

        <p class="price">
          ￥{{ item.price }}
        </p>

        <p>
          {{ item.description }}
        </p>

        <el-button
          type="primary"
          @click="handleAddCart(item.id)"
        >
          加入购物车
        </el-button>

      </el-card>

    </div>

  </div>

</template>

<style scoped>

.container {

  width: 1200px;

  margin: 0 auto;
}

.product-list {

  display: grid;

  grid-template-columns:
    repeat(4, 1fr);

  gap: 20px;
}

.product-card {

  border-radius: 12px;
}

.product-image {

  width: 100%;

  border-radius: 10px;
}

.price {

  color: red;

  font-size: 22px;

  font-weight: bold;
}

</style>