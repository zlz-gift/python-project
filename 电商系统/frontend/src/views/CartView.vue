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
<AppHeader />
<template>

  <div class="container">

    <h1>购物车</h1>

    <el-table
      :data="cartList"
      border
    >
    <div class="total-box">
    总价：
    <span class="price">
    ￥{{ totalPrice }}
    </span>

  </div>

      <el-table-column
        prop="name"
        label="商品名称"
      />

      <el-table-column
        prop="price"
        label="价格"
      />

      <el-table-column
        prop="quantity"
        label="数量"
      />

      <el-table-column
        label="操作"
      >

        <template #default="scope">

          <el-button
            type="danger"
            @click="handleDelete(scope.row.cart_id)"
          >
            删除
          </el-button>
          <el-button type="danger" @click="submitOrder">
            提交订单
          </el-button>

        </template>

      </el-table-column>

    </el-table>

  </div>

</template>

<style scoped>

.container {

  width: 1000px;

  margin: 50px auto;
}
.total-box {

  margin-top: 20px;

  text-align: right;

  font-size: 24px;

  font-weight: bold;
}

.price {

  color: red;
}

</style>