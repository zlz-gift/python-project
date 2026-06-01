<script setup>
import { onMounted, ref } from "vue"
import { getProducts, createProduct, updateProduct, deleteProduct } from "../api/product"
import AppHeader from "../components/AppHeader.vue"
import AppFooter from "../components/AppFooter.vue"
import { ElMessage, ElMessageBox } from "element-plus"

const productList = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const currentId = ref(null)

const form = ref({
  name: "",
  price: null,
  stock: null,
  category: "",
  description: "",
  image: ""
})

const rules = {
  name: [{ required: true, message: "请输入商品名称", trigger: "blur" }],
  price: [{ required: true, message: "请输入价格", trigger: "blur" }],
  stock: [{ required: true, message: "请输入库存", trigger: "blur" }]
}

async function loadProducts() {
  const res = await getProducts({ page_size: 100 })
  productList.value = res.data.items || res.data
}

function openAdd() {
  isEdit.value = false
  currentId.value = null
  form.value = { name: "", price: null, stock: null, category: "", description: "", image: "" }
  dialogVisible.value = true
}

function openEdit(row) {
  isEdit.value = true
  currentId.value = row.id
  form.value = {
    name: row.name,
    price: row.price,
    stock: row.stock,
    category: row.category || "",
    description: row.description || "",
    image: row.image || ""
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  if (isEdit.value) {
    await updateProduct(currentId.value, form.value)
    ElMessage.success("商品更新成功")
  } else {
    await createProduct(form.value)
    ElMessage.success("商品创建成功")
  }
  dialogVisible.value = false
  loadProducts()
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定要删除「${row.name}」吗？`, "删除确认", {
      type: "warning"
    })
    await deleteProduct(row.id)
    ElMessage.success("删除成功")
    loadProducts()
  } catch {
    // cancelled
  }
}

onMounted(() => {
  loadProducts()
})
</script>

<template>
  <AppHeader />
  <div class="container" style="min-height: calc(100vh - 70px - 200px)">
    <div class="page-header">
      <h1>商品管理</h1>
      <el-button type="primary" @click="openAdd">添加商品</el-button>
    </div>

    <el-table :data="productList" border stripe class="product-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="名称" min-width="150" />
      <el-table-column prop="price" label="价格" width="100">
        <template #default="{ row }">¥{{ row.price }}</template>
      </el-table-column>
      <el-table-column prop="stock" label="库存" width="80" />
      <el-table-column prop="category" label="分类" width="120" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑商品' : '添加商品'"
      width="500px"
    >
      <el-form :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input v-model.number="form.price" />
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input v-model.number="form.stock" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="form.category" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="图片URL">
          <el-input v-model="form.image" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
  <AppFooter />
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.product-table {
  border-radius: 8px;
  overflow: hidden;
}
</style>
