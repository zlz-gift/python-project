import request from "@/utils/request"

/**
 * 🔐 登录
 * FastAPI: OAuth2PasswordRequestForm（必须 x-www-form-urlencoded）
 */
export const login = (data) => {
  return request({
    url: "/user/login",
    method: "post",
    data: new URLSearchParams(data)
  })
}

/**
 * 👤 注册用户
 */
export const createUser = (data) => {
  return request({
    url: "/user/register",
    method: "post",
    data
  })
}

/**
 * 🙋 当前登录用户信息
 */
export const getMe = () => {
  return request({
    url: "/user/me",
    method: "get"
  })
}

/**
 * 📋 用户列表（⭐已统一分页参数）
 * 支持：page / size / keyword
 */
export const getUserList = (params) => {
  return request({
    url: "/user/list",
    method: "get",
    params
  })
}

/**
 * ❌ 删除用户
 */
export const deleteUser = (id) => {
  return request({
    url: `/user/${id}`,
    method: "delete"
  })
}

/**
 * ✏️ 更新用户
 */
export const updateUser = (id, data) => {
  return request({
    url: `/user/${id}`,
    method: "put",
    data
  })
}