import { defineStore } from 'pinia'
import { addCart, getCart, updateCart, deleteCart } from '../api/cart'

/**
 * 购物车全局状态（Pinia）
 *
 * 设计要点：
 * 1. 购物车数据只有一个来源（本 store），AppHeader 角标、购物车页、商品页加购全部读写这里，
 *    避免每个组件各自请求后端造成重复请求与状态不一致。
 * 2. 只有"加购"需要重新拉取后端：因为后端 POST /cart/ 不返回新建的购物车项，
 *    且同一商品重复加购会新增一行（后端未做合并），本地无法推断出 cart_id。
 * 3. 改数量、删除走"本地即时更新 + 后端同步"，不再整表重拉。
 * 4. `loaded` 标记用于页面间跳转时的复用：同一会话内不重复 GET 全量。
 */
export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    loading: false,
    loaded: false,
  }),

  getters: {
    // 商品总件数（数量求和），用于 Header 角标
    totalCount: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
    // 购物车总金额，前端计算避免多一次接口请求
    totalPrice: (state) =>
      state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    isEmpty: (state) => state.items.length === 0,
  },

  actions: {
    /**
     * 拉取购物车。
     * @param {boolean} force 为 true 时忽略本地缓存强制刷新
     */
    async fetch(force = false) {
      if (!localStorage.getItem('token')) {
        this.reset()
        return this.items
      }
      if (this.loaded && !force) {
        return this.items
      }
      this.loading = true
      try {
        const res = await getCart()
        this.items = Array.isArray(res.data) ? res.data : []
        this.loaded = true
      } finally {
        this.loading = false
      }
      return this.items
    },

    /** 加入购物车：后端不返回新项，故加购后刷新一次以拿到准确的 cart_id 与数量 */
    async add(productId, quantity = 1) {
      await addCart({ product_id: productId, quantity })
      await this.fetch(true)
      return this.totalCount
    },

    /** 修改数量：本地即时生效，失败时由调用方回滚（重新 fetch） */
    async changeQuantity(cartId, quantity) {
      await updateCart(cartId, { quantity })
      const target = this.items.find((item) => item.cart_id === cartId)
      if (target) {
        target.quantity = quantity
      }
    },

    /** 删除条目：本地移除，不再整表重拉 */
    async remove(cartId) {
      await deleteCart(cartId)
      this.items = this.items.filter((item) => item.cart_id !== cartId)
    },

    /** 下单成功后清空本地购物车（后端已在同一事务中清空购物车表） */
    clearLocal() {
      this.items = []
      this.loaded = true
    },

    /** 退出登录 / 未登录时重置，避免串号 */
    reset() {
      this.items = []
      this.loaded = false
      this.loading = false
    },
  },
})
