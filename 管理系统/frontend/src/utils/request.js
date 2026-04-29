import axios from "axios"

const request = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 5000
})

/**
 * ⭐请求拦截器：自动带 token
 */
request.interceptors.request.use(config => {
  const token = localStorage.getItem("token")

  if (token && token !== "undefined") {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

/**
 * ⭐响应拦截器
 */
request.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response?.status === 401) {
      console.log("未登录或token失效")
    }
    return Promise.reject(err)
  }
)

export default request