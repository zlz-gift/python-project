<template>
  <div>
    <!-- 🔍 顶部操作区 -->
    <div style="margin-bottom: 20px;">
      <el-input
        v-model="keyword"
        placeholder="请输入用户名"
        style="width: 200px; margin-right: 10px;"
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button type="success" @click="handleAdd">新增用户</el-button>
    </div>

    <!-- 📄 表格 -->
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />

      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">
            编辑
          </el-button>
          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 📦 分页 -->
    <div style="margin-top: 20px; text-align: right;">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="size"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 🧾 弹窗（新增 / 编辑共用） -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新增用户'">
      <el-form :model="form">
        <el-form-item label="用户名">
          <el-input v-model="form.username" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getUserList,
  deleteUser,
  updateUser,
  createUser
} from '@/api/user'
import { ElMessageBox, ElMessage } from 'element-plus'

// ===== 数据 =====

// 表格
const tableData = ref([])

// 分页
const page = ref(1)
const size = ref(5)
const total = ref(0)

// 搜索
const keyword = ref("")

// 弹窗
const dialogVisible = ref(false)

// 表单
const form = ref({
  id: null,
  username: '',
  password: ''
})

// 模式（新增 / 编辑）
const isEdit = ref(false)

// ===== 方法 =====

// 获取用户列表
const fetchUsers = async () => {
  const res = await getUserList({
    page: page.value,
    size: size.value,
    keyword: keyword.value
  })

  tableData.value = res.data.list
  total.value = res.data.total
}

// 搜索
const handleSearch = () => {
  page.value = 1
  fetchUsers()
}

// 分页
const handlePageChange = (p) => {
  page.value = p
  fetchUsers()
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该用户吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchUsers()
  })
}

// 编辑
const handleEdit = (row) => {
  form.value = { ...row, password: '' }
  dialogVisible.value = true
  isEdit.value = true
}

// 新增
const handleAdd = () => {
  form.value = { id: null, username: '', password: '' }
  dialogVisible.value = true
  isEdit.value = false
}

// 提交（核心：区分新增 / 编辑）
const handleSubmit = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  if (isEdit.value) {
    // 编辑
    await updateUser(form.value.id, form.value)
    ElMessage.success('更新成功')
  } else {
    // 新增
    await createUser(form.value)
    ElMessage.success('新增成功')
  }

  dialogVisible.value = false
  fetchUsers()
}

// 页面加载
onMounted(() => {
  fetchUsers()
})
</script>