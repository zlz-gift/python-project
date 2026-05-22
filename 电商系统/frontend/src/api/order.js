import request from "../utils/request"

export function createOrder() {
    return request({
        url: "/order/create",
        method: "post"
    })
}

export function getOrders() {
    return request({
        url: "/order/",
        method: "get"
    })
}

export function getOrderById(id) {
    return request({
        url: `/order/${id}`,
        method: "get"
    })
}
