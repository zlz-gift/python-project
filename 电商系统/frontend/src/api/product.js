import request from "../utils/request"

export function getProducts() {

    return request({

        url: "/products/",

        method: "get"
    })
}