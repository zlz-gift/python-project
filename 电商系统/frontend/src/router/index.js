import {
    createRouter,
    createWebHistory
} from "vue-router"
import ProductView from "../views/ProductView.vue"
import LoginView from "../views/LoginView.vue"
import CartView from "../views/CartView.vue"
import RegisterView from "../views/RegisterView.vue"
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
    component: CartView
    },
    {
    path: "/register",
    component: RegisterView
    }
]

const router = createRouter({

    history: createWebHistory(),

    routes
})

router.beforeEach((to, from, next) => {

    const token = localStorage.getItem(
        "token"
    )

    if (
        to.path !== "/login"&&to.path !== "/register"
        && !token
    ) {

        next("/login")

    } else {

        next()
    }
})

export default router

const submitOrder = async () => {

  const res = await request.post("/order/create", null, {
    params: {
      user_id: 1,
      total_price: totalPrice.value
    }
  })

  ElMessage.success(res.data.msg)
}