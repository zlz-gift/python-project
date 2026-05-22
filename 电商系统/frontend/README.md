# 电商系统 - 前端

## 技术栈

**Vue 3** (Composition API + `<script setup>`) · **Vite** · **Vue Router** · **Axios** · **Element Plus**

## 项目结构

```
src/
├── api/                  # API 请求层
│   ├── cart.js           #   购物车接口
│   ├── order.js          #   订单接口
│   ├── product.js        #   商品接口
│   └── user.js           #   用户接口（登录/注册/信息）
├── components/           # 公共组件
│   ├── AppHeader.vue     #   顶部导航栏（含角色识别）
│   └── HelloWorld.vue    #   脚手架遗留（未使用）
├── router/
│   └── index.js          # 路由配置 + JWT 鉴权守卫
├── utils/
│   └── request.js        # Axios 实例（baseURL + token 拦截器）
├── views/                # 页面
│   ├── ProductView.vue       # 商品列表（搜索/筛选/分类）
│   ├── LoginView.vue         # 登录
│   ├── RegisterView.vue      # 注册
│   ├── CartView.vue          # 购物车 + 结算
│   ├── OrderView.vue         # 我的订单
│   ├── OrderDetailView.vue   # 订单详情
│   └── AdminProductView.vue  # 商品管理后台（admin only）
├── App.vue
├── main.js
└── style.css
```

## 路由表

| 路径 | 页面 | 权限 |
|---|---|---|
| `/` | 商品首页 | 公开（未登录重定向到 /login） |
| `/login` | 登录 | 公开 |
| `/register` | 注册 | 公开 |
| `/cart` | 购物车 | 需登录 |
| `/orders` | 我的订单 | 需登录 |
| `/orders/:id` | 订单详情 | 需登录 |
| `/admin/products` | 商品管理后台 | 需 admin 角色 |

## 鉴权机制

- 登录后 JWT token 存储在 `localStorage`
- Axios 请求拦截器自动附加 `Authorization: Bearer <token>`
- 路由守卫解析 token payload，校验登录态和 admin 角色
- admin 用户导航栏显示「管理后台」入口，普通用户不可见

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产包
npm run build

# 预览构建结果
npm run preview
```

默认开发服务器运行在 `http://localhost:5173`，API 请求代理到 `http://127.0.0.1:8000`（后端 FastAPI）。

## 后端依赖

前端需要配合 [后端服务](../backend/) 运行，数据库需要以下表：

- `users`（含 `role` 字段区分 admin）
- `products`（含 `category` 字段）
- `cart`
- `orders`
- `order_items`

管理员账号需要手动将 `users` 表中对应用户的 `role` 字段设为 `"admin"` 并重新登录。
