import {
    createRouter,
    createWebHistory
} from "vue-router"
import ProductView from "../views/ProductView.vue"
import LoginView from "../views/LoginView.vue"
import CartView from "../views/CartView.vue"
import RegisterView from "../views/RegisterView.vue"
import AdminProductView from "../views/AdminProductView.vue"
import OrderView from "../views/OrderView.vue"
import OrderDetailView from "../views/OrderDetailView.vue"

const routes = [
    {
        path: "/",
        component: ProductView
    },
    {
        path: "/login",
        component: LoginView
    },
    {
        path: "/cart",
        component: CartView,
        meta: { requiresAuth: true }
    },
    {
        path: "/register",
        component: RegisterView
    },
    {
        path: "/orders",
        component: OrderView,
        meta: { requiresAuth: true }
    },
    {
        path: "/orders/:id",
        component: OrderDetailView,
        meta: { requiresAuth: true }
    },
    {
        path: "/admin/products",
        component: AdminProductView,
        meta: { requiresAuth: true, requiresAdmin: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

function parseToken(token) {
    try {
        const payload = token.split(".")[1]
        return JSON.parse(atob(payload))
    } catch {
        return {}
    }
}

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token")
    const publicPaths = ["/login", "/register"]

    if (!token && !publicPaths.includes(to.path)) {
        next("/login")
        return
    }

    if (to.meta.requiresAdmin) {
        const payload = parseToken(token)
        if (payload.role !== "admin") {
            next("/")
            return
        }
    }

    next()
})

export default router