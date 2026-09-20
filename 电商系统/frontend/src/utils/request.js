import axios from "axios"
import { ElMessage } from "element-plus"

const request = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 15000
})

// 请求拦截器：自动注入 JWT，业务代码无需关心鉴权头
request.interceptors.request.use(
    config => {
        const token = localStorage.getItem("token")
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => Promise.reject(error)
)

// 响应拦截器：统一处理"全局性"错误——登录失效、权限不足、网络不可达。
// 业务错误（如"库存不足"）不在这里弹提示，交给调用方 catch 处理，避免重复提示。
request.interceptors.response.use(
    response => response,
    error => {
        const status = error.response?.status
        const detail = error.response?.data?.detail

        if (status === 401) {
            // token 过期或被篡改：清理登录态并回到登录页
            localStorage.removeItem("token")
            localStorage.removeItem("user")
            ElMessage.error("登录已失效，请重新登录")
            if (window.location.pathname !== "/login") {
                window.location.href = "/login"
            }
        } else if (status === 403) {
            ElMessage.error(detail || "没有权限执行该操作")
        } else if (!error.response) {
            ElMessage.error("网络异常，请确认后端服务已启动")
        }

        return Promise.reject(error)
    }
)

export default request
