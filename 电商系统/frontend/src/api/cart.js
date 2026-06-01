import request from "../utils/request"

export function addCart(data) {
    return request({
        url: "/cart/",
        method: "post",
        data
    })
}

export function getCart() {
    return request({
        url: "/cart/",
        method: "get"
    })
}

export function updateCart(id, data) {
    return request({
        url: `/cart/${id}`,
        method: "put",
        data
    })
}

export function deleteCart(id) {
    return request({
        url: `/cart/${id}`,
        method: "delete"
    })
}
