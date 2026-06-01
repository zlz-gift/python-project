# 电商系统

一个基于 **Vue 3 + Element Plus + FastAPI + SQLAlchemy** 的全栈电商系统。

## 功能特性

- 🔐 用户注册/登录（JWT 认证）
- 🏠 首页轮播 Banner
- 🔍 商品搜索、分类筛选、价格区间筛选
- 📄 商品分页浏览 & 商品详情页
- 🛒 购物车（添加、修改数量、删除）
- 📋 订单管理（下单、订单列表、订单详情）
- 👑 管理后台（商品 CRUD）
- 🎨 现代化 UI 设计，响应式布局
- 📱 支持移动端

## 技术栈

### 前端
- Vue 3 (Composition API)
- Vue Router 4
- Element Plus
- Axios
- Vite

### 后端
- FastAPI
- SQLAlchemy
- SQLite
- JWT 认证
- bcrypt 密码加密

## 快速开始

### 1. 克隆项目
```bash
git clone <repo-url>
cd 电商系统
```

### 2. 启动后端
```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化种子数据
python seed_data.py

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 3. 启动前端
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问系统
- 前端地址：http://localhost:5173
- 后端 API 文档：http://localhost:8000/docs

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 普通用户 | test | test123 |

## 项目结构

```
电商系统/
├── backend/
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 安全验证、依赖
│   │   ├── db/           # 数据库配置
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # Pydantic 校验
│   │   └── main.py       # 入口文件
│   ├── seed_data.py      # 种子数据脚本
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # API 请求封装
│   │   ├── components/   # 公共组件
│   │   ├── views/        # 页面组件
│   │   ├── router/       # 路由配置
│   │   └── utils/        # 工具函数
│   └── package.json
└── README.md
```

## 商品分类

- 📱 手机数码
- 💻 电脑办公
- 🏠 家用电器
- 👔 服饰鞋包
- 🍔 食品生鲜
- 💄 美妆个护
- ⚽ 运动户外
- 🛋️ 家居家装
